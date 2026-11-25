---
name: frontend-test-value-assessment
description: >
  Assess frontend tests by the regressions they prevent and where those regressions can be detected.
  Use for frontend test strategy, static checks, unit, integration, and end-to-end test placement,
  mock-heavy suites, browser or device behavior, accessibility, visual regression, existing
  mutation reports, and flaky tests.
---

# Frontend Test Value Assessment

Assess each test against a concrete regression in an observable contract. Use the Testing Trophy
when reviewing a suite's distribution after placing individual checks.

## Scope

- Review frontend static checks and runtime tests, including components, hooks, browser behavior,
  accessibility, visual presentation, and boundaries that affect frontend behavior.
- Include Storybook scenarios when they supply setup or executable behavior checks.
- Include backend, load, or performance checks when they address a specific frontend regression.

When test labels vary across teams, use the
[terminology map and reading guide](references/REFERENCE.md#test-terminology-map) to agree on their
meanings before assessing tests.

## 1. Establish the Contract and Risk

For each test or coverage gap, identify:

- **Consumer and entry point.** Identify the end user, assistive technology, or developer calling
  the code, and the supported action or public input they use.
- **Expected result.** State what that consumer can observe and rely on. Examples include focus,
  accessible names, visual layout, persisted data, a return value, or a documented callback.
- **Regression.** Name the change in behavior the check should catch and why it matters. Use code,
  requirements, existing tests, or a known defect as evidence. Record material unknowns.
- **Existing coverage.** Identify which checks would fail for that regression and what additional
  confidence the test under review contributes.

A check should fail when its contract breaks and pass after a refactor that preserves the contract.
Internal state, private calls, incidental DOM structure, and framework guarantees can help diagnose
a failure. A product test earns its place by protecting a contract its consumers rely on. Assess the
regression and coverage directly. Reuse counts and coverage percentages are context.

Match coverage to the current contract. Add or update checks when new or changed behavior introduces
a regression risk worth protecting. Retire tests whose contract has been removed. Where an absence
is itself a current requirement, such as hiding a privileged control from unauthorized users, treat
it as an observable contract.

## 2. Choose a Check That Detects the Regression

1. Identify the runtime, collaborators, and assertions needed to expose the failure through the
   relevant public surface. Check whether a substitute preserves the behavior that matters at that
   boundary. Exercise real collaborators where their interaction is part of the failure.
2. Compare the current check with plausible alternatives. A type check, lint rule, or other static
   check is sufficient when it catches the same defect without running the code under review.
   Untrusted runtime inputs require evidence at the runtime boundary.
3. Favor the setup with stronger evidence for the intended regression. Among checks with comparable
   detection, prefer faster feedback, reliable execution, clear failures, and lower maintenance
   cost. Keep an effective current check when a change offers no meaningful gain.

Check what each assertion actually observes. A role, accessible name, or live-region update checks
accessibility semantics. Claims about actual screen reader output require evidence from the browser
and assistive technology in question. Use visual assertions for visual failures. Assess real focus,
layout, storage, or navigation in an environment that can expose the relevant failure. For boundary
failures, assert the outcome at the request, response, event, or storage boundary involved.

For flakiness, distinguish product nondeterminism from test instability. Use evidence from failures,
reruns, or existing reports. When mutation results are available, use surviving meaningful mutants
to identify weak assertions.

### Classify the Chosen Setup

- **Static check** examines code without running the code under review. Record it separately from
  runtime scopes and sizes.
- **Unit** verifies a contract owned by one function, hook, component, or other unit through its
  public surface. A renderer and supporting dependencies can be present.
- **Integration** verifies collaboration between parts within the declared system boundary. A
  browser test with a substituted API can verify client-side integration.
- **E2E** verifies a journey from entry point to observable result through the declared system
  boundary. Exercise the actual dependencies on the path that the test promises to verify.

Classify scope from what the assertions validate. Record runtime, real and substituted dependencies,
and applicable test-size policy separately. Assign Small, Medium, or Large when the project's
resource constraints support that label. Mark unknown constraints as unknown.

### Share Component Test Setup With Storybook

For a component covered by Storybook, use the story for the public scenario as the default setup for
its component test. Start from the runtime and collaborators the test needs to detect the
regression.

- **Suitable story.** Reuse its setup. When an existing test duplicates that setup, recommend
  sharing the story with the test at the selected scope.
- **Missing scenario.** Add a focused story with the test when the public use case or initial state
  would be useful to reproduce in Storybook and its setup can expose the regression.
- **Different setup required.** Consider whether the story can be composed in the required runtime
  with the required collaborators. When a separate setup is needed, identify the concrete condition
  or dependency that the story setup cannot provide.

Use the story to define the scenario and starting state. When an external spec uses Portable
Stories, compose the story with `composeStory` or `composeStories` and apply the relevant project
annotations. Exercise the public behavior and assert its observable result in the spec or in an
executed `play` function. Cite the story path and export and, when recommending Portable Stories
APIs, cite the applicable guide and implementation from the
[Storybook sources](references/REFERENCE.md#storybook-stories-and-portable-stories).

## 3. Recommend an Action

Use [the rubric](references/evaluation-rubric.md) to document applicable evidence and quality
checks. Give each assessed test exactly one status:

| Status | When to use it |
| - | - |
| `KEEP_STATIC`, `KEEP_UNIT`, `KEEP_INTEGRATION`, `KEEP_E2E` | The current check reliably protects a relevant contract in a suitable setup. |
| `REWRITE_AT_SAME_LAYER` | Keep the scope or static check and improve the assertion, execution environment, fixtures, collaborators, or stability. |
| `MOVE_TO_STATIC`, `MOVE_TO_UNIT`, `MOVE_TO_INTEGRATION`, `MOVE_TO_E2E` | A different scope or a change between static and runtime coverage is warranted by the regression. |
| `REMOVE` | The tested contract has been retired, the assertion protects no current contract, or verified coverage makes the check redundant. |

For moves and removals, name any meaningful current regression signal that must survive the change.
Keep it until replacement coverage is in place. A retired contract needs no replacement. If an
unsupported assertion exposes a gap in a still-current contract, report the gap and recommend a
check that detects it.

When evidence supports a conditional recommendation, mark it as provisional and state what would
change it. List unassessed tests and the missing evidence in Residual Risk.

For a critical journey such as authentication, purchase, or a destructive action, require a
realistic non-unit check that exercises the material failure path and asserts its observable
outcome. Recommend E2E when detecting the regression requires exercising the journey across the
declared system boundary. Report missing or unreliable coverage as residual risk, including
unresolved flakiness.

## 4. Review the Suite's Distribution

When reviewing an entire suite or its distribution, use the Testing Trophy to look for missing
coverage, duplication, and opportunities to shift effort toward checks with better regression
signal. In particular, ask whether integration checks cover the important collaborations. Revisit
individual tests when the review reveals a concrete gap or better setup. Base placement on the
regression and the evidence for the proposed check. Treat the distribution as an outcome of those
decisions.

## Report and Evidence

Use every required heading in the [report template](references/evaluation-rubric.md#report-template)
in order. Include Suite Distribution when the user requests a distribution assessment or the review
covers an entire suite.

In Findings by Test, create one top-level bullet per assessed test, including when the report covers
a single test. Start each bullet with the test path or name and its status, each in backticks,
separated by an em dash. Put the current and proposed classifications and supporting evidence under
that bullet. Summarize recommendations in prose in Decision Summary and reserve status codes for the
test entries. Use `NONE` for a removed check's proposed classification and `UNKNOWN` where the
evidence cannot establish one.

- Cite production and test paths and the relevant assertions. Give line references when available.
- For framework-specific claims, cite the official documentation and a source permalink with the
  repository path, commit, and relevant lines. Use the
  [reference](references/REFERENCE.md#evidence-protocol) to identify supporting evidence.
- Separate observed behavior from assumptions. Mark unknowns and identify what would resolve them.
