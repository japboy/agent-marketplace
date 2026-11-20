# Frontend Test Value Assessment Evaluation Notes

**Review state.** The report-entry correction and Storybook setup policy are `accepted` for the
Codex cases evaluated below. Claude Code manifest validation and distribution are verified. Its
generated-report behavior is unverified. The comparisons use synthetic cases from
[evals.json](../evals/evals.json).

## Pre-fix review on 2026-11-20

The review compared the version before the classification redesign with the redesigned version
before the single-test reporting fix. Each arm received the same browser-layout and checkout prompts
in fresh workspaces. The prompt instructed the agent to read its snapshot of the skill and
applicable bundled references. Codex CLI 0.169.0 used `gpt-6.2-sol` at low reasoning effort with
read-only sandboxing. Reviewers traced decisions to the generated text.

| Case | Before the redesign | Pre-fix redesign snapshot |
| - | - | - |
| Browser layout and stubbed API (case 7) | `MOVE_TO_E2E` despite identifying both setups as frontend integration. | `REWRITE_AT_SAME_LAYER` with a real browser, the same API stub, and Medium size. The test path and status appeared together in Decision Summary. Findings by Test contained scope, runtime, and size without that entry. |
| Checkout cart recovery after real sign-in | `MOVE_TO_E2E` with real sign-in, cart persistence, and return navigation. Retained the distinct payment-display protection. | `MOVE_TO_E2E` under the same boundary and coverage requirements. Findings by Test included the path and status together. |

| Case | Total tokens, before / pre-fix | Wall time, before / pre-fix |
| - | -: | -: |
| Browser layout | 71,037 / 90,880 | 17.238 s / 24.059 s |
| Checkout | 76,481 / 59,496 | 18.050 s / 22.463 s |

