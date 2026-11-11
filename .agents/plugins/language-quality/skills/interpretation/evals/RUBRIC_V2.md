# Plan-Gap Evaluation Rubric V2

Freeze this rubric before any raw or interpreted model output. The source standard is the fixture's
`speaker` facts and `gold`; the listener's private fields establish only role, prior state, and next
decision. Every case predeclares a nonempty subset of `goal`, `means`, `condition`,
`requested_response`, and `decision_status` as decision-relevant slots. This subset is fixed before
`L0` is observed. If a gold item conflicts with the source or admits two reasonable readings, mark
`fixture_issue` with evidence and exclude affected pairs symmetrically.

## Raw `L0` grade, before either interpretation

Grade each of the five slots `correct`, `unknown`, or `incorrect` from the raw listener's structured
response, natural reply, and uncertainties. `Correct` requires a materially complete,
source-supported reading; paraphrases count. For `means`, naming goal and means without their
relationship is `unknown`. `Unknown` covers omission, vagueness, or honest uncertainty. `Incorrect`
covers contradiction, unsupported positive claims, or wrong speaker, scope, modality, or deadline.
Grade `next_action` as `valid`, `unknown`, or `invalid`. A valid action may be a safe partial step
or a question kept for later, without deciding an unsupported point. Record evidence for the grade;
quote decisive wording for every incorrect or disputed slot.

Complete the runner's `l0-grade-template.json` with all five slot grades, next action, and a
nonempty evidence summary for every pair. Preserve case ID, repeat, raw-result SHA-256, fixture
SHA-256, raw-run manifest SHA-256, and predeclared slots exactly. Freeze the completed file and
record its SHA-256 before any comparison run; pass that value as `--expected-l0-grades-sha256`.
Material `L0` gaps are computed only from predeclared slots whose frozen grade is `unknown` or
`incorrect`. Do not infer understanding from the scripted prior belief.

## Interpreted listener state and fidelity

Grade the same five slots and next action at `L1`, and at `L2` only if a follow-up was delivered.
Read structured fields together with the natural reply and uncertainties; a reply that contradicts a
correct-looking field makes the field `incorrect`. Record each material open question as `open`,
`resolved_by_source`, or `invented_resolution`. With no speaker answer, a queued question stays
open. Disagreement with a correctly understood proposal is understanding, not an error or a repair
target.

Inspect the interpreter's first message and any follow-up separately against the source. A
source-fidelity hard failure is an unsupported positive assertion that the speaker has a goal,
request, instruction, permission, delegated decision, or resolution of an open decision. It also
includes attribution of another party's goal to the speaker, a proposal/condition turned into a
final decision, or a directive that grants the listener permission or decision authority over an
open point the source does not grant. Apply this rule in **any section**, including a separately
labeled clarification, regardless of whether the directive is explicitly attributed to the speaker.
A clearly identified interpreter suggestion to ask the person who can resolve an open point is not a
speaker instruction or permission; assess its action validity separately. Record the exact assertion
and why the source does not support it. A listener-only mistake belongs in the listener slot/action
grade unless the interpreter supplied the unsupported claim.

`L1`-time closure requires every frozen material `L0` gap to become correct, a valid next action, no
new material slot error, required open questions preserved, and no hard failure in the **first**
interpreter message. A hard failure in a later follow-up cannot retroactively change `L1`; it does
make the exchange unsafe under the separate end-to-end outcome. For `no_observed_gap` pairs, grade
preservation of already correct decision-relevant slots and valid action, not closure.

Grade follow-up `stop` or `reply` using only the natural `L1` reply the interpreter saw. `Stop` is
appropriate when it shows enough understanding for the current decision, including informed
disagreement. `Reply` is appropriate only when that reply reveals a material misunderstanding or
unresolved point the interpreter can address. Mark `not_observable` if it gives too little evidence.
A successful repair targets that revealed point without inventing a speaker answer and improves its
`L2` slot or action. Report `L2` closure separately; stopped arms have no `L2`.

## Blind comparison

Use the frozen `L0` grade and predeclared slots in each anonymous full packet as the denominator.
Grade every label, record evidence, and resolve disputes before opening the arm mapping or costs.
Report `L1` wins, losses, both kinds of ties, no-gap preservation, hard-failure turns and arms,
indirect-request and matched-speaker safeguards, follow-up opportunities, repairs, `L2` closure, and
cost. These model-simulated transcripts support only conclusions about this harness.
