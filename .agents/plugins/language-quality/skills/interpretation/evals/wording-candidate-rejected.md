---
name: interpretation
description: >
  Interpret a participant's remark or the agent's own answer for a listener
  across languages, roles, or domains, including within the same language
  (通訳). Use when the listener needs the speaker's purpose, conditions, or
  expected response to understand a proposal, decide, or act. In an AI session,
  the agent's draft or prior answer may be the source and the user the listener.
  For wording-only translation or polishing, or standalone term research, use
  the workflow for that task instead.
---

# Interpretation

Help the listener understand what the speaker is trying to achieve and how, so they can make their
next decision. Relay an expected response when the speaker's meaning supports one.

## Resolve the input

1. Identify the remark or answer to interpret and the listener. Use the source the user named. When
   interpreting the agent's own output for the user, use its current draft or prior answer. If no
   source can be identified, request it before composing the interpretation.
2. Use the listener's role, knowledge, preferences, actual reply, and next decision to choose what
   to explain or clarify. Check who can respond or answer questions. Start with the current exchange
   and consult accessible history, memory, or referenced material when needed. Attribute a purpose
   or request only when the remark or other evidence traceable to the speaker supports it. Ask for a
   missing detail only if it could change the meaning or the listener's next decision.

## Interpret the remark

1. In the first interpretation, show how the speaker's purpose explains their means or conditions
   when the evidence supports that connection, even if the listener could answer the immediate
   request without it. Distinguish information, proposals, requests, and decisions.
2. Write an interpretation the listener can use directly, using their language and terms. Attribute
   the speaker's position and preserve its scope and certainty. Add only background supported by the
   exchange or an identified source. Put unresolved points, questions, and advice in a separate
   clarification. When interpreting the agent's own answer for the user, preserve what was found or
   done, its limits, and the decision or reply actually sought.
3. Before delivery, check each action against the source for who would act, what they would do and
   to what or whom, and whether it is optional, proposed, requested, or decided. Keep conditions and
   deadlines attached to the action they qualify. Include indirect requests when supported by the
   speaker's words in context. If an unresolved point could change the listener's decision or
   action, provide an interpretation based on the available evidence and a separate, specific
   question addressed to whoever can resolve it. Keep the question pending even when that person is
   currently unavailable. Do not ask the listener to decide what an ambiguous speaker meant. When it
   is unclear whether the speaker's condition applies to the listener's action, ask the speaker to
   clarify its scope. If the listener has no relevant next decision, omit unnecessary questions.

## Check and repair understanding

- **One-way:** Deliver an interpretation limited to what the speaker's remark or answer and relevant
  context support. If a material point is unresolved, add a separate clarification with the question
  and its addressee. If the speaker has already stated what reply they want and no material point is
  unresolved, end after the interpretation.
- **Two-way:** Use the listener's actual reply as evidence of understanding. When it reveals a
  material mismatch, identify the part misunderstood and explain the speaker's supported meaning to
  the listener. If the original remark or answer does not resolve the mismatch, relay the listener's
  reading or question to the speaker, then relay the speaker's actual answer back. When the agent is
  the speaker, respond to the user directly. Check only the point needed for the next decision,
  preserving whether it remains a proposal or has become a decision. A relevant reply can show
  understanding even when the listener disagrees. Stop when the participants have enough shared
  understanding for the current purpose. If the listener or speaker cannot provide a needed reply,
  leave that point open.

For skill updates or audits only, see the source map in [REFERENCE.md](references/REFERENCE.md) and
the observed results in [evaluation-notes.md](references/evaluation-notes.md).
