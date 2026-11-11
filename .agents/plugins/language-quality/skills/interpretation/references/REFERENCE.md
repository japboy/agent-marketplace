# Interpretation References

Use this source map when reviewing or changing the skill. For a live interpretation task, follow
`SKILL.md` and the evidence in the actual exchange. These publications motivate the workflow; they
do not establish the facts of a particular conversation or prove that the skill improves outcomes.

## Conceptual sources

The term predates Hermans's book. Pennington uses it in 1987 while citing earlier programming-plan
research; the earliest coinage is not established here. See the
[full text of Pennington's paper](https://www.cs.kent.edu/~jmaletic/cs69995-PC/papers/pennington87.pdf),
pp. 307–309.

| Source                                                                                                                                                                                                                                                                                   | What it supports in this skill                                                                                                                                                                                                                           | Boundary                                                                                                                                                                                                               |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Nancy Pennington, [“Stimulus Structures and Mental Representations in Expert Comprehension of Computer Programs”](https://doi.org/10.1016/0010-0285(87)90007-7) (1987), pp. 307–309                                                                                                      | Defines program plan knowledge as patterns of instructions that work together to accomplish functions, in contrast with text-structure knowledge.                                                                                                        | Cites earlier work by Rich, Shrobe, Waters, Soloway, and Ehrlich; it does not establish who coined the term or show that plan knowledge dominates initial comprehension. Its subject is programs, not AI conversation. |
| Felienne Hermans, [*The Programmer's Brain*, chapter 5](https://livebook.manning.com/book/the-programmers-brain/chapter-5/), especially “Text knowledge vs. plan knowledge” (§5.3.1 in the published book)                                                                               | Later explanation of plan knowledge as understanding what a code creator planned or aimed to achieve, beyond surface details.                                                                                                                            | A later exposition, not the term's original source. Applying the concept to a speaker's remark is this skill's analogy, not a tested interpretation method from the book.                                              |
| Herbert H. Clark and Susan E. Brennan, [“Grounding in Communication”](https://web.stanford.edu/~clark/1990s/Clark,%20H.H.%20_%20Brennan,%20S.E.%20_Grounding%20in%20communication_%201991.pdf) (1991), pp. 128–129, 132–133                                                              | Participants seek evidence of understanding sufficient for their current purpose; a listener's relevant next turn can supply evidence, and a revealed misunderstanding calls for repair.                                                                 | Sufficient understanding is contextual. The source does not require a readback or confirmation question after every relay.                                                                                             |
| Council of Europe, [CEFR Mediation](https://www.coe.int/en/web/common-european-framework-reference-languages/mediation) and [*CEFR Companion Volume*](https://rm.coe.int/common-european-framework-of-reference-for-languages-learning-teaching/16809ea0d4) (2020), §2.5 and pp. 114–118 | Mediation can occur within one language or across languages. The descriptors cover differences in domain knowledge, relevant background, links to prior knowledge, audience-appropriate language, clarification, and misunderstandings or disagreements. | The CEFR describes language mediation competencies; it does not prescribe this skill's output structure or access to agent memory.                                                                                     |

## Professional interpreting practice

- NAATI,
  [*Interpreter Certification: Knowledge, Skills and Attributes*](https://www.naati.com.au/wp-content/uploads/2020/02/Knowledge-Skills-and-Attributes_Interpreter.pdf)
  (2016), §§5.5 and 5.6.1: thematic competence covers the subject, terminology, setting, audience,
  and interlocutors. Discourse analysis includes understanding what participants use language to
  achieve. These directly support gathering relevant context and identifying a speaker's purpose.
- AUSIT,
  [*Code of Ethics and Code of Conduct*](https://ausit.org/wp-content/uploads/2024/09/AUSIT-Code-of-Ethics-and-Code-of-Conduct.pdf)
  (2012), §§5.1–5.4, 6.1, and 7.4: accurate transfer preserves content and intent without adding or
  omitting anything; practitioners seek clarification where possible, request background material,
  and keep interpreting distinct from advice. These support avoiding invented listener requests and
  keeping any advice visibly separate from the relay.

Both documents address professional human interpretation, principally between languages. Neither
specifies same-language mediation, an agent interpreting its own answer, or use of session memory.
AUSIT Int12 also leaves judgments about participants' understanding to the participants; its code is
not the basis for the skill's grounding check. The grounding rationale above comes from Clark and
Brennan, and the check does not certify a listener's understanding.

## Skill design decisions

The sources above inform the goal-and-means reading, listener adaptation, accurate transfer, and
grounding loop. The following are this skill's operational choices for an AI-mediated session, not
procedures specified by those sources:

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
