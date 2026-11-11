# Interpretation: Design and Evaluation

## Design basis

The research and professional-practice sources, the points they support, and the boundaries of their
application are mapped in [REFERENCE.md](REFERENCE.md). In particular, applying
program-comprehension plan knowledge to conversation and separating the speaker's goal from the
listener's requested action are choices made for this skill.

All evaluation prompts are constructed scenarios, not records of actual conversations. Case 1 adapts
the release example supplied in the request. The prior explanation about customer inquiries, the
meaning of the intake desk, and the fact that Sales is preparing a customer notice are premises of
the fixture. Whether Sales should hold the notice is deliberately missing. Cases 2–4 and all trigger
prompts are synthetic. Their provided remarks and context are the evidence for the relay; the
references above inform the workflow and do not establish facts about the scenarios.

## Output comparison

Run on 2026-11-11 with Codex CLI 0.163.0, `gpt-6.1-sol`, low reasoning effort, and fresh temporary
working directories without repository skills. Each run used `codex exec --ignore-user-config
--ignore-rules --ephemeral -s read-only --skip-git-repo-check --json`. Both arms received the
identical prompt from [evals.json](../evals/evals.json) and the same instruction to answer directly
from the supplied scenario without tools. The candidate also received the skill body as inline
instructions. The command traces contained no tool calls in these comparisons. The author reviewed
the results against the fixture assertions without blinding.

| Case                                     | Without the skill                                                                                                                                    | With the revised skill                                                                                                                                                                                    |
| ---------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1. Japanese, Development to Sales        | Connected the inquiry goal to the intake condition and preserved the proposal. Omitted what Sales needed to check before proceeding with its notice. | Preserved the proposal and added a separate question to Development: whether Sales should hold the customer notice too.                                                                                   |
| 2. English, supplier to warehouse        | Preserved the reason, conditional offer, and Friday reply deadline. In one run, “before 10 a.m.” was left to attach implicitly to Tuesday.           | Stated Tuesday before 10 a.m. as the receiving condition and kept the Friday reply deadline separate. Asked no extra question.                                                                            |
| 3. Ambiguous remark, Operations to Sales | Flagged the missing facts but instructed Sales to check existing approvals and contact a decision maker, steps absent from the remark.               | Kept the tentative view and provided specific questions for Operations about the target, release condition, and expected action. The relay still repeated some unknowns alongside the separate questions. |
| 4. Two-way relay of disagreement         | Returned the listener’s understanding, dissent, and question about Thursday.                                                                         | Returned the same three elements without inventing agreement or an answer.                                                                                                                                |

The first candidate missed the question in case 1 and left the date of the receiving condition
implicit in case 2. The revision ties clarifications to a concrete decision and keeps conditions and
deadlines attached to the action they qualify. A further wording change tried to keep notes about
uncertainty out of the relay in case 3. That run still repeated the notes, so the shorter revision
was retained.

Reported usage and elapsed time for the second paired run (baseline / retained candidate):

| Case |    Input tokens | Output tokens | Wall time (s) |
| ---- | --------------: | ------------: | ------------: |
| 1    | 16,920 / 17,383 |      60 / 132 |   6.50 / 9.32 |
| 2    | 16,872 / 17,335 |       82 / 91 |   6.39 / 7.42 |
| 3    | 14,974 / 15,437 |     199 / 186 |  10.11 / 7.44 |
| 4    | 16,919 / 17,382 |       76 / 80 |   6.40 / 5.91 |

Input totals include the CLI’s context, including cached tokens. Wall time is one observation per
arm per case; it is not a latency estimate.

## Invocation check

In separate fresh Codex CLI runs, exposed all three Language Quality skills under `.agents/skills/`
and passed only the query from [triggers.json](../evals/triggers.json). Counted a skill as invoked
when the trace showed a read of its `SKILL.md`. The candidate was read for all three relay requests
and none of the four near misses. The rewriting and terminology requests read
`japanese-naturalization` and `term-translation-research`, respectively. Literal translation and a
general explanation for Sales did not read any of the three. This check used the first candidate
body; the discovery descriptions did not change in the revision.

