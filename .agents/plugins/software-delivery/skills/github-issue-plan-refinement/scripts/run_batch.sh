#!/usr/bin/env bash
# Review batch entry point for the github-issue-plan-refinement skill.
#
# This is the single user-facing entry point. `run_review.sh` is an
# internal worker that this script dispatches; direct invocation of
# `run_review.sh` is supported for debugging only.
#
# Usage:
#   run_batch.sh --main <codex|claude> --concurrency <N> \
#                --issue <N> --round <K> \
#                [--repo <owner/name>] [--effort <low|medium|high>]
#                [--dry-run]
#
# A batch consumes `concurrency` consecutive round numbers starting at
# `--round K`, i.e. rounds K, K+1, ..., K+N-1. Each round maps to one
# reviewer worker and its own `round-<n>/` directory; workers share no
# state mid-batch. The next invocation should pass `--round (K + N)`.
#
# Reviewer distribution inside the batch:
#   others = 0                         when N == 1
#   others = max(1, round(N * 0.3))    when N >= 2
#   main   = N - others
# The "other" reviewer is claude when --main is codex, and vice versa.
# Main slots take the lower round numbers; other slots take the upper.
#
# Before dispatch, the orchestrator reads the immutable manifest owned
# by round K-1, then concatenates that explicit previous batch's
# final.md files into a single prior-feedback file. All workers in the
# batch see the same prior context and never race on sibling results.
# If any worker in the previous batch failed, the prior file is empty.
#
# On success prints one TSV line per round to stdout:
#   <round>\t<reviewer>\t<round-dir>
# Exits non-zero if any worker fails; surviving rounds' artifacts
# remain on disk for inspection.
#
# --dry-run prints the planned rounds to stdout without dispatching.

set -euo pipefail

script_dir="$(cd "$(dirname "$0")" && pwd)"
# shellcheck disable=SC1091
. "${script_dir}/lib.sh"

usage() { iir_print_usage "$0"; }

main=""
concurrency=""
issue=""
round=""
repo=""
effort="high"
dry_run=0

while [ $# -gt 0 ]; do
    case "$1" in
        --main)        main="${2:-}";        shift 2 ;;
        --concurrency) concurrency="${2:-}"; shift 2 ;;
        --issue)       issue="${2:-}";       shift 2 ;;
        --round)       round="${2:-}";       shift 2 ;;
        --repo)        repo="${2:-}";        shift 2 ;;
        --effort)      effort="${2:-}";      shift 2 ;;
        --dry-run)     dry_run=1;            shift ;;
        -h|--help)     usage; exit 0 ;;
        *)
            echo "unknown argument: $1" >&2
            usage >&2
            exit 64
            ;;
    esac
done

for name in main concurrency issue round; do
    value="$(eval "printf '%s' \"\${$name}\"")"
    if [ -z "$value" ]; then
        echo "missing required argument: --${name}" >&2
        exit 64
    fi
done

case "$main" in
    codex)  other="claude" ;;
    claude) other="codex"  ;;
    *)
        echo "--main must be 'codex' or 'claude', got '${main}'" >&2
        exit 64
        ;;
esac

if ! [[ "$concurrency" =~ ^[0-9]+$ ]] || [ "$concurrency" -lt 1 ]; then
    echo "--concurrency must be a positive integer (>= 1), got '${concurrency}'" >&2
    exit 64
fi

if ! [[ "$issue" =~ ^[0-9]+$ ]]; then
    echo "--issue must be a positive integer, got '${issue}'" >&2
    exit 64
fi

if ! [[ "$round" =~ ^[0-9]+$ ]] || [ "$round" -lt 1 ]; then
    echo "--round must be a positive integer (>= 1), got '${round}'" >&2
    exit 64
fi

case "$effort" in
    low|medium|high) ;;
    *)
        echo "--effort must be low, medium, or high; got '${effort}'" >&2
        exit 64
        ;;
esac

if [ "$concurrency" -gt 5 ]; then
    echo "notice: --concurrency=${concurrency} multiplies reviewer cost by ${concurrency}x and may trip API rate limits" >&2
fi

if [ -n "$repo" ] && ! iir_validate_repo "$repo"; then
    echo "--repo must be a safe owner/name identifier, got '${repo}'" >&2
    exit 64
fi

others_count="$(iir_others_count "$concurrency")"
main_count=$((concurrency - others_count))
batch_start="$round"
batch_end=$((batch_start + concurrency - 1))
batch_manifest_header="$(printf 'version\tbatch_start\tbatch_end\tconcurrency\tmain\tother\teffort')"

