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
- [HELDOUT_PROTOCOL.md](HELDOUT_PROTOCOL.md) fixes the repeated comparison and review gates before
  output inspection. Select either held-out fixture with `--cases`.
- [wording-candidate-rejected.md](wording-candidate-rejected.md) and
  [structural-candidate-rejected.md](structural-candidate-rejected.md) preserve the exact rejected
  candidate inputs as evaluation data. A package can carry these files alongside the Skill. The
  parent directory's `SKILL.md` is the runtime entry. The runner uses a snapshot when selected
  explicitly with `--candidate-skill`.
- [run_plan_gap_eval.py](run_plan_gap_eval.py) runs the scenarios with fresh model contexts and
  saves prompts, responses, tool events, timing, and blinded grading packets outside the repository.
  It rejects output paths inside the source Git worktree so each model call starts outside the
  repository. The manifest records the runner SHA-256 and actual Codex CLI version. The blind seed
  is stored separately in `blind-seed.private.json` with restricted file permissions, never in the
  manifest or grading packets. The runner does not make a grading decision.
- [RUBRIC.md](RUBRIC.md) defines the pre-outcome, per-arm grading rules for listener state, source
  fidelity, gap closure, follow-up, and blinded comparison.
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
