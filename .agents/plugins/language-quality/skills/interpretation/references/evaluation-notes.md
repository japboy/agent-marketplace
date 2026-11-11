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

The [wording candidate snapshot](../evals/wording-candidate-rejected.md) shortened the runtime text
from 758 to 688 whitespace-delimited words. It moved the speaker's purpose-to-means link toward the
opening and added a source check for actor, action, object, modality, condition, and deadline. The
aim remained listener understanding for the next decision; grounding stayed conditional. Its
formatted snapshot SHA-256 was `10cc8a374a1eb68fc6ac94e20ff005b35ee94ea3d63c4910593997930b0716e0`,
compared with the unchanged baseline
`48c663541e064c26dee3478b8b50b13cdc812ba2f77c4f4f65d7da070019870d`.

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

## Structural candidate: rejected on fresh held-out cases

The [structural candidate snapshot](../evals/structural-candidate-rejected.md) reorganized the Skill
around establishing the speaker's position, adapting to the listener, delivering the interpretation,
and repairing misunderstandings. It grouped supported speaker facts by goal and means, conditions
and status, and requested response. It used labeled sections when the listener needed a
clarification alongside the relay. The frozen candidate SHA-256 was
`39cdc7da5440cc1ef7a8bcf678bd8f87fdbcfebb1aba503163ba46a18a725b34`. The baseline SHA-256 was
`48c663541e064c26dee3478b8b50b13cdc812ba2f77c4f4f65d7da070019870d`.

The [second fixture](../evals/plan-gap-heldout-2-cases.json) used six fresh cases with the same
[protocol](../evals/HELDOUT_PROTOCOL.md) and [rubric](../evals/RUBRIC.md). Its frozen SHA-256 was
`0b718119195dca3cd0a071b9bfafc4e5bda428e1a628c281cb1d281e357db692`. Codex CLI 0.163.0 ran
`gpt-6-luna` at medium reasoning effort for three repeats of the raw, baseline, and candidate arms.
All 131 calls ran in distinct model contexts and completed without tool use. The run audit verified
the frozen input hashes, exact source inputs in all 72 interpreter prompts, and the 18 shared `L0`
observations. Three graders scored the anonymous packets. An independent blind reviewer reconciled
grading differences before the arm mapping and costs were opened.

| Measure                                      | Baseline | Candidate |
| -------------------------------------------- | -------: | --------: |
| Full `L1` closure among 12 eligible pairs    |        3 |         6 |
| `L1` preservation among 6 no-gap pairs       |        5 |         4 |
| Source-fidelity hard-failure arms among 18   |        1 |         1 |
| Median interpreter output tokens per pair    |    202.5 |     140.5 |
| Median interpreter elapsed time per pair (s) |    9.575 |      8.36 |

The three candidate-only `L1` closures occurred in three cases across repeats 1 and 3. The seed
cases recovered the same-cultivar criterion for the Friday candidate number. The transcription case
recovered why only supplied characters belonged in brackets and where to put the sample. There were
no baseline-only `L1` closures. Both arms carried the supported woodshop request and closed its
measurement and entry gaps in all three repeats. The baseline repaired one follow-up question about
the subject of the facilities check. That repair occurred in a no-gap pair and adds no `L1` closure.
The paired median candidate-to-baseline ratios were 0.7554 for output tokens and 0.8864 for elapsed
time. Both arms had a median of one delivered turn.

**Review state: rejected.** In the first floor-marker repeat, the source left marker permission open
and identified the equipment custodian as the person who could resolve it. The candidate's
clarification told the survey attendant to decide whether to apply the marker. The listener then
planned to apply it because no prohibition had been stated, and the candidate repeated the invented
delegation in its follow-up. This candidate-only hard failure meets the rejection rule. In the
second floor-marker repeat, the candidate's listener attributed the interpreter's suggestion to ask
about the marker to the speaker, losing preservation while still planning to defer. The baseline's
distinct hard failure occurred in the informed seed-library case, where its relay added a
reservation-table instruction. The paired failures identify where the protocol rejected the
candidate despite its higher `L1` closure count.

One hypothesis for a future evaluation is to leave unresolved actions open, direct the question to
the person who can resolve it, and require source evidence before reporting an instruction,
permission, or delegation. The baseline remains the runtime Skill.

Each listener observation came from a fresh model context with transcript history and structured
comprehension questions. The repeated synthetic cases provide no human grounding. These counts
describe this harness and leave effects on human understanding and decisions unmeasured.

## Plan-map candidate: rejected under the V2 held-out protocol

The [plan-map candidate snapshot](../evals/plan-map-candidate-rejected.md) made the speaker's
supported goal, means, condition, decision status, and requested response explicit before adapting
the interpretation to the listener. It is preserved byte for byte from the tested candidate (SHA-256
`257442417bfa4ed2c19450fffcc372d551fcce8d25b7edababe91e463d88867a`). The baseline was the retained
runtime Skill snapshot (SHA-256 `48c663541e064c26dee3478b8b50b13cdc812ba2f77c4f4f65d7da070019870d`).

