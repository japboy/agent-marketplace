# Evaluation Notes

## 2026-09-08: Catalogue Generalization

- Review state: `provisional` for measured behavioral improvement. The implementation and structural
  validation are complete; no product-level activation or performance claim is made.
- Targets: shared Agent Skills content for Codex and Claude Code. Product manifests were validated
  with their respective validators; runtime behavior was not tested in both products.
- Baseline: the former `web-architecture-pattern-application` skill from the repository HEAD before
  this change. Its intended scope was route-state product analytics only.
- Candidate: `architecture-pattern-application`, with the existing analytics pattern and the new
  workspace layout reference. Source links distinguish documented constraints from design synthesis.
- Method: one fresh subagent manually generated responses for both versions against the seven
  prompts in `evals/evals.json` and inspected the assertions. This is a qualitative smoke
  comparison, not an isolated per-case benchmark or a measured trigger evaluation. Both versions
  were visible to the evaluator, so the comparison is not blinded.
- Result: candidate responses satisfied the assertions in all seven supplied cases. The existing
  checkout and uncertain-route cases retained their applicability and deferral behavior. Cache
  strategy and cache transport stayed outside scope. Workspace cases selected the new pattern or
  deferred when role and ownership were unknown.
- Baseline interpretation: abstention on workspace cases is expected scope behavior, not a defect.
  The original cache-strategy assertion named both catalogue entries and unfairly penalized the
  one-entry baseline; it now checks catalogue mismatch without requiring a particular entry count.
  The recorded responses satisfy that revised assertion.
- Cost: token counts and wall duration were not measured. Do not infer efficiency gains from this
  evaluation or compare the expanded catalogue's score as a quality improvement over the baseline.
- Remaining evaluation gate: repeated isolated runs, held-out trigger prompts, and token/duration
  measurements on a fixed model and harness before promoting the behavioral improvement claim to
  `accepted`.

The applicability wording was clarified after evaluation to express one state per matched pattern.
The initial seven cases exercised single-pattern decisions; mixed-state coverage was added in the
follow-up below.

## 2026-09-08: Mixed Applicability Review Follow-up

- Review evidence: [PR 10 review](https://github.com/japboy/agent-marketplace/pull/10) identified
  that request-wide stopping/output rules could suppress another pattern's applicable result. The
  correction makes stopping and output local to each matched pattern.
- Scope: applicability rules, output rules, three new evaluation cases, and this record. Individual
  design references are unchanged.
- Method: one fresh subagent generated responses for all ten prompts and checked all 36 assertions.
  This was a qualitative smoke test using the supplied cases, not isolated product invocation or a
  blinded comparison. Token counts and reliable elapsed duration were unavailable.
- Result: 10/10 cases and 36/36 assertions passed for the generated responses. The original seven
  cases retained their expected decisions and abstention behavior.
- Case 8: layout remained applicable with a single Rust package container and membership checks;
  analytics deferred pending canonical route semantics and a route registry.
- Case 9: layout deferred pending package role/ownership evidence; analytics retained a canonical
  transition model, semantic derivation, and privacy boundaries.
- Case 10: two separately named deferrals retained their own missing facts and resolving artifacts;
  neither architecture was invented and neither result was discarded.
- Validation: `mise run check` passed after the rule and case changes. The follow-up record was
  separately checked for formatting and prose compliance.
- Review state: `provisional` for quantitative behavioral improvement. This smoke test covers the
  reported mixed-state failure; automatic activation and repeated fixed-harness evaluation remain
  outside the evidence collected here.

## 2026-09-08: Route-State Analytics Intent Alignment

- Review state: `provisional` for behavioral improvement; this update corrects the expression of the
  author's stated intent, without claiming measured agent performance gains.
- Targets: shared reference content for Codex and Claude Code; activation rules are unchanged.
- Evidence: the author confirmed three corrections in the originating conversation: make reduced
  instrumentation changes the goal, separate operational maturity from implementation mechanisms,
  and motivate meaningful URL-state design through future analytics reuse.
- Scope: the analytics reference and three representative evaluation cases (11–13). Other
  participants' operational requests are not requirements for this update.
- Baseline: repository commit `8df35d2`, whose reference emphasized removing feature-owned tracking,
  ranked DWH modeling highest, and primarily described applicability to existing meaningful routes.
- Candidate: states the analysis-change success criterion, uses the author's level 0–2 operating
  model, treats projection locations as choices, and adds analytics reuse as a URL design
  motivation.
- Method: a subagent independently proposed the three evaluation prompts and expectations; the
  authoring agent inspected the candidate text against them. No fresh agent response comparison or
  product-level invocation was performed. Cases 11–13 are evaluation inputs, not reported passes.
- Cost: token counts and comparative runtime were not measured.
- Remaining evaluation gate: isolated baseline/candidate responses on a fixed model and harness,
  including existing applicability cases and held-out prompts, with quality and cost measurements.