# Validate and expose one immutable previous-batch manifest. The caller
# supplies the expected final round, which must be K-1 for a new batch.
previous_batch_start=0
previous_batch_end=0
previous_batch_complete=1
load_previous_batch_manifest() {
    local manifest="$1"
    local expected_end="$2"
    local line_count header record tab
    local version manifest_start manifest_end manifest_concurrency
    local manifest_main manifest_other manifest_effort extra
    local expected_concurrency n marker state

    if [ ! -f "$manifest" ]; then
        echo "previous batch manifest not found: $manifest" >&2
        return 1
    fi

    line_count="$(awk 'END { print NR }' "$manifest")"
    header="$(sed -n '1p' "$manifest")"
    record="$(sed -n '2p' "$manifest")"
    if [ "$line_count" -ne 2 ] || [ "$header" != "$batch_manifest_header" ]; then
        echo "invalid previous batch manifest structure: $manifest" >&2
        return 1
    fi

    tab="$(printf '\t')"
    IFS="$tab" read -r version manifest_start manifest_end manifest_concurrency \
        manifest_main manifest_other manifest_effort extra <<< "$record"

    if [ "$version" != "1" ] ||
       ! [[ "$manifest_start" =~ ^[0-9]+$ ]] || [ "$manifest_start" -lt 1 ] ||
       ! [[ "$manifest_end" =~ ^[0-9]+$ ]] || [ "$manifest_end" -lt "$manifest_start" ] ||
       ! [[ "$manifest_concurrency" =~ ^[0-9]+$ ]] || [ "$manifest_concurrency" -lt 1 ] ||
       [ -n "$extra" ]; then
        echo "invalid previous batch manifest values: $manifest" >&2
        return 1
    fi

    expected_concurrency=$((manifest_end - manifest_start + 1))
    if [ "$manifest_end" -ne "$expected_end" ] || [ "$manifest_concurrency" -ne "$expected_concurrency" ]; then
        echo "previous batch manifest does not end at round ${expected_end}: $manifest" >&2
        return 1
    fi
    case "$manifest_main:$manifest_other" in
        codex:claude|claude:codex) ;;
        *)
            echo "invalid reviewer pair in previous batch manifest: $manifest" >&2
            return 1
            ;;
    esac
    case "$manifest_effort" in
        low|medium|high) ;;
        *)
            echo "invalid effort in previous batch manifest: $manifest" >&2
            return 1
            ;;
    esac

    n="$manifest_start"
    while [ "$n" -le "$manifest_end" ]; do
        marker="$(head -n 1 "${round_root}/round-${n}/batch-start" 2>/dev/null || true)"
        state="$(head -n 1 "${round_root}/round-${n}/state" 2>/dev/null || true)"
        if [ "$marker" != "$manifest_start" ]; then
            echo "round ${n} does not belong to previous batch ${manifest_start}" >&2
            return 1
        fi
        case "$state" in
            succeeded) ;;
            failed) previous_batch_complete=0 ;;
            *)
                echo "round ${n} has invalid terminal state '${state}'" >&2
                return 1
                ;;
        esac
        n=$((n + 1))
    done

    previous_batch_start="$manifest_start"
    previous_batch_end="$manifest_end"
}

# Assign rounds to reviewers in a stable order: main on the lower
# rounds, other on the upper.
rounds=()
reviewers=()
i=0
while [ "$i" -lt "$concurrency" ]; do
    r=$((batch_start + i))
    if [ "$i" -lt "$main_count" ]; then
        reviewer="$main"
    else
        reviewer="$other"
    fi
    rounds+=("$r")
    reviewers+=("$reviewer")
    i=$((i + 1))
done

if [ "$dry_run" -eq 1 ]; then
    printf 'plan issue=%s main=%s effort=%s concurrency=%s rounds=%s..%s (main=%d other=%d)\n' \
        "$issue" "$main" "$effort" "$concurrency" "$batch_start" "$batch_end" \
        "$main_count" "$others_count"
    i=0
    while [ "$i" -lt "${#rounds[@]}" ]; do
        printf '  round=%s  reviewer=%s\n' "${rounds[$i]}" "${reviewers[$i]}"
        i=$((i + 1))
    done
    printf 'next-round: %s\n' "$((batch_end + 1))"
    exit 0
fi

run_review="${script_dir}/run_review.sh"
if [ ! -x "$run_review" ]; then
    echo "helper not executable: $run_review" >&2
    exit 70
fi

if [ -z "$repo" ]; then
    if ! command -v gh >/dev/null 2>&1; then
        echo "gh not on PATH and --repo not given; cannot resolve repo" >&2
        exit 72
    fi
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
mkdir -p "$round_root"

# Resolve the exact previous batch from round K-1. Its manifest, rather
# than the new concurrency value, owns the previous batch boundaries.
if [ "$batch_start" -gt 1 ]; then
    previous_last=$((batch_start - 1))
    previous_marker_file="${round_root}/round-${previous_last}/batch-start"
    if [ ! -f "$previous_marker_file" ]; then
        echo "cannot resolve previous batch from missing marker: $previous_marker_file" >&2
        exit 73
    fi
    previous_start="$(head -n 1 "$previous_marker_file")"
    if ! [[ "$previous_start" =~ ^[0-9]+$ ]] || [ "$previous_start" -lt 1 ] || [ "$previous_start" -gt "$previous_last" ]; then
        echo "invalid previous batch marker in $previous_marker_file" >&2
        exit 73
    fi
    load_previous_batch_manifest "${round_root}/batch-${previous_start}.tsv" "$previous_last" || exit 73
