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
