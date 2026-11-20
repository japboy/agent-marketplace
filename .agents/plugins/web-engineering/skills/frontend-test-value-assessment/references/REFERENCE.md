# Reference

Use this reference for terminology, placement examples, and evidence. The [skill](../SKILL.md)
contains the review workflow.

## Test Terminology Map

Use the [test terminology map](../assets/test-term-map.svg) to agree on what test labels mean in the
review. Read across from a concrete test example. Aligned bands show plausible uses, and hatching
marks where a different setup or source can change the classification. Follow the skill and rubric
for recommendations.

- **Scope** describes what the assertions validate. State which parts are under test, which
  dependencies are real or substituted, and where an end-to-end path starts and ends.
- **Size** depends on the resources the test is allowed to use. Apply the project's policy. Under
  Google's model, a browser and a real API can run in a Medium configuration if all network calls
  stay on `localhost`.
- **Names and techniques** may describe what a test checks, how it is designed, or its scope.
  ISO/IEC/IEEE 29119-1:2022 §3.130 lists *functional testing* as an example of a test type and
  explains that a type can apply at one or several test levels. The ISTQB Foundation Level syllabus
  describes functional testing as evaluating the functions a component or system should perform.
  Google's book lists *functional test* as one label for wide-scope tests. For a *scenario test*,
  state the starting conditions, actions, expected outcome, and scope.
- **Pyramid and Trophy** describe suite-level emphasis. The pyramid percentages in the figure are
  Google's example by test case count. The Trophy illustrates where Dodds suggests focusing effort.
  Review the resulting mix for gaps and duplication after choosing coverage for individual
  behaviors.

### Sources for the Map