Token totals include cached input. Wall times are single observations for each case and arm. The
`SKILL.md` SHA-256 identifiers are
`f5843995c6b89116c2e523b3682477c9e123bd958ae20fc25db74609cf379cc4` for the prior version and
`8cfaff73d1366b292160ec27195907ebf3dfed95561a274bbb4ebb31273f24c6` for the pre-fix redesign.
[Agent Skills evaluation guidance](https://agentskills.io/skill-creation/evaluating-skills#running-evals)

The separate discovery check installed the skill under `.agents/skills/` and used one run per query
with default model and reasoning settings. The trace read `SKILL.md` for checkout test placement and
test-suite distribution. The implementation-only query about a clipped focus ring left it unread.
Both snapshots showed this pattern. The reporting fix preserves the discovery description.
[Agent Skills discovery guidance](https://agentskills.io/skill-creation/optimizing-descriptions#testing-whether-a-description-triggers)

## Report-entry correction on 2026-11-20

Compared the pre-fix redesign and the reporting correction on cases 4 and 5, with two separate runs
of case 7 per arm. Each run used a fresh temporary workspace, one skill snapshot, and the same case
prompt and explicit instruction to read that snapshot's `SKILL.md` and applicable references. Both
arms used Codex CLI 0.169.0, `gpt-6.2-sol`, low reasoning effort, ephemeral sessions, and a
read-only sandbox.

The mechanical check isolated `Findings by Test` and matched one top-level bullet per assessed test.
Its first line had to contain the backticked test path, an em dash, and the expected backticked
status. The check also verified that the corrected reports summarized their decisions without status
codes in `Decision Summary`. The exact-entry check passed in 0 of 4 pre-fix runs and 4 of 4
corrected runs. One pre-fix browser run put the status in the summary and listed scope, runtime, and
size under the findings. The other put the path and status together on an unbulleted line. The
corrected browser reports both started the sole finding with this entry:

```markdown
- `tests/SearchFlow.test.tsx` — `REWRITE_AT_SAME_LAYER`
```

Inspection confirmed that both corrected browser reports kept integration scope and the API stub,
required a real browser to expose the overlay, and recorded Medium for the proposed setup and
unknown for the current size. Case 4 retained the isolated unit scope and public DOM semantics. Case
5 retained both integration findings and included the suite discussion.

| Case | Total tokens, pre-fix / corrected | Wall time, pre-fix / corrected |
| - | -: | -: |
| 4. Single component | 59,309 / 65,319 | 17.518 s / 17.071 s |
| 5. Catalog suite | 91,175 / 63,726 | 25.704 s / 20.579 s |
| 7. Browser layout, first run | 92,698 / 91,826 | 25.067 s / 19.334 s |
| 7. Browser layout, second run | 91,306 / 62,506 | 36.252 s / 18.204 s |

Token totals include cached input. Wall times are observations for these runs. The corrected
`SKILL.md` SHA-256 is `fea8037271b44724ea8d7cfb9b8a3009d7c1579a887b0819da1fca677f412a5f`. The rubric
SHA-256 values are `f4c9815f39ed6b7446ce716cb78d72b1a891511c769148c58b29519996644d63` before the fix
and `436dc5790f3d201992137f64fed57f1db0616c650f382a458b7bbb9c982f4d0f` after it.

## Storybook test setup on 2026-11-20

Compared the preceding snapshot with the Storybook setup update on cases 1, 8, and 9. Each arm
received the same prompt for its case in a fresh workspace, with an explicit instruction to read its
own skill and relevant bundled references. Codex CLI 0.169.0 used `gpt-6.2-sol` at low reasoning
effort in ephemeral read-only sessions. The author inspected each report against the case evidence
and checked that each finding starts with the expected test path and status.

| Case | Before / after observation |
| - | - |
| 1. Suitable invitation story | Both used `ValidInvite` and its project annotations for integration coverage of the real form, hook, and client. Both proposed asserting confirmation and accessible inline error outcomes with HTTP fixtures. |
| 8. Missing public scenario | Both proposed a `Rejected` story and a unit test using its setup. The updated skill proposed composing the story with the supplied Jest preview annotations and cited the official Jest guide and implementation. Its test checked the alert and exact message. |
| 9. Required production shell | Both kept the `OpenDrawer` callback unit test and proposed browser integration coverage of Back with the production shell and native history. The reports identified the shell and adapter as the reason for the separate setup. |

The case 8 input was clarified to state that Jest already supports Portable Stories and applies the
preview annotations. The same clarified input was run against both snapshots. Case 7 was run as a
control with the updated skill. It kept integration scope and recommended a real browser for the
layout regression with the same API stub.

| Case | Total tokens, before / after | Wall time, before / after |
| - | -: | -: |
| 1. Invitation | 94,193 / 66,265 | 27.511 s / 24.895 s |
| 8. Rejected upload | 65,888 / 60,789 | 18.402 s / 23.880 s |
| 9. Native browser Back | 66,106 / 93,355 | 20.981 s / 23.073 s |
| 7. Browser layout control | — / 109,695 | — / 25.441 s |

Token totals include cached input. Wall times are observations for these runs. The `SKILL.md`
SHA-256 values are `fea8037271b44724ea8d7cfb9b8a3009d7c1579a887b0819da1fca677f412a5f` before the
update and `8d4d0632de46bfb4d23a1652bbb81c468478ecddfd035550b23c31e8b5a8a048` after it.

## Distribution and Claude Code

`mise run apm-test` verified clean installation and frozen replay for Claude and Codex package
targets. Claude Code 2.1.323 passed `claude plugin validate .agents/plugins/web-engineering
--strict`. A separate Claude Code runtime attempt stopped at account authentication and reported
zero input and output tokens. Claude Code runtime behavior remains unverified.
[Claude Code CLI reference](https://code.claude.com/docs/en/cli-reference)

Cases 4, 7, 8, and 9 provide equivalent inputs and assertions for a future Claude Code runtime
comparison using the skill under `.claude/skills/`.
[Claude Code skills](https://code.claude.com/docs/en/skills#where-skills-live)
