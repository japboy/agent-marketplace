#!/usr/bin/env bash
# Internal worker for the github-issue-plan-refinement skill.
#
# `run_batch.sh` is the documented entry point for users; this script
# is the per-round worker it dispatches. Direct invocation is
# supported only for debugging.
#
# Usage:
#   run_review.sh --reviewer <codex|claude> --issue <N> --round <K>
#                 [--repo <owner/name>]
#                 [--effort <low|medium|high>]
#                 [--prior-feedback-file <path>]
#                 [--batch-start <K>]  (internal; set by run_batch.sh)
#
# One invocation runs one reviewer CLI against the current issue body
# and writes artifacts into round-<K>/. A round number identifies one
# reviewer pass; a batch of size N assigns distinct round numbers
# (K..K+N-1) to its workers, so there is never more than one
# reviewer pass per round directory.
#
# On success prints the round working directory path to stdout and
# exits 0. The directory contains:
#   current_body.md   issue body at the start of the round
#   prompt.md         prompt sent to the reviewer
#   raw.txt           full reviewer stdout (diagnostic)
#   final.md          reviewer's final message (authoritative)
#   reviewer          name of the reviewer CLI used (audit)
#   effort            requested reasoning effort (audit)
#   batch-start       owning batch's first round number
#   state             claimed | running | succeeded | failed
#
# Prior-round feedback handling:
#   --prior-feedback-file <path>   use the given file verbatim as the
#                                  prior-feedback block in the prompt.
#                                  Empty or missing file is treated as
#                                  "(no prior round)".
#   (no flag)                      fall back to the most recent
#                                  round-<M>/final.md with M < K.

set -euo pipefail

script_dir="$(cd "$(dirname "$0")" && pwd)"
# shellcheck disable=SC1091
. "${script_dir}/lib.sh"

usage() { iir_print_usage "$0"; }

reviewer=""
issue=""
round=""
repo=""
effort="high"
prior_feedback_file=""
batch_start=""

while [ $# -gt 0 ]; do
    case "$1" in
        --reviewer)             reviewer="${2:-}";             shift 2 ;;
        --issue)                issue="${2:-}";                shift 2 ;;
        --round)                round="${2:-}";                shift 2 ;;
        --repo)                 repo="${2:-}";                 shift 2 ;;
        --effort)               effort="${2:-}";               shift 2 ;;
        --prior-feedback-file)  prior_feedback_file="${2:-}";  shift 2 ;;
        --batch-start)          batch_start="${2:-}";          shift 2 ;;
        -h|--help)              usage; exit 0 ;;
        *)
            echo "unknown argument: $1" >&2
            usage >&2
            exit 64
            ;;
    esac
done

for name in reviewer issue round; do
    value="$(eval "printf '%s' \"\${$name}\"")"
    if [ -z "$value" ]; then
        echo "missing required argument: --${name}" >&2
        exit 64
    fi
done

case "$reviewer" in
    codex|claude) ;;
    *)
        echo "--reviewer must be 'codex' or 'claude', got '${reviewer}'" >&2
        exit 64
        ;;
esac

case "$effort" in
    low|medium|high) ;;
    *)
        echo "--effort must be low, medium, or high; got '${effort}'" >&2
        exit 64
        ;;
esac

if ! [[ "$issue" =~ ^[0-9]+$ ]]; then
    echo "--issue must be a positive integer, got '${issue}'" >&2
    exit 64
fi

if ! [[ "$round" =~ ^[0-9]+$ ]] || [ "$round" -lt 1 ]; then
    echo "--round must be a positive integer (>= 1), got '${round}'" >&2
    exit 64
fi

if [ -n "$batch_start" ] && { ! [[ "$batch_start" =~ ^[0-9]+$ ]] || [ "$batch_start" -lt 1 ] || [ "$batch_start" -gt "$round" ]; }; then
    echo "--batch-start must be a positive integer no greater than --round, got '${batch_start}'" >&2
    exit 64
fi

if [ -n "$prior_feedback_file" ] && [ ! -e "$prior_feedback_file" ]; then
    echo "--prior-feedback-file not found: $prior_feedback_file" >&2
    exit 64
fi

for tool in gh python3; do
    if ! command -v "$tool" >/dev/null 2>&1; then
        echo "required tool not found on PATH: ${tool}" >&2
        exit 72
    fi
done

if [ "$reviewer" = "claude" ] && ! command -v jq >/dev/null 2>&1; then
    echo "jq is required when --reviewer is 'claude'" >&2
    exit 72
fi

if ! command -v "$reviewer" >/dev/null 2>&1; then
    echo "reviewer CLI not found on PATH: ${reviewer}" >&2
    exit 72
fi

if [ -z "$repo" ]; then
    repo="$(gh repo view --json nameWithOwner -q .nameWithOwner)"
fi
if ! iir_validate_repo "$repo"; then
    echo "--repo must be a safe owner/name identifier, got '${repo}'" >&2
    exit 64
fi

tmpdir="$(iir_detect_tmpdir)" || {
    echo "cannot detect OS temp directory" >&2
    exit 74
}

round_root="$(iir_round_root "$tmpdir" "$repo" "$issue")"
workdir="${round_root}/round-${round}"
mkdir -p "$round_root"