The [third fixture](../evals/plan-gap-heldout-3-cases.json) supplied six fresh synthetic cases
(SHA-256 `c2e101dd6bc4b6efceb8c837c6c104065d6d1bc4c15ff86602edd1ec1ad44e21`). The
[V2 protocol](../evals/HELDOUT_PROTOCOL_V2.md) and [rubric](../evals/RUBRIC_V2.md) fixed
decision-relevant slots and required raw `L0` grades to be frozen before either interpretation arm
ran. Their frozen SHA-256 hashes were
`5c9195bfb42cf76bb74d02539c6f6178bc66f98c4178637edfb0e1fc96879b45` and
`4e1a4452b00c34c03f3e57d0782fad64ea1fc4a86fa74531af28ec918f1ae3b6`; the runner SHA-256 was
`63b4ec4b72ab0861ad1f18d5aa38cd903385af9810840c60994da9904769559c`. The frozen `L0` grade SHA-256
was `da0356ffef59b948cbd897ed67ba1863c3fabf04dd55ffaebe940a9703a722ff`. The comparison manifest
SHA-256 was `1fc9aef6774264c2983071913307db54d6025ae01f1f15bc8f02776a98e668d4`; the blind
adjudication SHA-256 was `89fddc45e624bc1557177c4c240718d2de0cac0ce2aa13d2bf4eb19d0782e8d0`. Codex
CLI 0.163.0 ran `gpt-6-luna` at medium reasoning effort for three repeats. The run audit found no
failed model calls or tool calls and verified reuse of the 18 frozen raw listener observations. The
18 planned pairs were all analyzable, with no exclusions. The blind grades were settled before the
arm mapping and cost records were opened.

| V2 measure                                            | Baseline | Plan-map candidate |
| ----------------------------------------------------- | -------: | -----------------: |
| Full `L1` closure among 12 eligible pairs             |        2 |                 10 |
| `L1` preservation among 6 no-gap pairs                |        2 |                  4 |
| First-message source-fidelity hard-failure arms of 18 |        4 |                  2 |
| Follow-up source-fidelity hard-failure arms of 18     |        1 |                  0 |
| Median interpreter output tokens per pair             |      162 |                238 |
| Median interpreter elapsed time per pair (s)          |    8.975 |              10.58 |

The candidate had eight paired `L1` wins across four cases and all three repeat indices, with no
primary losses; two pairs closed in both arms and two in neither. It preserved the supported
indirect request in all three film-night repeats, compared with one for the baseline. The
same-speaker rain-venue pair retained source facts in all six candidate relays, compared with one of
six baseline relays. Those gains did not clear the safety gates. In planetarium repeats 1 and 3, the
candidate said that correcting the reception board would make the already-decided 10:00 school
showing start on time. The source requested communication of the correct start time, not a change
that would cause it. Both were candidate-only first-message hard failures. Planetarium repeat 1 also
changed a baseline-preserved no-gap pair into a failed one. In the rain-venue assumption case's
first repeat, the candidate sent an unnecessary follow-up after the listener had already understood
the approved branch; the baseline correctly stopped. The candidate had three unnecessary follow-up
replies, while the baseline had one unnecessary reply and two missed repair opportunities. Two
candidate `L2` closures were already closed at `L1`; neither was a successful targeted repair.

The paired median candidate-to-baseline ratio was 1.547 for interpreter output tokens, exceeding the
V2 provisional-cost threshold of 1.25, and 1.165 for elapsed time, below its 1.50 threshold. Each
arm used 36 interpreter calls with complete usage records; delivered turns had median one and range
one to two in both arms.

Per-case interpreter cost sums the initial and follow-up calls in each repeat. Each cell gives the
baseline / candidate median [range] over three repeats:

| Case                  | Output tokens                 | Elapsed time (s)                          |
| --------------------- | ----------------------------- | ----------------------------------------- |
| Assistant caption     | 164 [109–227] / 430 [260–467] | 8.47 [8.13–9.27] / 13.22 [10.63–14.16]    |
| Film-night sign       | 128 [74–163] / 205 [193–212]  | 8.24 [8.21–8.68] / 9.64 [8.64–9.79]       |
| Library purchase      | 263 [161–424] / 163 [146–183] | 11.29 [7.88–13.73] / 8.76 [7.68–10.35]    |
| Rain-venue assumption | 161 [149–392] / 294 [292–385] | 11.49 [9.66–12.81] / 12.71 [10.53–12.78]  |
| Rain-venue dissent    | 421 [272–459] / 537 [268–851] | 13.49 [10.87–13.66] / 16.12 [12.60–21.19] |
| Planetarium handoff   | 103 [85–111] / 203 [163–216]  | 7.37 [7.27–8.30] / 9.02 [8.57–10.82]      |

**Review state: rejected.** Candidate-only hard failures, a confirmed no-gap regression, and a
follow-up-choice regression independently trigger the precommitted V2 rejection rule. The working
Skill remains the baseline. This result describes repeated transcripts from one model acting as a
simulated listener. The assistant-authored case uses a fresh interpreter of earlier assistant
content, and the harness does not measure a model interpreting its own live answer, human grounding,
or effects on real decisions.
