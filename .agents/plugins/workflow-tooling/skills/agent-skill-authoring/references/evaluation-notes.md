# Evaluation Notes

This file records validation evidence for changes to the `agent-skill-authoring` skill. It is
update/audit context, not runtime instruction.

## 2026-11-18 Standards and Completion Review

Status: **Accepted for source-backed corrections. Provisional for broader behavioral effects.** The
comparison found a more precise standards review and passed the existing regression checks. The
cases provide limited evidence for the new completion and verification guidance.

### Comparison setup

- Previous version: Git commit `d6224a0324b0b0d4a6cd7328edac4ea70ea9f33c`.
- Candidate `SKILL.md` SHA-256: `8ff81570f7a4f3a84af53a27ff4f2a6e1b31374d5bf02a66aca16886e6558db3`.
  The staged candidate contained the updated guidance and references before this result and the
  changelog entry were recorded.
- Fixture: unchanged [evals/evals.json](../evals/evals.json) from the previous version. Each arm
  received the original prompts and was graded against the same 15 assertions.
- Target: Codex CLI 0.163.0, `gpt-6.1-sol` at medium reasoning effort. One fresh ephemeral session
  per case and version, with the same explicit skill-loading instruction, permissions, and cached
  offline validator. The runtime and its references were available read-only. The filesystem profile
  blocked other installed skill bodies and the evaluator's fixture. All six traces confirmed the
  intended `SKILL.md` was read.
- Excluded diagnostic attempts: Claude Code could not authenticate. The initial Codex run allowed
  access to unrelated local instructions. The fenced rerun supplied the results below.

### Results

Wall time is measured per run. Total tokens are the CLI's input plus output, including cached input.
Reasoning output is included in output.

| Case | Assertions, previous / candidate | Wall time in seconds, previous / candidate | Total tokens, previous / candidate |
| - | -: | -: | -: |
| 1. Create a portable skill | 5/5 / 5/5 | 82.662 / 70.811 | 326,730 / 272,465 |
| 2. Review standard compliance | 5/5 / 5/5 | 52.669 / 44.888 | 227,592 / 110,709 |
| 3. Review an anecdote-based edit | 5/5 / 5/5 | 49.377 / 47.766 | 145,726 / 143,189 |
| Total | 15/15 / 15/15 | 184.708 / 163.465 | 700,048 / 526,363 |

- Case 1: Both sessions produced only `review-changelog/SKILL.md` and passed the validator. An
  independent `skills-ref` 0.1.1 run passed on both files. The candidate defined a final comparison
  against the source. The previous output explicitly kept links from omitted entries. The candidate
  gave a general preservation rule with less detail for that edge case.