fi

batch_manifest="${round_root}/batch-${batch_start}.tsv"
prior_blob="${round_root}/prior-for-batch-${batch_start}.md"
if [ -e "$batch_manifest" ] || [ -e "$prior_blob" ]; then
    echo "batch artifacts already exist; batch starts are immutable: ${batch_start}" >&2
    exit 73
fi

# Atomically claim every round before writing batch artifacts or
# launching workers. A collision aborts without modifying the existing
# round and releases only directories claimed by this invocation.
claimed_round_dirs=()
cleanup_claimed_round_dirs() {
    local claimed
    for claimed in "${claimed_round_dirs[@]}"; do
        rm -f -- "${claimed}/batch-start" "${claimed}/state"
        rmdir "$claimed" 2>/dev/null || true
    done
}

i=0
while [ "$i" -lt "${#rounds[@]}" ]; do
    r="${rounds[$i]}"
    round_dir="${round_root}/round-${r}"
    if ! mkdir "$round_dir" 2>/dev/null; then
        echo "round directory already exists; round numbers are immutable: $round_dir" >&2
        cleanup_claimed_round_dirs
        exit 73
    fi
    claimed_round_dirs+=("$round_dir")
    printf '%s\n' "$batch_start" > "${round_dir}/batch-start"
    printf '%s\n' "claimed" > "${round_dir}/state"
    i=$((i + 1))
done

if ! {
    printf '%s\n' "$batch_manifest_header"
    printf '1\t%s\t%s\t%s\t%s\t%s\t%s\n' \
        "$batch_start" "$batch_end" "$concurrency" "$main" "$other" "$effort"
} > "$batch_manifest"; then
    rm -f -- "$batch_manifest"
    cleanup_claimed_round_dirs
    exit 74
fi

# Compose one immutable prior-feedback file. A partial/failed previous
# batch is intentionally excluded because it was never consolidated.
if ! : > "$prior_blob"; then
    rm -f -- "$batch_manifest" "$prior_blob"
    cleanup_claimed_round_dirs
    exit 74
fi
if [ "$previous_batch_start" -gt 0 ] && [ "$previous_batch_complete" -eq 1 ]; then
    n="$previous_batch_start"
    while [ "$n" -le "$previous_batch_end" ]; do
        candidate="${round_root}/round-${n}/final.md"
        if [ ! -s "$candidate" ]; then
            echo "succeeded previous round has no final message: $candidate" >&2
            rm -f -- "$batch_manifest" "$prior_blob"
            cleanup_claimed_round_dirs
            exit 73
        fi
        {
            printf '### From: round-%s\n\n' "$n"
            cat "$candidate"
            printf '\n\n'
        } >> "$prior_blob"
        n=$((n + 1))
    done
fi

# Dispatch workers after all round claims and batch inputs are durable.
pids=()
logs=()
i=0
while [ "$i" -lt "${#rounds[@]}" ]; do
    r="${rounds[$i]}"
    reviewer="${reviewers[$i]}"
    log_file="${round_root}/round-${r}/dispatch.log"
    logs+=("$log_file")
    (
        "$run_review" \
            --reviewer "$reviewer" \
            --issue "$issue" \
            --round "$r" \
            --repo "$repo" \
            --effort "$effort" \
            --batch-start "$batch_start" \
            --prior-feedback-file "$prior_blob"
    ) > "$log_file" 2>&1 &
    pids+=("$!")
    echo "started round=${r} reviewer=${reviewer} pid=$!" >&2
    i=$((i + 1))
done

# Wait and tally.
failed=0
i=0
while [ "$i" -lt "${#pids[@]}" ]; do
    pid="${pids[$i]}"
    r="${rounds[$i]}"
    reviewer="${reviewers[$i]}"
    log_file="${logs[$i]}"
    if wait "$pid"; then
        echo "round=${r} reviewer=${reviewer}: ok" >&2
    else
        status=$?
        echo "round=${r} reviewer=${reviewer}: failed (exit ${status}); see ${log_file}" >&2
        failed=1
    fi
    i=$((i + 1))
done

# Emit TSV: <round>\t<reviewer>\t<round-dir>
i=0
while [ "$i" -lt "${#rounds[@]}" ]; do
    r="${rounds[$i]}"
    reviewer="${reviewers[$i]}"
    printf '%s\t%s\t%s/round-%s\n' "$r" "$reviewer" "$round_root" "$r"
    i=$((i + 1))
done

exit "$failed"
