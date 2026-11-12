# Interpretation Evaluation Architecture

This directory owns evaluation inputs and repeatable runs for the `interpretation` Skill. Runtime
instructions remain in [SKILL.md](../SKILL.md); the sources and limits of the design remain in
[REFERENCE.md](../references/REFERENCE.md).

## Files and boundaries

- [evals.json](evals.json) holds single-response regression cases. Its assertions check the
  interpretation's content and known failure modes, but do not by themselves measure a listener's
  change in understanding.
- [triggers.json](triggers.json) holds positive and adjacent-task discovery prompts.
- [plan-gap-cases.json](plan-gap-cases.json) holds role-pair scenarios for observing a listener
  before and after interpretation. The runner filters `speaker` and `listener` fields by recipient:
  `listener.brief` and `listener.prior_belief` are private to the simulated listener, while that
  listener's natural `L0` reply is shared with each interpreter arm. `gold` and `test_focus` are
  evaluator-only and must never be included in an interpreter or listener prompt.
- [plan-gap-heldout-cases.json](plan-gap-heldout-cases.json) provides a separate fixture in the same
  schema and with the same prompt boundaries. The theater pair keeps the speaker, listener role, and
  next decision fixed while varying the listener's knowledge and stance. Other cases cover a
  context-supported indirect request, an unresolved sharing condition, a clear handoff, and an
  assistant-authored answer relayed by a fresh interpreter.
- [plan-gap-heldout-2-cases.json](plan-gap-heldout-2-cases.json) provides six fresh cases for the
  structural candidate. The seed-library pair holds the speaker facts, gold answers, listener role,
  and next decision fixed while varying prior knowledge and stance. The other cases cover an
  indirect measurement request, a floor-marker decision with unresolved permission, a clear
  classroom handoff, and a request for a sample outside a working transcript.
- [plan-gap-heldout-3-cases.json](plan-gap-heldout-3-cases.json) provides six new cases for a
  further held-out comparison. A rain-venue pair holds the speaker facts, gold answers, listener
  role, and next decision fixed while varying prior knowledge and stance. The other cases cover a
  polite indirect request for a specified object, purchase decision authority, a no-gap handoff that
  withdraws and replaces an earlier instruction, and an assistant-authored answer with partial
  completion and an open question for the shared-album owner. Each case predeclares
  decision-relevant plan slots for evaluation only; the runner excludes `predeclared_decision_slots`
  from interpreter and listener prompts.
- [plan-gap-heldout-4-cases.json](plan-gap-heldout-4-cases.json) provides six cases for the V3
  temporal-label comparison. An oral-history pair holds the same speaker facts while changing the
  listener's prior understanding and stance. Other cases cover a supported indirect request,
  unresolved photo-use authority, an internal transcript handoff, and an assistant-authored backup
  choice. The photo-use case's three repeats were symmetrically excluded after blind review found
  source/gold ambiguity; the fixture remains frozen as tested.
- [HELDOUT_PROTOCOL.md](HELDOUT_PROTOCOL.md) fixes the repeated comparison and review gates before
  output inspection. [HELDOUT_PROTOCOL_V2.md](HELDOUT_PROTOCOL_V2.md) defines the prospective
  two-stage comparison: observe and freeze `L0` grades before either interpretation arm runs, then
  compare the arms against those same raw replies. [HELDOUT_PROTOCOL_V3.md](HELDOUT_PROTOCOL_V3.md)
  retains V2's grade and outcome rules while labeling the speaker utterance as earlier than the
  already-observed listener reply. Select a held-out fixture with `--cases`.
- [wording-candidate-rejected.md](wording-candidate-rejected.md),
  [structural-candidate-rejected.md](structural-candidate-rejected.md), and
  [plan-map-candidate-rejected.md](plan-map-candidate-rejected.md), and
  [source-anchor-candidate-rejected.md](source-anchor-candidate-rejected.md) preserve the exact
  rejected candidate inputs as evaluation data. The plan-map snapshot is the v8 input tested with
  the V2 protocol and third fixture; the source-anchor snapshot is the v17b input tested with V3 and
  the fourth fixture. A package can carry these files alongside the Skill. The parent directory's
  `SKILL.md` is the runtime entry. The runner uses a snapshot when selected explicitly with
  `--candidate-skill`.