**Review state: provisional.** This is a small, single-model comparison on the cases used to refine
the skill. Follow up with held-out prompts, repeat the invocation check, and run behavioral checks
in Claude Code. In particular, check whether ambiguous cases keep all material unknowns and
questions outside the relay and whether one-way shares with no pending decision avoid unnecessary
clarification.

## Independent review on 2026-11-11

A separate reviewer checked the source claims against the primary texts. Hermans describes
recognizing the programmer’s goal through structure and connections. Pennington’s original
[1987 paper](https://www.cs.kent.edu/~jmaletic/cs69995-PC/papers/pennington87.pdf), pp. 307–309,
discusses plan knowledge in terms of program functions, data flow, and plans. Distinguishing a
speaker’s goal from the reply they seek is the skill’s application of this idea. Clark and Brennan’s
grounding criterion involves evidence of understanding sufficient for the participants’ current
purpose. A relevant reply can supply that evidence. The
[CEFR Companion Volume](https://rm.coe.int/common-european-framework-of-reference-for-languages-learning-teaching/16809ea0d4#page=35),
§2.5 and pp. 115–116, supports mediation within a language and adding relevant background or
clarifying questions as needed. These sources motivate the workflow and do not measure its
performance.

An evaluator who did not author the skill designed four new synthetic cases, set three checks for
each case before running them, and graded the first outputs under randomized IDs before revealing
which arm received the skill. Both arms used fresh Codex CLI 0.163.0 sessions with `gpt-6.1-sol` at
low reasoning effort, the same input, and the same instruction to use the supplied scenario. The
candidate received the current skill body inline. No case involved real participants or delivery of
a message.

| Scenario                                                                   | Without / with | Observation                                                                                                                                                                                                                             |
| -------------------------------------------------------------------------- | -------------: | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Relay an English logistics update in Japanese                              |      3/3 / 2/3 | The logistics speaker had explained the goal of unloading exhibits even if the dock equipment stopped. Both arms kept the truck booking and the request to confirm gate access by Thursday noon. The candidate omitted the stated goal. |
| Relay a tentative remark about circulating a monthly report                |      1/3 / 2/3 | Only the candidate asked the analyst what “drawing a line” meant and whether it applied to Accounting’s internal distribution. Both outputs put some missing information in the relay itself.                                           |
| Return Public Relations’ mistaken reading of a conditional production plan |      3/3 / 3/3 | Both arms returned the actual misunderstanding to Production and told Public Relations that the date remained conditional and the notice should stay as written.                                                                        |
| Relay an overnight monitoring report to a new colleague                    |      2/3 / 3/3 | Both arms explained the backup server and omitted a clarification. Only the candidate explicitly named the monitoring team as the source.                                                                                               |

In two additional pairs per scenario for the logistics and report cases, the omission of the
logistics goal recurred. Across the three runs per arm, the candidate preserved that goal once and
the baseline twice. The candidate directed the report questions to the analyst in two of three runs,
compared with zero of three for the baseline. All three candidate runs repeated some missing
information in the relay. These observations are specific to the prompts and runs.

Three additional paired probes checked attribution and the interaction before and after a listener
response. Both arms avoided attributing an executive meeting goal to the quality assurance speaker.
When Procurement had yet to answer a request to ask about morning delivery, both arms left the reply
open. The candidate also asked the warehouse for an exact time window, which was not needed for the
initial inquiry. In a case where Support mistook a pause on sending a notice for a pause on writing
it, both arms conveyed the original distinction. The candidate asked whether the already stated
division was acceptable, leaving unclear whether it was checking Support’s understanding or
reopening the instruction.

A separate discovery check exposed the three skills under `.agents/skills/`. A request to write a
message for Purchasing with the purpose and requested action, without naming interpreting, read
`intent-interpretation/SKILL.md`. A closely matched request to polish a previous answer read
`japanese-naturalization/SKILL.md`. Each was run once. The Claude Code 2.1.303 behavioral probe
could not run because the CLI reported that it was not logged in.

**Review state: provisional.** The candidate can preserve attribution and turn some ambiguity into
actionable questions. It does not reliably convey a confirmed purpose or keep missing information
out of the relay. The two-way instructions describe returning an actual reply and when to stop. They
leave the steps for checking a material misunderstanding and relaying the correction to the listener
implicit.

## Revision and lower-capability evaluation on 2026-11-11

The skill was renamed from `intent-interpretation` to `interpretation`. The revision names its
source and listener, permits relevant history or memory for audience adaptation, keeps a confirmed
goal with the means or condition it explains, places material clarification outside the relay, and
describes repair after a listener's actual response. It also supports the agent's own answer as the
source and its user as the listener. The adjacent evaluation fixture and Plugin architecture use the
new name.

The requested `gpt-6.1-luna` at medium reasoning effort was rejected by Codex CLI 0.163.0 as
unsupported with this ChatGPT account. `gpt-6-luna` at medium succeeded in a smoke run, so all
paired runs below used that available lower-capability model and fresh temporary directories. Both
arms received the exact same scenario and instruction to use only that scenario. The earlier arm
received the saved pre-revision skill body, while the candidate received the current skill body. No
paired run called a tool. These are synthetic scenarios and single observations, not estimates of
general performance.

| Scenario                                                   | Earlier body                                                                                                                     | Revised body                                                                                                                                                                                       |
| ---------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| English logistics update to a Japanese facilities listener | Preserved the reason for booking a liftgate truck, the booking, and the gate check, but added a redundant check to the listener. | Preserved the equipment-failure purpose, the truck booking, gate condition, and Thursday deadline in the relay. No extra question in the final run.                                                |
| Ambiguous monthly report remark to Accounting              | Gave the remark and described missing information, but did not direct concrete questions to the analyst.                         | Kept the analyst's remark as the relay and separately identified the missing meaning and whether the condition applies to Accounting's distribution. The analyst's unavailability stayed explicit. |
| Agent's own draft to its user                              | Reported tests, a conditional hold proposal, and requested a release decision.                                                   | Preserved the same distinction and linked the hold to customer inquiries. The user's final decision role was explicit in the fixture.                                                              |
| User mistakenly reads passing tests as release approval    | Corrected the unapproved state and restated the intake condition.                                                                | Corrected the same misunderstanding and asked whether that distinction was understood.                                                                                                             |
| User accurately describes the proposal but disagrees       | Treated the reply as understanding plus opposition.                                                                              | Also treated it as understanding plus opposition, without requesting another readback.                                                                                                             |

The saved paired runs took 5–7 seconds per arm in most cases. Input tokens were approximately
15,000–17,000 per run, including varying CLI context. The skill text grew from 419 to 683
whitespace-delimited words. Intermediate edits sometimes caused missing-information notes to appear
inside the relay or added unnecessary questions, so they were discarded. The retained candidate
passed the two targeted scenarios in another run with the same inputs.

Native discovery runs exposed the three Language Quality skills under `.agents/skills/`. The renamed
skill was read for an explicit Development-to-Sales relay and an implicit request to interpret the
agent's own progress report. A writing-polish request read `japanese-naturalization`; literal
translation read no Language Quality skill. The explicit relay run also exposed a material failure.
Although Development only proposed holding a release, `gpt-6-luna` added an unsupported request that
Sales coordinate the first-response staffing. Adding a general no-invented-request rule and a short
example did not remove this failure in subsequent single runs, so those additions were discarded.
The new regression case records this as an open check.

**Review state: provisional.** The requested changes and rename are implemented, and the targeted
paired tests improved the documented failures. The low-capability native invocation still invented a
listener action in one scenario. Claude Code behavior was not tested because the local CLI reported
that it was not logged in.

## English-wording revision and paired re-evaluation on 2026-11-12

The revision clarifies when the agent's own output can be the source, which speaker a contextual
goal belongs to, whose reply is available, and who should answer a question about a condition's
scope. It also replaces the noun *relay* with *interpretation* and makes the grounding heading
procedural. The baseline was the previous `SKILL.md` (SHA-256
`943f59008f796fad10d4b450c05ff622b6818426c3a23165526c9236d200a3fc`); the candidate was the revised
file (SHA-256 `48c663541e064c26dee3478b8b50b13cdc812ba2f77c4f4f65d7da070019870d`).

Both arms received the same wrapper, skill-body placement, and exact prompt for each case. Runs used
Codex CLI 0.163.0, `gpt-6-luna` at medium reasoning effort, fresh temporary working directories,
`codex exec --ignore-user-config --ignore-rules --ephemeral -s read-only --skip-git-repo-check
--json`, and an instruction to use only the scenario without tools. All runs exited successfully and
recorded no tool calls. The first pass used the eight existing prompts in
[evals.json](../evals/evals.json) plus two probes for goal attribution and an unavailable speaker,
defined before the candidate runs and now retained as cases 9 and 10. Each arm ran once per case. A
separate reviewer graded outputs under randomized A/B labels against the fixed assertions without
seeing the arm mapping.

| Case                                | Baseline | Candidate | Observed difference                                                                                           |
| ----------------------------------- | -------: | --------: | ------------------------------------------------------------------------------------------------------------- |
| 1. Development to Sales             |      3/3 |       2/3 | Candidate omitted a separate question to Development about the customer notice.                               |
| 2. Supplier to warehouse            |      3/4 |       3/4 | Baseline rendered “before 10” as “by 10”; candidate repeated the stated reply request as a separate question. |
| 3. Ambiguous Operations remark      |      2/3 |       2/3 | Both omitted at least one needed question to Operations.                                                      |
| 4. Sales reply to Development       |      2/3 |       3/3 | Candidate explicitly retained Sales' understanding of the conditional proposal.                               |
| 5. Agent's own draft                |      3/3 |       3/3 | Both separated test success from the proposed release hold.                                                   |
| 6. User's mistaken approval reading |      3/3 |       2/3 | Candidate's “Is this understanding correct?” did not check the condition and undecided state specifically.    |
| 7. User understands but disagrees   |      3/3 |       3/3 | Both treated disagreement as compatible with understanding.                                                   |
| 8. Unsupported Sales action         |      2/4 |       3/4 | Both invented a request for Sales to help arrange the first-response desk.                                    |
| 9. Goal from another document       |      3/3 |       3/3 | Neither attributed Sales' revenue goal to Quality Assurance.                                                  |
| 10. Analyst unavailable             |      2/3 |       3/3 | Candidate directly corrected Accounting's mistaken reading and kept the analyst question open.                |

The candidate passed 27/32 assertions versus 26/32 for the baseline; each passed every assertion in
5/10 cases. The extra question in candidate case 2 was a repeated request, not a request for new
information, so that assertion is a borderline judgment. To check the two candidate regressions,
cases 1 and 6 were each repeated twice per arm with the same prompt and fresh contexts. Across three
runs per arm, case 1 passed 8/9 baseline versus 7/9 candidate assertions; case 6 passed 7/9 in both
arms. Both versions sometimes omitted the Development question or asked only a generic understanding
check. The repeated outputs do not establish a consistent benefit for the revised wording.

In the first ten pairs, total elapsed time was 49.31 seconds baseline versus 58.94 seconds
candidate, and output tokens were 1,089 versus 1,318. The complete skill text grew from 701 to 758
whitespace-delimited words. Timing and token totals are observations from single runs, not estimates
of general cost; reported input tokens include CLI context and cache variation. The preceding
evaluation record does not preserve its five lower-model prompts verbatim, so this comparison used
the preserved fixture prompts instead. Native skill discovery and Claude Code behavior were not
rerun.

**Review state: provisional.** The revised English is clearer about the intended roles and sources,
but the paired outputs do not demonstrate a reliable behavioral improvement. The unsupported Sales
request remains an open failure on case 8. Retain the wording as a scoped clarification, with no
claim of improved reliability pending broader testing.

## Plan-knowledge gap evaluation on 2026-11-12

The new [role-pair cases](../evals/plan-gap-cases.json), [runner](../evals/run_plan_gap_eval.py),
[architecture](../evals/ARCHITECTURE.md), and pre-outcome [rubric](../evals/RUBRIC.md) measure a
specific question: after a speaker's remark, can the listener identify the speaker's purpose, the
means and condition, the actual request, and the decision state well enough to take a supported next
step? The cases cover manager to subordinate, engineer to designer, and director to engineer. An
informed-dissent control uses the same engineer remark with a listener who already understands the
proposal but has a reason to object. The case premises and gold answers are synthetic; the
application of program plan knowledge to conversation is a design analogy described in
[REFERENCE.md](REFERENCE.md).

Each case begins with one simulated listener response to the raw remark (`L0`). The `no_skill`,
`previous`, and `candidate` interpreters see the same speaker context, listener role and next
decision, and natural `L0` reply. They do not see the listener's private brief or prior belief, or
the gold answers. A fresh simulated listener receives each interpretation and the common history
(`L1`); the interpreter then sees only its natural reply and may stop or send a repair (`L2`). The
rubric grades the listener's stated plan knowledge and next action, source fidelity, open questions,
and whether an actual reply warrants repair. It does not count agreement as a requirement.

The first full run used a generic listener prompt that left `goal` ambiguous between the speaker's
purpose and the listener's own work. Its 45 calls and blind grades are retained as a measurement
pilot, not used to compare skill versions. The final runner asks every listener the same generic
speaker-purpose and goal-to-means questions, and preserves the listener's documented stance unless
the exchange addresses it. The runner also rejects output inside the source worktree, separates the
private blind seed from the manifest, and records its hash and the CLI version. The pilot runner
SHA-256 was `dcb36d5ccf4a9092397c33277f6d0f78647c6cc64069f9a202005db985b0d2cd`; the final runner
SHA-256 was `6bfcd0732321b20301f0d7a69a397095e1cafcf5dfba5728efb662768d37d49d`.

The final run used Codex CLI 0.163.0 and `gpt-6-luna` at medium reasoning effort. The previous skill
body had SHA-256 `943f59008f796fad10d4b450c05ff622b6818426c3a23165526c9236d200a3fc`; the candidate
had SHA-256 `48c663541e064c26dee3478b8b50b13cdc812ba2f77c4f4f65d7da070019870d`. All 42 calls used
fresh contexts, exited successfully, and made no tool calls. A reviewer graded all four packets
under anonymous labels before the arm mapping was opened. A separate protocol review challenged two
hard-failure flags; the blind reviewer recorded an addendum without changing the frozen original
grades. The two corrections offset, leaving eight hard-failure arms in total.

| Case                     | Observed raw `L0` gap                                                                    | `no_skill`                                                   | Previous body                                                                 | Candidate body                                                                                                                   |
| ------------------------ | ---------------------------------------------------------------------------------------- | ------------------------------------------------------------ | ----------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| Manager to subordinate   | Speaker purpose and means missing.                                                       | No closure; turns the proposed release hold into a decision. | No closure; purpose and means still missing.                                  | No closure; purpose and means still missing, and the proposed hold is stated as operative. The customer-notice scope stays open. |
| Engineer to designer     | Purpose and goal-to-means link missing; review request misread as an availability reply. | No closure; wrong review reply remains.                      | No closure; adds an availability request.                                     | No closure; adds the same request. A follow-up corrects the review request, but purpose and means remain missing.                |
| Director to engineer     | Purpose and goal-to-means link missing.                                                  | No closure; adds an instruction to start the estimate today. | Recovers purpose and means but adds an unsupported reply about starting work. | All material gaps close at `L1`; the listener estimates feasibility and effort and does not start implementation.                |
| Informed dissent control | No observed gap; the listener understands the proposal and keeps a scope concern.        | Adds new errors.                                             | Adds a new scope deliverable.                                                 | Adds a new scope deliverable. None fully preserves the already adequate understanding.                                           |

Full `L1` closure occurred in **1 of 9** interpreted outputs from the three cases with an observed
`L0` gap: candidate 1/3, previous 0/3, and no-skill 0/3. The candidate's two follow-up attempts
produced one repair of the review-request slot and no full `L2` closure. The informed-dissent case
had no gap to close and none of the three interpreters preserved it without a new material error.
Source-fidelity hard failures affected candidate 3/4 cases, previous 2/4, and no-skill 3/4. One
no-skill focus output also made a first-person role error that changed the listener's requested
response; the adjudication kept its listener-side error but did not count it as a speaker-request
hard failure.

| Arm            | Model calls | Input tokens | Output tokens | Summed call time (s) |
| -------------- | ----------: | -----------: | ------------: | -------------------: |
| Raw `L0`       |           4 |       62,452 |         1,457 |                37.55 |
| No skill       |          12 |      181,540 |         1,680 |                65.76 |
| Previous body  |          12 |      186,570 |         2,276 |                77.45 |
| Candidate body |          14 |      217,172 |         3,500 |               100.61 |

Input totals include CLI context and cached tokens; the candidate also made two extra listener
calls. The times are sums of observed calls in this run, not latency estimates.

**Review state: provisional.** The candidate closed one constructed gap, but it also introduced
unsupported requests or decision status in three of four cases and cost more tokens and calls. The
run has one repeat per case. `L1` and `L2` reconstruct a listener from a private brief and the
transcript rather than track one person's understanding. The structured questions prompt explicit
analysis, and no actual speaker answer was supplied for two-way grounding. These outputs support
only a within-harness comparison; they do not establish improvement in human understanding or
reliable skill benefit. A separate human-listener study and held-out cases would be needed for those
claims.

## First bounded wording candidate: rejected on held-out cases

The next candidate shortened the runtime text from 758 to 688 whitespace-delimited words. It moved
the speaker's purpose-to-means link toward the opening and added a source check for actor, action,
object, modality, condition, and deadline. The aim remained listener understanding for the next
decision; grounding stayed conditional. Its formatted snapshot SHA-256 was
`10cc8a374a1eb68fc6ac94e20ff005b35ee94ea3d63c4910593997930b0716e0`, compared with the unchanged
baseline `48c663541e064c26dee3478b8b50b13cdc812ba2f77c4f4f65d7da070019870d`.

The six [fresh cases](../evals/plan-gap-heldout-cases.json) and their gold answers were designed
without seeing this candidate or its outputs. [The held-out protocol](../evals/HELDOUT_PROTOCOL.md)
and [rubric](../evals/RUBRIC.md) were fixed before the complete run. The case SHA-256 was
`733b88a61a26ba8412955e1760907fade59f46263f7ee59a6fcdd8eefe548dee`; the protocol SHA-256 was
`d37e0574244046fe584dad3f2606465303a9f940cf90f11890cbaad2904b254a`. An initial attempt was stopped
during its first raw-listener call to format the candidate snapshot; it produced no listener result
and is excluded. The complete run used Codex CLI 0.163.0, `gpt-6-luna` at medium reasoning effort,
three repeats of all six cases, and `raw`, baseline, and candidate arms. All 135 fresh calls
completed with no tool use or failures. Each case/repeat shared one raw `L0` reply, and the 72
interpreter prompts were checked for direct leakage of private listener facts or gold.

Three separate graders scored one repeat each under anonymous packet-local labels. A fourth,
still-blind reviewer applied the same materiality rule across repeats and recorded corrections
without changing the original grades. Only then were labels and cost records opened. Of 18 paired
case/repeats, seven had a decision-relevant gap at `L0`; the other 11 were no-gap preservation
checks. The normalized results were:

| Measure                                      | Baseline | Candidate |
| -------------------------------------------- | -------: | --------: |
| Full `L1` closure among 7 eligible pairs     |        1 |         0 |
| `L1` preservation among 11 no-gap pairs      |        5 |         5 |
| Source-fidelity hard-failure arms among 18   |        6 |        10 |
| Median interpreter output tokens per pair    |      281 |     133.5 |
| Median interpreter elapsed time per pair (s) |   10.115 |     8.165 |

There were six candidate-only and two baseline-only hard-failure pairs. In the theater cases the
candidate repeatedly turned a listener-side work-table action into a request attributed to the
caption lead. In the recording case it turned an unresolved preference about sharing into a
staff-link stop instruction. Both violate source fidelity regardless of the score of the indirect
request case. The only primary loss was a roster pair: both `L1` listeners understood the request,
but the candidate's later message treated a placeholder name as delivered and promised to update the
table without a speaker answer. The precommitted protocol disqualifies closure after a
source-fidelity hard failure in a follow-up, so this is a protocol-level loss rather than a
difference in the two `L1` comprehension fields. The paired median candidate-to-baseline ratios were
0.731 for output tokens and 0.853 for elapsed time; the shorter candidate was cheaper but less
faithful.

**Review state: rejected.** Candidate-only hard failures independently satisfy the precommitted
rejection rule. The working-tree `SKILL.md` was restored to the frozen baseline before another
revision. The assistant-authored answer case relays earlier assistant content through a fresh
interpreter; it does not test a model interpreting an answer it actually wrote. These are synthetic
model-listener transcripts, with structured questions and no human grounding. The three graders also
required cross-repeat adjudication, so the counts are descriptive of this run, not a precise
estimate of real-world reliability.