- Case 2: Both passed the original assertions. A supplemental check used the standard's
  [description field](https://agentskills.io/specification#description-field) and the
  [reference validator](https://github.com/agentskills/agentskills/blob/main/skills-ref/src/skills_ref/validator.py#L70-L84).
  The previous answer included a description rewrite in the minimum compliance fix. The candidate
  identified the invalid name as the format defect and recommended a more useful description and
  targeted reference links as authoring improvements. The supplemental result improved from fail to
  pass.
- Case 3: Both kept the update provisional, declined a universal five-step rollback rule, and
  specified a fixed-target comparison with quality, token, and duration evidence.

Cached input fell from 613,376 to 433,024 tokens. Uncached input rose from 81,369 to 88,278 and
output fell from 5,303 to 5,061. The elapsed and usage totals describe these runs. They provide
limited evidence about repeatable latency or cost. This suite exercises explicit loading in one
client and model. Implicit triggering, Claude Code execution, and the behavior of the generated
changelog skill on actual release notes remain unverified.

## 2026-07-31 LicenseUndecided Metadata Validation

Status: **Accepted as a non-behavioral metadata and packaging change.**

Target:

- Repository licensing state: `LicenseUndecided`
- Skill: `.agents/plugins/workflow-tooling/skills/agent-skill-authoring`
- Products: Codex and Claude Code

Checks and results:

- `mise run check`: passed dprint, Vale boundary fixtures, Vale prose lint, and `skills-ref`
  validation for all 12 Skills.
- Codex Plugin Creator validator: passed all five Plugin directories without a Plugin `license`
  field or license files.
- `claude plugin validate --strict`: passed the marketplace and all five Plugin directories without
  a Plugin `license` field or license files.
- Repository audit: found no distributed `LICENSE*` files, no `license` frontmatter or manifest
  fields, and no previous license identifiers or terms.

The Agent Skills specification and both product validators treat the removed fields and files as
optional. No trigger text or runtime instruction changed, so no behavioral improvement is claimed.

## 2026-07-31 Marketplace Migration Validation

Target:

- Skill: `.agents/plugins/workflow-tooling/skills/agent-skill-authoring`
- Validator: current PyPI `skills-ref` package via the `agentskills` executable
- Command:

  ```bash
  uvx --from skills-ref agentskills validate .agents/plugins/workflow-tooling/skills/agent-skill-authoring
  ```

Result:

```text
Valid skill: .agents/plugins/workflow-tooling/skills/agent-skill-authoring
```

Additional checks performed:

- Validated the containing Codex Plugin manifest with the bundled Plugin Creator validator.
- Validated the containing Claude Code Plugin manifest and marketplace catalog in strict mode.
- Confirmed the migrated Plugin tree contains no symbolic links.
- Confirmed migration changed only this skill's authoring-location wording, optional frontmatter,
  and maintenance records; no runtime behavior improvement is claimed.

Earlier entries retain their original `common/.agents/skills/` target paths as historical evidence.
Those paths no longer identify the canonical installed skill.

## 2026-05-30 Validation

Target:

- Skill: `common/.agents/skills/agent-skill-authoring`
- Validator: current PyPI `skills-ref` package via the `agentskills` executable
- Command:

  ```bash
  uvx --from skills-ref agentskills validate common/.agents/skills/agent-skill-authoring
  ```

Result:

```text
Valid skill: common/.agents/skills/agent-skill-authoring
```

Additional checks performed:

- Confirmed `SKILL.md` frontmatter description is within the 1024-character standard limit.
- Confirmed Markdown code fences are balanced.
- Confirmed local links from `SKILL.md` to `references/` files resolve.
- Confirmed `SKILL.md` remains below the 500-line recommendation after adding record/runtime
  separation guidance.

Evidence basis:

- Agent Skills specification and source for portable structure, frontmatter, progressive disclosure,
  and optional directories.
- OpenAI Codex skills documentation for Codex-specific discovery and `agents/openai.yaml` behavior.
- Claude Code skills documentation for Claude Code-specific frontmatter, dynamic context injection,
  and discovery behavior.
- SkillOpt v2 paper and arXiv source for bounded updates, validation gates, rejected-edit buffers,
  optimizer-side meta guidance, and compact deployed skills.

## 2026-07-25 Context-Engineering Review

Target:

- Skill: `common/.agents/skills/agent-skill-authoring`
- Validator: current PyPI `skills-ref` package via the `agentskills` executable
- Reviewing model/harness: Claude Opus 5 in Claude Code
- Evaluator: documentation cross-check against primary sources, not a scored rollout. No
  trigger-rate or benchmark run was performed for this revision.

Result:

```text
Valid skill: common/.agents/skills/agent-skill-authoring
```

Additional checks performed:

- `SKILL.md` is 498 lines, within the 500-line recommendation, after adding the new material and
  compressing duplicated content by a comparable amount.
- Markdown code fences are balanced (10 fence markers).
- All eight `references/` links from `SKILL.md` resolve to existing files.
- Frontmatter was not modified, so the 1024-character `description` limit is unaffected.

### Source changes found during review

- The Agent Skills standard site now publishes a `skill-creation` section: `quickstart`,
  `best-practices`, `optimizing-descriptions`, `using-scripts`, and `evaluating-skills`. None were
  in the previous source map.
- `developers.openai.com/codex/skills` and `developers.openai.com/codex/build-skills` now issue HTTP
  308 redirects to `learn.chatgpt.com/docs/build-skills`.
- Anthropic prompt-engineering documentation now resolves to `platform.claude.com`;
  `docs.claude.com` returns a 302 redirect.

### Fixed-target evidence: vendor model guidance

Recorded here rather than in `SKILL.md`, per the decision record on keeping model-specific guidance
out of runtime rules.

Claude Opus 5 (Anthropic, "Prompting Claude Opus 5"):

- Explicit verification instructions cause over-verification; removing them reduces wasted tokens
  with no loss in quality. The same applies to "double-check your answer" style re-check
  instructions.
- The effort parameter controls thinking volume, not visible output length. Response length and
  written-deliverable length must be prompted explicitly.
- Conservative review instructions such as "only report high-severity issues" are followed literally
  and reduce reported findings; the documented remedy is to report everything and filter in a
  separate pass.
- The model delegates to subagents more readily than prior models; explicit delegation criteria or
  deterministic caps are recommended, and subagents should not be used to verify the model's own
  work.
- Positive examples of a wanted communication style outperform instructions about what not to do.

GPT-5.6 Sol (OpenAI, "Prompting guidance for GPT-5.6 Sol"):

- Recommends removing repeated rules, style or process instructions that do not change behavior,
  examples that do not change behavior, and process instructions for behavior the model already
  performs reliably. Reported internal result: leaner system prompts improved evaluation scores by
  roughly 10-15% while reducing total tokens by 41-66% and cost by 33-67%.
- Recommends keeping the user-visible outcome, success criteria and stopping conditions,
  safety/business/evidence/permission constraints, and context-dependent tool-routing rules.
- Reserves ALWAYS, NEVER, must, and only for true invariants.
- Recommends a short preamble before the first tool call, then sparse outcome-based updates at phase
  changes, and no narration of routine tool calls.
- Before raising reasoning effort, recommends checking whether the prompt is missing a success
  criterion, dependency rule, tool-routing rule, or verification loop.

Convergence between the two, and with the standard site's "keep the skill lean" and "explain the
why" guidance, is what justified promoting these into the shared Instruction Calibration rules.
Model-specific numbers stayed here.

### Product context budgets

- Codex: startup skills list capped at 2% of the model's context window, or 8,000 characters when
  the window is unknown; descriptions are shortened first when many skills are installed.
- Claude Code: listing budget scales at 1% of the context window (`skillListingBudgetFraction`,
  `SLASH_COMMAND_TOOL_CHAR_BUDGET`); on overflow, descriptions are dropped starting with the
  least-invoked skills; each entry's combined `description` and `when_to_use` is capped at 1,536
  characters (`skillListingMaxDescChars`).
- Claude Code: after auto-compaction, only the first 5,000 tokens of each re-attached skill survive,
  within a combined 25,000-token budget filled from the most recently invoked skill.

### Not verified

- No trigger-rate measurement and no completed previous-version/candidate benchmark exist for this
  revision. A harness was built and the previous-version arm ran to completion, but the run was
  stopped before the candidate arm finished, so there is no comparison and no conclusion. The
  changes are documentation-derived, so the validation gate for behavioral edits remains open; the
  2026-07-25 changes are provisional and the new Instruction Calibration rules remain unmeasured.
- The `description` was not modified in this revision, so a trigger-rate evaluation would validate
  nothing about it. Run one only as a regression check.

### Harness facts for the next benchmark run

Verified on 2026-07-25 with Claude Code CLI 2.1.201 on darwin:

- The headless CLI defaults to `claude-opus-4-8`, and the `opus` alias also resolves to 4.8. Pass
  `--model claude-opus-5` explicitly, and confirm the actual model from the `modelUsage` key of the
  `--output-format json` envelope. Without this, the run silently measures a different target than
  intended.
- `~/.claude/skills` is a symlink into this repository, so the working-tree version of every skill
  is discoverable from any working directory, including temporary ones. A previous-version arm is
  therefore contaminated by default. Pass `--disallowedTools Skill` and hand the versioned skill
  path to the agent in the prompt instead of relying on discovery.
- `--output-format json` supplies `duration_ms`, `usage`, and `total_cost_usd`, which cover the
  `timing.json` fields the standard workflow expects.
- `--permission-mode acceptEdits` with a tool denylist completes file-writing runs headlessly with
  no permission denials.
- Observed cost and wall time per authoring task at `claude-opus-5`: roughly $0.70-$3.00 and 2-9
  minutes, scaling with turn count (8-23 turns).

### Repository helper path correction

- The canonical documented entrypoint is `~/.agents/skills/.system/skill-creator/`, matching the
  repository's user-facing symlink layout.
- On 2026-07-25 the directory resolved to this repository, but the four documented helper files
  resolved through self-referential child symlinks and failed regular-readable-file checks.
- Runtime guidance therefore keeps an explicit target check and portable fallback; it does not claim
  that the current symlink targets are usable.
