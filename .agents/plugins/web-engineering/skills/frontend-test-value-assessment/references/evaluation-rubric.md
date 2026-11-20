# Evaluation Rubric

Use the [skill workflow](../SKILL.md) for placement and status decisions. Use this rubric to record
why an existing or proposed check protects the behavior and to format the report.

## Evidence for Placement

| Question | Evidence to record |
| - | - |
| What behavior is worth protecting? | The end user, assistive technology, or developer caller. Their public operation or input, expected observable result, and a concrete regression. |
| Can the check detect that regression? | The assertion or static diagnostic that would fail, the relevant production path, and where the failure would be visible. Explain any way the check could pass with the regression present. |
| What must run for the result to be meaningful? | The execution environment, relevant runtime capabilities, and real and substituted dependencies. A critical journey needs non-unit coverage through the seam where it can fail. |
| Which plausible setup fits best? | Whether each relevant candidate can detect the regression. Among candidates with comparable detection, explain the differences in stability, maintenance, and execution cost that affect the recommendation. |
| How is the check classified? | `STATIC` for a static check, or `UNIT`, `INTEGRATION`, or `E2E` by asserted scope for an executable check. Record its runtime and test doubles separately. Give dynamic size under the project's evidenced resource policy, or record it as unknown. |

Two checks on the same public contract can cover different regressions. A type check of an internal
union and a runtime check of an untrusted payload each need evidence for the defect they can detect.
A browser integration test with a stubbed API can detect layout or navigation failures within the
tested scope. A journey that must survive a real sign-in redirect needs coverage across that
redirect and the return path. State the tested system boundary when reporting E2E.

## Check Quality

Record the applicable dimensions and the specific strength, weakness, or evidence gap in each. Use
those findings to justify the status in the skill workflow.

| Dimension | Evidence to look for |
| - | - |
| Observable behavior and refactor resilience | The check accesses a public surface and fails when the promised result changes. It survives internal changes that preserve that result. For a hook or component, identify the documented return value, callback payload, or user-facing result that a caller relies on. |
| Accessibility | The assertion matches the promised role, name, keyboard interaction, focus behavior, or announcement semantics. A claim about what a specific assistive technology announces requires evidence from the relevant setup. |
| Boundary and visual fidelity | The test exercises the actual contract when compatibility is at issue. A visual assertion detects the specific presentation regression under review. A test double preserves every property the check relies on. |
| Stability and cost | Evidence from runs or setup explains intermittent outcomes, isolation problems, execution time, or unnecessary duplication. Mark missing measurements as unknown. |
| Story setup and behavior | Record the public scenario and whether the story supplies the required setup. Cite the story export and relevant configuration, describe the proposed scenario for a new story, or name the runtime condition or collaborator that requires separate setup. Inspect the assertions in the paired spec or `play` function. |

Use surviving meaningful mutants and known flaky failures as additional evidence of weak detection
or unreliable results. Identify the particular assertion or setup that needs work. Treat missing
mutation data as an evidence gap only when it affects a specific claim.

## Coverage During Changes

Keep the check that covers a current regression until its replacement is in place and shown to
protect that risk. For `REMOVE`, cite why the contract was retired, why the check covers only
implementation details, or where equivalent coverage already exists. Broader coverage counts as
equivalent when it can fail for the same regression. A retired contract can be removed on evidence
of retirement alone. If its absence is now a required behavior, assess that requirement separately.

Mark a recommendation provisional when it relies on an assumption and state what would resolve it.
List a test as unassessed when there is too little evidence to support any status. Put both findings
in the report so a reviewer can tell which recommendations are actionable.

## Report Template

Include all required headings in order. Include **Suite Distribution** when the user requests a
distribution assessment or the review covers an entire suite. When a required section has no
applicable findings, say so briefly under that heading.

Under **Findings by Test**, use one top-level bullet per assessed test, including a review of one
test. Start each bullet with its test path and one allowed status on the same line, then record the
current and proposed setup beneath it.

```markdown
## Decision Summary

- <test set and most important coverage decision in prose>

## Test Placement

- <actor, public operation or input, observable result, and concrete regression>
- <setup and oracle needed to detect it, with the reason for choosing that setup>

## Findings by Test

- `<test path>` — `<one status from the skill workflow>`
  - Current setup — <STATIC, UNIT, INTEGRATION, E2E, or UNKNOWN, plus runtime, doubles, and
    applicable size>
  - Proposed setup — <STATIC, UNIT, INTEGRATION, E2E, NONE, or UNKNOWN, plus relevant changes>
  - <specific quality finding and production and test evidence>
  - <story path and export if reused, evidence gaps if material>

## Recommended Moves

- <change to the current check, with the protection required before replacing or removing it>

## Higher-Value Scenarios to Add

- <uncovered regression, executable or static check, and expected failing condition>

## Suite Distribution

- <what reviewing the suite as a whole reveals about gaps or duplicate coverage>

## Residual Risk

- <remaining risks, unassessed tests, and unresolved assumptions or flakiness>

## References

- <official documentation and source-code permalink for each framework-bound claim>
```
