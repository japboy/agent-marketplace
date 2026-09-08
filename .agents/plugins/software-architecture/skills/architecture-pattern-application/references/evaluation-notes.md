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
The supplied cases exercise single-pattern decisions; combined-pattern behavior remains unmeasured.
