# Plan-Gap Evaluation Rubric

Freeze this rubric before opening any run output or arm mapping. The unit of grading is one case,
repeat, and anonymous arm label. Use the case's `speaker` facts and `gold` as the source standard;
use `listener` facts only for the listener's role, prior state, and next decision. If a gold item
conflicts with the supplied source or admits two reasonable readings, mark the item `fixture_issue`,
record the reason, and exclude it from comparisons rather than forcing a preferred answer.

## Listener state at L0, L1, and L2

Grade the same five slots in `listener_after_first` for the raw utterance (`L0`) and for each
interpretation (`L1`). Grade `listener_after_followup` only when a follow-up message exists (`L2`):

| Slot                 | What must be understood                                                                    |
| -------------------- | ------------------------------------------------------------------------------------------ |
| `goal`               | The speaker's supported purpose, attributed to that speaker.                               |
| `means`              | What the speaker proposes or uses toward that purpose, and how it serves the goal.         |
| `condition`          | The scope, prerequisite, or time condition attached to the relevant action.                |
| `requested_response` | What, if anything, the speaker asks this listener to do or answer, including its deadline. |
| `decision_status`    | What is proposed, decided, implemented, or still unresolved.                               |

For each slot assign `correct`, `unknown`, or `incorrect` against the source and gold. `Correct`
requires a materially complete, source-supported reading; paraphrases count. For `means`, a list of
the goal and means without their relationship is `unknown` for the relationship. `Unknown` covers
omission, vagueness, or an explicit admission of uncertainty without a false claim. `Incorrect`
covers a contradiction, an unsupported positive claim, or a wrong speaker, scope, modality, or
deadline. Read the structured slot together with `reply` and `uncertainties`: a natural reply that
contradicts a correct-looking structured slot makes that slot `incorrect`; an uncertainty about a
genuinely open question does not make an otherwise correct slot wrong. Quote the decisive text for
each `incorrect` or disputed grade. Do not infer understanding from the scripted `prior_belief`
alone.

Grade `next_action` separately as `valid`, `unknown`, or `invalid`, using both that field and the
natural reply. `Valid` means the listener can take the stated action from the speaker's request and
their own role, while leaving any unsupported decision open. It may include a safe partial step or a
question held for later; it need not repeat the gold wording. `Unknown` means the action is absent
or too vague to assess. `Invalid` means it assumes an unapproved action, an invented instruction, or
an answer to an unresolved question. Record whether the listener explicitly preserves each material
`gold.open_questions` item as `open`, `resolved_by_source`, or `invented_resolution`. With no
speaker answer in the transcript, an unavailable speaker's question may be queued for later and must
not be treated as answered.

## Fidelity and follow-up

Inspect each interpreter `first_message` and any `followup.message` against the speaker's supplied
context and utterance. Record a hard failure if either asserts an invented speaker goal, invents a
request to the listener, attributes another party's goal to the speaker, or turns a proposal or
condition into a final decision. Also record listener-side unsupported claims in the relevant slot
and action grades; do not automatically attribute a listener error to the interpreter. A hard
failure prevents an overall pass even if the simulated listener later states the gold answer.

Judge `followup.status` from the **natural L1 `reply` available to the interpreter**, not from
private structured slots. `stop` is appropriate when that reply shows enough understanding for the
current decision, including informed disagreement. `reply` is appropriate when the natural reply
reveals a material misunderstanding or unresolved point that the interpreter can address. Grade the
choice `appropriate`, `inappropriate`, or `not_observable` when the natural reply gives too little
evidence. A repair is successful only if it targets the revealed mismatch without inventing a
speaker answer, and the relevant L2 slot or action improves to `correct` or `valid`. If the arm
stops, leave L2 as `not_applicable`. Disagreement with a correctly understood proposal is not a
knowledge gap and does not require persuasion or repair.

## Gap closure and comparison

Before grading L1, identify the material slots that are `unknown` or `incorrect` at the shared L0
and affect the listener's stated next decision. If there are none, label the case/repeat
`no_observed_gap`: report preservation or new errors, never gap closure. For each material L0 gap,
record whether L1 and, if present, L2 change it to `correct`. Mark overall closure at a stage only
when **all** material L0 gaps are correct, `next_action` is valid, no new material slot is
incorrect, required open questions remain open, and the interpreter has no hard failure. A correct
slot already present at L0 is preservation, not a gain. Keep L1 closure and post-repair L2 closure
separate.

Grade every anonymous label in a packet and record evidence before consulting the separate arm
mapping. Record the L0 gap status once per case/repeat, then each label's five slot grades, action,
open questions, hard failures, follow-up choice, L1 closure, and L2 closure. Resolve fixture issues
without using arm identity. Only after all grades are frozen, unblind and compare arms within the
same case/repeat; report counts by case and stage alongside output tokens, turns, and elapsed time.
These are constructed, model-simulated listener transcripts. They support conclusions about this
harness's observed outputs, not about a single human's latent understanding or real-world effects.
