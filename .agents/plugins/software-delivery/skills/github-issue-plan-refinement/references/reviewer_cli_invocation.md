# Reviewer CLI Invocation

How `run_review.sh` invokes each reviewer CLI. The skill accepts the finite cross-client set `low`,
`medium`, or `high`, defaults to `high`, and records the selected value in each round. The binding
rule lives in [SKILL.md](../SKILL.md); this file documents the implementation details.

## Codex

```bash
codex exec \
    --ignore-user-config \
    --ignore-rules \
    --ephemeral \
    --sandbox read-only \
    --cd "<workdir>" \
    --skip-git-repo-check \
    -c 'model_reasoning_effort="<low|medium|high>"' \
    -o "<workdir>/final.md" \
    - \
    < "<workdir>/prompt.md" \
    > "<workdir>/raw.txt" 2>&1
```

- `--ignore-user-config` and `--ignore-rules`: exclude local user/project customizations from the
  reviewer process, so they cannot add action-taking instructions or capabilities.
- `--ephemeral`: does not persist a session.
- `--sandbox read-only`: denies workspace mutation by reviewer-issued commands.
- `--cd <workdir>` and `--skip-git-repo-check`: constrain the reviewer's working directory to the
  round artifacts without requiring it to be a Git checkout.
- `-c key=value`: TOML config override that wins over any `~/.codex/config.toml` setting.
- `model_reasoning_effort`: this skill deliberately uses the portable subset `low`, `medium`, or
  `high`.
- `-o` / `--output-last-message`: writes the final assistant message to the given file. The skill
  reads `final.md` from this path; the full transcript stays in `raw.txt`.
- A final `-` reads the prompt from stdin. This avoids command-line length limits and keeps the
  prompt out of process arguments.

## Claude Code

```bash
claude -p \
    --safe-mode \
    --tools "" \
    --permission-mode plan \
    --no-session-persistence \
    --effort "<low|medium|high>" \
    --output-format json \
    < "<workdir>/prompt.md" \
    > "<workdir>/raw.txt" 2>&1
jq -r '.result // ""' "<workdir>/raw.txt" > "<workdir>/final.md"
```

- `--safe-mode`: excludes filesystem customizations, including project instructions, skills,
  plugins, hooks, and MCP servers, while retaining the normal authentication and model settings.
- `--tools ""`: exposes no tools to the reviewer.
- `--permission-mode plan`: selects Claude Code's non-executing planning mode as a second explicit
  guard against actions.
- `--no-session-persistence`: does not save or resume a reviewer session.
- `--effort`: this skill deliberately uses `low`, `medium`, or `high`.
- `--output-format json`: emits a single JSON object whose `.result` field contains the final
  message.
- `jq -r '.result // ""'`: extracts the final message into `final.md`. Empty string fallback
  prevents `null` text from reaching the file.
- Omitting a positional prompt makes `-p` read the prompt from stdin, avoiding command-line length
  limits and process-argument exposure.

## Isolation invariant

Both invocation forms are review-only: no tool access, no persistent session, and no inherited
project customization. Do not remove one of these flags unless the Skill's review-only contract is
changed deliberately and revalidated against the corresponding CLI's built-in `--help` output.

## Diagnostics

Both modes capture full session output to `raw.txt`. Inspect this file when:

- `final.md` is empty (run_review.sh exits 75)
- The reviewer reports an error
- A worker fails inside `run_batch.sh` (also see the per-round `dispatch.log`)

## Why make effort explicit

An explicit batch value prevents review configuration from drifting with unrelated local CLI
settings. Keeping one value across a batch also makes rounds comparable without asserting that
maximum effort is universally optimal. See [cost_and_rate_limits.md](cost_and_rate_limits.md).
