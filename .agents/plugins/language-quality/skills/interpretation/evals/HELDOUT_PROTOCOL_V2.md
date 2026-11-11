# Prospective held-out protocol for interpretation

Use this protocol only with a fresh fixture that declares `predeclared_decision_slots` for each
case. The historical [first protocol](HELDOUT_PROTOCOL.md), [first rubric](RUBRIC.md), and their
results remain unchanged. Freeze this protocol, [the V2 rubric](RUBRIC_V2.md), fixture and gold,
runner, baseline Skill, and candidate Skill before the first model call. Record their SHA-256
hashes, CLI version, model, reasoning effort, case IDs, and three repeats. Use the same settings in
every arm.

## Two-stage observation and grade freeze

1. Run `run_plan_gap_eval.py --protocol-v2 --arms raw` for all cases and three repeats. This stage
   calls only the raw listener. Its `blind/` packets contain source, evaluator gold, the predeclared
   slots, and raw `L0` output, with no interpretation arms or cost records.
2. Give the raw-only packets and `l0-grade-template.json` to graders without Skill snapshots or
   candidate plans. Before opening any interpreted output, grade all five `L0` slots and the next
   action, and write evidence for each case/repeat. The decision-relevant slots are fixed by the
   fixture; material `L0` gaps are precisely those predeclared slots graded `unknown` or
   `incorrect`. Save the completed grade file and record its SHA-256 in the pre-comparison freeze
   record. Do not revise a grade after interpreted outputs are opened. If a fixture defect becomes
   apparent, record `fixture_issue` and exclude affected comparisons symmetrically.
3. Run `run_plan_gap_eval.py --protocol-v2 --arms raw previous candidate` with `--initial-raw-run`
   pointing to the raw-only output, `--l0-grades` pointing to the completed grade file, and
   `--expected-l0-grades-sha256` set to the pre-recorded hash. Pass explicit `--previous-skill` and
   `--candidate-skill` snapshots with different SHA-256 hashes. The runner checks the grade hash,
   Skill difference, raw-run manifest, settings, fixture and runner hashes, all raw-result hashes,
   and complete grade coverage before creating comparison output or calling an interpreter. It
   copies rather than regenerates `L0`, records the expected and actual grade hashes, and preserves
   the exact grade bytes with the comparison. The runner checks equality; the external freeze record
   establishes when the expected hash was fixed.

The runner's existing CLI without `--protocol-v2` remains the historical workflow. Keep model
prompts limited to the speaker context, visible listener role and next decision, and the natural
`L0` reply. `gold`, `test_focus`, `predeclared_decision_slots`, the listener's private brief and
prior belief, and frozen grades are evaluator-only. Before unblinding, audit model prompts for that
boundary and verify no unexpected tool calls or failed model calls. V2 output directories have
owner-only access; the blind arm mapping and seed files have owner-only read/write permissions.

## Outcomes

- **Primary: `L1`-time closure.** Compare the listener state after the first interpretation within
  each case/repeat. Include only pairs with at least one frozen material `L0` gap. Closure requires
  all those gaps correct, a valid next action, no new material slot error, required questions still
  open, and no source-fidelity hard failure in the first interpreter message. A later follow-up
  cannot change this earlier observation. Count candidate-only closures as wins and baseline-only
  closures as losses; report ties and the eligible denominator.
- **End-to-end safety.** Separately grade the first message, the natural `L1` reply, the
  interpreter's follow-up or stop, and `L2` if present. Any source-fidelity hard failure in either
  interpreter turn makes the overall exchange unsafe, even if `L1` was correct. Report full `L2`
  closure and successful targeted repairs separately. Compare follow-up choices against each arm's
  own observable opportunity: a gap already closed at `L1` needs no repair.
- **No-gap preservation.** For pairs with no frozen material `L0` gap, assess whether `L1` preserves
  the decision-relevant correct slots and valid action, keeps required questions open, and adds no
  material error. Report these pairs outside the primary denominator.
- **Supported indirect requests.** In designated cases, check whether the relay and `L1` preserve
  source-supported addressee, action, scope, and deadline. A supported indirect request is a
  request; a listener's role alone supplies none.
- **Same-speaker counterfactual.** In designated matched cases, source facts stay fixed while the
  listener's prior understanding changes. Wording may adapt, but every asserted speaker goal,
  condition, request, and decision must retain its source-supported meaning in both relays.
- **Cost.** After grades freeze, report interpreter output tokens, delivered turns, and elapsed time
  per case and arm. Sum initial and follow-up interpreter calls per pair. Report medians, ranges,
  paired candidate-to-baseline median ratios, and missing usage.

## Blinding and decision

Give graders only the anonymous full packets after `L0` grades are frozen. Keep Skill identities,
arm mapping, run manifests, prompts, and cost records with the operator. Record decisive transcript
evidence and settle disputes while blind. Do not change the frozen denominator, rubric, endpoints,
or thresholds after seeing comparison output. Report exclusions, planned and analyzable counts, and
the frozen `L0` grade file hash. A necessary protocol revision requires another fresh fixture.

- **Rejected** if the candidate has a primary loss, a candidate-only source-fidelity hard failure in
  either interpreter turn, or a confirmed baseline pass and candidate failure on a paired safeguard
  above. An inappropriate follow-up is a safeguard failure when the baseline's choice was
  appropriate under its own observable reply.
- **Accepted for this harness** only if the candidate avoids every rejection condition and every
  source-fidelity hard failure, wins in at least two distinct cases and at least two repeat indices,
  and all planned safeguards are assessable. A paired median ratio above 1.25 for interpreter output
  tokens or 1.50 for interpreter time, or missing cost measurements, makes the result provisional.
  Unnecessary delivered replies count as follow-up errors.
- **Provisional** otherwise, including ties, isolated wins, incomplete runs, or insufficient
  safeguard coverage. Report which condition remains open.

These are conservative review gates for constructed cases, repeated on one model. They measure
observable model-listener transcripts, not one person's latent understanding or the effect on human
decisions. Human grounding and transfer to other models or clients remain unmeasured.