if [ -n "$batch_start" ]; then
    if [ ! -f "${round_root}/batch-${batch_start}.tsv" ]; then
        echo "owning batch manifest not found: ${round_root}/batch-${batch_start}.tsv" >&2
        exit 73
    fi
    if [ ! -d "$workdir" ]; then
        echo "round directory was not claimed by run_batch.sh: $workdir" >&2
        exit 73
    fi
    claimed_batch="$(head -n 1 "${workdir}/batch-start" 2>/dev/null || true)"
    claimed_state="$(head -n 1 "${workdir}/state" 2>/dev/null || true)"
    if [ "$claimed_batch" != "$batch_start" ] || [ "$claimed_state" != "claimed" ]; then
        echo "round claim mismatch for ${workdir}: batch-start='${claimed_batch}' state='${claimed_state}'" >&2
        exit 73
    fi
else
    batch_start="$round"
    if ! mkdir "$workdir" 2>/dev/null; then
        echo "round directory already exists; round numbers are immutable: $workdir" >&2
        exit 73
    fi
    printf '%s\n' "$batch_start" > "${workdir}/batch-start"
    printf '%s\n' "claimed" > "${workdir}/state"
fi

round_succeeded=0
finish_round() {
    status=$?
    trap - EXIT
    if [ "$status" -eq 0 ] && [ "$round_succeeded" -eq 1 ]; then
        printf '%s\n' "succeeded" > "${workdir}/state" || true
    else
        printf '%s\n' "failed" > "${workdir}/state" || true
    fi
    exit "$status"
}
trap finish_round EXIT
printf '%s\n' "running" > "${workdir}/state"

gh issue view "$issue" --repo "$repo" --json body -q .body \
    > "${workdir}/current_body.md"

# Resolve the prior-feedback source file.
effective_prior=""
if [ -n "$prior_feedback_file" ]; then
    effective_prior="$prior_feedback_file"
else
    prior_candidate=$((round - 1))
    while [ "$prior_candidate" -ge 1 ]; do
        candidate="${round_root}/round-${prior_candidate}/final.md"
        if [ -s "$candidate" ]; then
            effective_prior="$candidate"
            break
        fi
        prior_candidate=$((prior_candidate - 1))
    done
fi

if [ -n "$effective_prior" ]; then
    python3 - "$round_root" "$effective_prior" <<'PY'
import pathlib
import sys

base = pathlib.Path(sys.argv[1]).resolve()
candidate = pathlib.Path(sys.argv[2]).resolve()
try:
    candidate.relative_to(base)
except ValueError as exc:
    raise SystemExit(f"prior-feedback file escapes round root: {candidate}") from exc
PY
fi

template_path="${script_dir}/../references/reviewer_prompt.md"

python3 - "$template_path" "${workdir}/current_body.md" \
        "${effective_prior:-}" "${workdir}/prompt.md" \
        "$repo" "$issue" "$round" <<'PY'
import pathlib
import sys

tpl_path, body_path, prior_path, out_path, repo, issue, round_ = sys.argv[1:8]

raw = pathlib.Path(tpl_path).read_text()
begin = "---BEGIN-TEMPLATE---\n"
end = "\n---END-TEMPLATE---"
if begin not in raw or end not in raw:
    raise SystemExit(f"template markers missing in {tpl_path}")
template = raw.split(begin, 1)[1].split(end, 1)[0]

body = pathlib.Path(body_path).read_text()
if prior_path:
    prior = pathlib.Path(prior_path).read_text().strip() or "(no prior round)"
else:
    prior = "(no prior round)"

prompt = (template
          .replace("{{repo}}", repo)
          .replace("{{issue}}", issue)
          .replace("{{round}}", round_)
          .replace("{{current_body}}", body)
          .replace("{{prior_feedback}}", prior))

pathlib.Path(out_path).write_text(prompt)
PY

printf '%s\n' "$reviewer" > "${workdir}/reviewer"
printf '%s\n' "$effort" > "${workdir}/effort"

# Pass one explicit, cross-client effort value so local CLI defaults cannot
# silently change the review configuration.
case "$reviewer" in
    codex)
        codex exec \
            --ignore-user-config \
            --ignore-rules \
            --ephemeral \
            --sandbox read-only \
            --cd "$workdir" \
            --skip-git-repo-check \
            -c "model_reasoning_effort=\"${effort}\"" \
            -o "${workdir}/final.md" \
            - \
            < "${workdir}/prompt.md" \
            > "${workdir}/raw.txt" 2>&1
        ;;
    claude)
        claude -p \
            --safe-mode \
            --tools "" \
            --permission-mode plan \
            --no-session-persistence \
            --effort "$effort" \
            --output-format json \
            < "${workdir}/prompt.md" \
            > "${workdir}/raw.txt" 2>&1
        jq -r '.result // ""' "${workdir}/raw.txt" > "${workdir}/final.md"
        ;;
esac

if [ ! -s "${workdir}/final.md" ]; then
    echo "reviewer produced no final message; see ${workdir}/raw.txt" >&2
    exit 75
fi

round_succeeded=1
printf '%s\n' "$workdir"