- [run_plan_gap_eval.py](run_plan_gap_eval.py) runs the scenarios with fresh model contexts and
  saves prompts, responses, tool events, timing, and blinded grading packets outside the repository.
  It rejects output paths inside the source Git worktree so each model call starts outside the
  repository. The manifest records the runner SHA-256 and actual Codex CLI version. The blind seed
  is stored separately in `blind-seed.private.json` with restricted file permissions, never in the
  manifest or grading packets. The runner does not make a grading decision.
- [test_run_plan_gap_eval_v2.py](test_run_plan_gap_eval_v2.py) checks raw-result reuse,
  evaluator-only prompt boundaries, and rejection of changed raw evidence or incomplete frozen
  grades without calling a model.
- [RUBRIC.md](RUBRIC.md) defines the pre-outcome, per-arm grading rules for listener state, source
  fidelity, gap closure, follow-up, and blinded comparison. [RUBRIC_V2.md](RUBRIC_V2.md) fixes
  decision-relevant slots in the fixture, separates `L1` observation from later follow-up safety,
  and includes unsupported permission or delegation in the hard-failure definition.
- [evaluation-notes.md](../references/evaluation-notes.md) records observed results and review
  state. A fixture or runner is an evaluation instrument, not evidence that the Skill works.

## Gap and outcome model

Each case explicitly supplies a speaker's prior context and current utterance, plus a listener's
brief, prior belief, and next decision. The `gold` object separates the speaker's supported goal,
means, condition, requested response, and decision status from acceptable next actions, open
questions, and forbidden inferences. A role title never establishes a knowledge gap by itself. The
informed-dissent control keeps the same engineer-to-designer utterance as the knowledge-gap case
while changing the listener's documented prior understanding.

The runner first shows the raw utterance to a fresh simulated listener to observe one natural
initial reply (`L0`). It then shows that same reply to the `no_skill`, `previous`, and `candidate`
interpreter arms, along with the speaker's supported context and the listener's visible task. Each
arm's interpretation enters a fresh listener call with the raw utterance and `L0` reply as shared
history. That call records comprehension, a next action, and a natural reply (`L1`). The interpreter
receives only the natural reply, then either repairs a material mismatch or stops. A response after
a repair is `L2`, produced by another fresh listener call from the transcript. The runner reports
simulated, transcript-based change; it does not track a single human's latent understanding. It
keeps arms isolated and saves anonymous grading packets. The listener's structured fields ask for
the speaker's purpose, proposed means, conditions, request, and decision status; `next_action`
records the listener's own action.

The opt-in `--prompt-version v3-temporal` uses the same data flow but names the source utterance as
the original remark before `L0`, and labels `L0` and `L1` as later listener turns. The default
`legacy` setting preserves the V1/V2 prompt text and manifest shape. A V3 raw run cannot be reused
with a legacy comparison, or vice versa. The temporal labels can also be used in historical mode for
development replays, but that path is not a formal V3 evaluation.

For the V2 path, the runner first uses `--protocol-v2 --arms raw` to produce raw-only packets and a
grade template. The grader sees no interpretation output when freezing the `L0` slot grades. A
comparison run requires the frozen grade file and the exact raw run. It verifies the manifest,
settings, fixture and runner hashes, every raw-result hash, complete grades, and the externally
precommitted grade SHA-256 before creating comparison output or starting an interpreter call. The
full anonymous packets include the frozen grade and predeclared slots; neither enters a model
prompt. The comparison records `L1`-time closure and end-to-end follow-up safety separately. The V2
output directory is owner-only, and its arm mapping is owner-read/write only. The comparison also
requires explicit, different baseline and candidate Skill snapshots. The historical CLI path and
records remain unchanged.

Grade whether the listener understands the supported goal-to-means link, conditions, requested
response, and decision status well enough for the next decision. Also grade whether the next action
is supported, a material misunderstanding is repaired, and an unresolved speaker question stays open
when the speaker is unavailable. Invented requests, goals attributed to the wrong speaker, and
proposals turned into decisions are separate failure conditions. Correct disagreement is evidence of
understanding, not a failed relay. Output length, turns, and time are cost measures, not substitutes
for understanding.

These are constructed scenarios with a model as the listener. They test an operational analogy from
program plan knowledge to conversation and cannot establish improvement in real people's
understanding. Any such claim requires a separate human-listener study.
