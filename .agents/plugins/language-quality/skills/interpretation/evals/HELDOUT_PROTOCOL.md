# Held-out protocol for the interpretation wording change

Before the first held-out model call, freeze this protocol, [the rubric](RUBRIC.md), the held-out
cases and their gold answers, and the baseline and candidate Skill snapshots. Record their hashes,
the [runner](run_plan_gap_eval.py) hash, CLI version, model, reasoning effort, and case IDs. Run
three repeats per case with the runner's `raw`, `previous`, and `candidate` arms. `previous` is the
unchanged Skill snapshot. Each case and repeat shares one raw listener observation (`L0`) across
both interpretation arms. Use the same model settings and runner prompts in both arms.

## Outcomes

- **Primary.** Compare closure at `L1` within each case and repeat. Before grading interpretations,
  identify the decision-relevant slots that are `unknown` or `incorrect` in observed raw `L0`.
  Include only pairs with at least one such gap in the primary denominator. Closure requires all
  those slots to be correct, a valid next action, no new material slot error, and preservation of
  required open questions. Any interpreter source-fidelity hard failure under the rubric, in the
  first message or follow-up, disqualifies closure. Count candidate-only closures as wins and
  baseline-only closures as losses. Report both kinds of ties and the eligible denominator.
- **No-gap preservation.** For `no_observed_gap` pairs, check that the interpretation preserves
  decision-relevant correct slots and valid actions observed at `L0`, keeps required questions open,
  and introduces no material error or invalid action. Report these pairs outside the primary
  denominator.
- **Supported indirect requests.** In the preselected indirect-request cases, check whether the
  relay and `L1` carry the source-supported addressee, action, scope, and deadline where present. A
  supported indirect request counts as a request. The listener's role alone supplies no request.
- **Same-speaker counterfactual.** In the preselected matched cases, hold the speaker's utterance
  and supporting facts fixed while varying the listener's prior understanding. Check both relays
  against those same facts. Listener-specific wording and emphasis may vary. Any asserted speaker
  goal, condition, request, or decision must retain its source-supported meaning in both relays.
- **Follow-up.** Grade reply or stop from the natural `L1` reply, including appropriate stop after
  informed disagreement. Record `not_observable` when that reply gives too little evidence. A
  successful reply addresses the revealed gap without inventing a speaker answer and makes the
  affected `L2` slot correct or action valid. Report repair opportunities, successful repairs, and
  `L2` closure separately. An arm that stops has no `L2`.
- **Cost.** After grades freeze, report interpreter output tokens, delivered turns, and elapsed time
  by case and arm from the runner records. Sum the two interpreter calls per pair for tokens and
  time, including the follow-up decision. Count the initial message and any delivered follow-up as
  turns. Report arm medians and ranges and the median candidate-to-baseline ratio across paired
  observations for each metric. Mark missing usage explicitly.

## Blinding and decision

Give the grader only anonymous packets with the source, gold answers, and transcripts. The raw
utterance identifies `L0`. Keep the two Skill identities, arm mapping, seed, run manifest, prompts,
and cost records with the run operator. Record decisive transcript evidence and resolve disputes
while blind. Apply the rubric's `fixture_issue` rule symmetrically to affected comparisons and
report all exclusions and planned versus analyzable counts. Freeze grades before unblinding. Keep
cases, rubric, endpoints, and thresholds fixed after any held-out output is seen. If they need
revision, freeze a new protocol and use fresh held-out cases for the revised comparison.

- **Rejected** if the candidate has a primary loss, a source-fidelity hard failure where the
  baseline has none, or a confirmed baseline pass and candidate failure on a paired safeguard above.
  Compare follow-up behavior against each arm's own observable opportunity. A gap closed at `L1`
  removes the need to repair it at `L2`.
- **Accepted for this harness** if the candidate avoids all rejection conditions and all
  source-fidelity hard failures, wins in at least two distinct cases and across at least two repeat
  indices, and the planned safeguard comparisons are assessable. A paired median ratio above 1.25
  for interpreter output tokens or 1.50 for interpreter time, or missing cost measurements, makes
  the result provisional. These are review thresholds for a bounded wording change. Unnecessary
  delivered replies count as follow-up errors.
- **Provisional** otherwise, including ties, isolated wins, incomplete runs, or insufficient
  coverage. Report the observed paired counts and which condition remains open.

The acceptance gate is a conservative internal rule for a small synthetic suite. Repeats share
fixtures and a model, so paired counts describe this run. Each listener observation comes from a
fresh model context with transcript history and structured elicitation of understanding. This setup
provides no human grounding and cannot establish a change in human understanding or real-world
decisions. See [the evaluation architecture](ARCHITECTURE.md).