- [Software Engineering at Google, Chapter 11](https://abseil.io/resources/swe-book/html/ch11.html)
- [The Testing Trophy and Testing Classifications](https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications)
  and
  [Static vs Unit vs Integration vs E2E Testing](https://kentcdodds.com/blog/static-vs-unit-vs-integration-vs-e2e-tests)
- [ISO/IEC/IEEE 29119-1:2022 §3.130, Test type](https://www.iso.org/obp/ui/#iso:std:iso-iec-ieee:29119:-1:ed-2:v1:en:term:3.130)
  and
  [ISTQB Foundation Level Syllabus v4.0.1, §2.2.2](https://istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf#page=29)
- [An Introduction to Scenario Testing](https://kaner.com/pdfs/ScenarioIntroVer4.pdf)
- [Playwright component testing](https://playwright.dev/docs/test-components),
  [API mocking](https://playwright.dev/docs/mock), and
  [mock response implementation](https://github.com/microsoft/playwright/blob/ce480a952553175eae75342aad2c5e86cdf2cbba/packages/playwright-core/src/client/network.ts#L350-L374)
- [Vitest Browser Mode](https://vitest.dev/guide/browser/),
  [Storybook interaction tests](https://storybook.js.org/docs/writing-tests/interaction-testing),
  and [Testing Library](https://testing-library.com/docs/dom-testing-library/intro/)
- [Go command documentation](https://pkg.go.dev/cmd/go),
  [gomock](https://pkg.go.dev/go.uber.org/mock/gomock), and
  [Testcontainers for Go](https://golang.testcontainers.org/modules/postgres/)
- [cargo test](https://doc.rust-lang.org/cargo/commands/cargo-test.html)
  ([source](https://github.com/rust-lang/cargo/blob/9ae79c984e55ee94ed9642ea101abd3f16f82916/src/bin/cargo/commands/test.rs#L4-L12)),
  [Clippy](https://doc.rust-lang.org/clippy/usage.html)
  ([source](https://github.com/rust-lang/rust-clippy/blob/ddecc8599b65b25351726777db63c727903c9ba8/src/main.rs#L179-L187)),
  [Mockall](https://docs.rs/mockall/latest/mockall/)
  ([source](https://github.com/asomers/mockall/blob/a47295fb08a178e1f5c570c38c8b40cd663a2750/mockall_derive/src/lib.rs#L1376-L1392)),
  and [Testcontainers for Rust](https://rust.testcontainers.org/quickstart/community_modules/)

## Evidence Protocol

| Claim | Evidence to cite |
| - | - |
| Protected behavior | Actor, public operation or input, expected observable result, and concrete regression. Cite the production symbol or contract and the test assertion. |
| Test placement | Current and proposed scope, runtime, and collaborators. Explain how the setup exposes the failure and how the assertion detects it. Cite test or runner configuration and the real or substituted dependency. Include size when the applicable resource policy and configuration establish it. |
| Accessibility | Expected role, name, focus, keyboard response, or live-region update. Cite the locator or assertion and the runtime or assistive technology needed to observe it. |
| Visual behavior | Expected visual outcome, relevant viewport or environment, and the screenshot, comparison baseline, or diff. |
| Boundary contract | Source of the request, response, event, callback, storage, or API contract and the assertion that observes its effect. |
| Stability or mutation | Failing run, retry history, or nondeterministic dependency. For mutation evidence, cite the report and explain which survival exposes a missed regression. |
| Framework behavior | Official documentation and a code permalink pinned to the implementation's repository path, commit, and line range. |
| Story reuse | Story file and export, scenario setup, project annotations, and the test's behavior assertion, whether in a spec or the story's `play` function. |

## Test Placement Examples

- A type checker can reject an invalid call to a typed public API. For an external response that can
  carry an invalid value, the check needs to exercise the runtime boundary that receives it and
  assert the observable rejection or fallback.
- A component's documented callback payload is part of its caller-facing contract. A focused unit
  test can invoke the public interaction and assert the payload received by the caller. Calls to a
  private helper are implementation evidence.
- A DOM test that checks a live region's role and changed text provides evidence of the exposed
  semantics. Evidence of actual speech comes from the relevant browser and assistive technology.
  [MDN ARIA live regions](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Guides/Live_regions)
- A real browser can host an integration test that stubs API traffic and verifies UI behavior across
  components. An end-to-end test for a login redirect that loses a cart exercises the real
  authentication and persistence dependencies that can lose it and checks the cart on return.
- A screenshot or layout assertion can protect a verified visual risk, such as a clipped control at
  a given viewport. Its scope depends on the UI under test and its runtime depends on what can
  reproduce that layout.

## Storybook Evidence

A story can provide a canonical use case or visible state through its args, decorators, globals, or
loaders. Record the starting state and collaborators that the story supplies and the observable
behavior the test checks. For a proposed story, describe the public scenario it would make
reproducible in Storybook and in the test.

For portable stories, look for reuse through `composeStory` or `composeStories` with the applicable
project annotations, such as those applied via `setProjectAnnotations`. Check that the test executes
the setup or `play` steps its assertion depends on. When a spec recreates the same props,
decorators, or providers, cite the duplicated setup. If the test needs a separate setup, cite the
runtime condition or collaborator that matters to the regression. For example, a story with an
in-memory navigation provider may capture a component state while a regression in native browser
history requires the application's actual router shell.

A paired story and spec can keep scenario setup synchronized. A story's `play` function can itself
supply behavior evidence when it runs under test and asserts the expected result. The assertions and
the collaborators they exercise establish the test's scope.

## Supporting Sources

### Observable Behavior

- [Software Engineering at Google, Chapter 12, Test via Public APIs](https://abseil.io/resources/swe-book/html/ch12.html#test-via-public-apis)
- [Testing Library introduction](https://testing-library.com/docs/dom-testing-library/intro/)
- [Testing Library query priority](https://testing-library.com/docs/queries/about/#priority)

### Scope, Runtime, and Fidelity

- [Cypress testing types](https://docs.cypress.io/app/core-concepts/testing-types)
- [Playwright browsers and projects](https://playwright.dev/docs/browsers)
- [Playwright locators](https://playwright.dev/docs/locators)
- [Software Engineering at Google, Chapter 13, Test Doubles](https://abseil.io/resources/swe-book/html/ch13.html)
- [Google Testing Blog, Increase Test Fidelity by Avoiding Mocks](https://testing.googleblog.com/2024/02/increase-test-fidelity-by-avoiding-mocks.html)

### Storybook Stories and Portable Stories

- [Storybook AI best practices](https://storybook.js.org/docs/ai/best-practices)
- [Storybook writing stories](https://storybook.js.org/docs/writing-stories)
- [Storybook writing tests](https://storybook.js.org/docs/writing-tests)
- [Storybook stories in unit tests](https://storybook.js.org/docs/writing-tests/integrations/stories-in-unit-tests)
- [Storybook portable stories in Jest](https://storybook.js.org/docs/api/portable-stories/portable-stories-jest)
- [Storybook portable stories in Vitest](https://storybook.js.org/docs/api/portable-stories/portable-stories-vitest)
- [Storybook React portable stories source](https://github.com/storybookjs/storybook/blob/370524faae96a30d27e36efcaa2fc39cd65fab29/code/renderers/react/src/portable-stories.tsx#L46-L159)
- [Storybook core portable stories source](https://github.com/storybookjs/storybook/blob/370524faae96a30d27e36efcaa2fc39cd65fab29/code/core/src/preview-api/modules/store/csf/portable-stories.ts#L73-L233)

### Other Evidence

- Accessibility semantics.
  [W3C Accessible Name and Description Computation](https://www.w3.org/TR/accname-1.1/)
- Boundary contracts.
  [Martin Fowler, Consumer-Driven Contracts](https://martinfowler.com/articles/consumerDrivenContracts.html)
  and [Pact docs](https://docs.pact.io/)
- Visual regression. [Playwright screenshot assertions](https://playwright.dev/docs/test-snapshots)
- Mutation testing. [StrykerJS docs](https://stryker-mutator.io/docs/stryker-js/introduction/)
- Flaky tests.
  [Martin Fowler, Eradicating Non-Determinism in Tests](https://martinfowler.com/articles/nonDeterminism.html)
