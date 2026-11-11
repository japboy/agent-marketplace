# Interpretation References

Use this source map when reviewing or changing the skill. For a live interpretation task, follow
`SKILL.md` and the evidence in the actual exchange. These publications motivate the workflow; they
do not establish the facts of a particular conversation or prove that the skill improves outcomes.

## Conceptual sources

| Source                                                                                                                                                                                                                                                                                   | What it supports in this skill                                                                                                                                                                                                                           | Boundary                                                                                                                                                          |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Felienne Hermans, [*The Programmer's Brain*, chapter 5](https://livebook.manning.com/book/the-programmers-brain/chapter-5/), especially “Text knowledge vs. plan knowledge” (§5.3.1 in the published book)                                                                               | Looking beyond surface details to a creator's goal and the relationships that explain a chosen means.                                                                                                                                                    | The book concerns program comprehension. Applying plan knowledge to a speaker's remark is this skill's analogy, not a tested interpretation method from the book. |
| Nancy Pennington, [“Stimulus Structures and Mental Representations in Expert Comprehension of Computer Programs”](https://doi.org/10.1016/0010-0285(87)90007-7) (1987), pp. 307–309                                                                                                      | The distinction between procedural relations and functional or goal-hierarchy relations behind the plan-knowledge framing.                                                                                                                               | This is research on understanding programs. It does not establish how an AI agent should interpret conversation.                                                  |
| Herbert H. Clark and Susan E. Brennan, [“Grounding in Communication”](https://web.stanford.edu/~clark/1990s/Clark,%20H.H.%20_%20Brennan,%20S.E.%20_Grounding%20in%20communication_%201991.pdf) (1991), pp. 128–129, 132–133                                                              | Participants seek evidence of understanding sufficient for their current purpose; a listener's relevant next turn can supply evidence, and a revealed misunderstanding calls for repair.                                                                 | Sufficient understanding is contextual. The source does not require a readback or confirmation question after every relay.                                        |
| Council of Europe, [CEFR Mediation](https://www.coe.int/en/web/common-european-framework-reference-languages/mediation) and [*CEFR Companion Volume*](https://rm.coe.int/common-european-framework-of-reference-for-languages-learning-teaching/16809ea0d4) (2020), §2.5 and pp. 114–118 | Mediation can occur within one language or across languages. The descriptors cover differences in domain knowledge, relevant background, links to prior knowledge, audience-appropriate language, clarification, and misunderstandings or disagreements. | The CEFR describes language mediation competencies; it does not prescribe this skill's output structure or access to agent memory.                                |

## Skill design decisions

The sources above inform the goal-and-means reading, listener adaptation, and grounding loop. The
following are this skill's own operational choices, not procedures established by those sources:

- Treat the source remark or answer and the listener as inputs, and use relevant session history or
  accessible memory when needed to understand the listener's context.
- Permit the agent's own draft or prior answer to be the source and the user to be the listener.
- Separate a ready-to-use relay from unresolved questions, advice, and other clarification.
- Preserve the distinction between the speaker's goal, a proposal or condition, and an action
  actually requested of the listener; do not create a request from the listener's role alone.
- Correct a material misunderstanding using the available source and check only what matters for the
  current decision. Treat informed disagreement as evidence of understanding, not as a failure to
  understand.

For the comparisons, observed failures, and remaining limits of these choices, see
[evaluation-notes.md](evaluation-notes.md).

## Skill format and evaluation

The [Agent Skills specification](https://agentskills.io/specification) permits a `references/`
directory alongside `SKILL.md`. Its
[evaluation guidance](https://agentskills.io/skill-creation/evaluating-skills) recommends comparing
a skill against a baseline or previous version on the same prompts. These are authoring sources, not
evidence for the interpretation theory above.
