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

Relay what the speaker is trying to achieve and what they expect from this listener now. These are
separate questions. A goal or condition does not by itself assign anyone an action.

## Resolve the input

1. Identify the remark or answer to interpret and the listener. Use the source the user named, or
   the agent's own draft or prior answer when the user asks to interpret it. If the source cannot be
   identified, request it before composing a relay.
2. Find the listener's relevant role, knowledge, preferences, next decision or action, and whether a
   reply can be obtained. Use the current exchange first, then accessible relevant history, memory,
   or referenced material when needed. Ask for a missing detail only when it could change the
   meaning or the listener's next decision. Otherwise choose a reasonable level of explanation.
   Treat another source's stated goal as context, not automatically as this speaker's motive.

## Interpret the remark

1. Identify the speaker's goal, the means and conditions related to it, and any response the speaker
   expects from the listener. Distinguish information, proposal, request, and decision, and preserve
   speaker, scope, certainty, conditions, and deadlines. When a confirmed goal explains a means or
   condition, include that connection briefly even if the listener could answer the immediate
   request without it. Do not infer intent merely from roles.
2. Write a ready-to-use relay in the listener's language and terms. Attribute the speaker's position
   and add only background supported by the exchange or an identified source. Put your explanation
   of what is unknown, any questions, and your advice about the listener's decision in a separate
   clarification. A statement such as “this remark does not tell us whether you should proceed”
   belongs in the clarification, outside the relay. Do not extend a speaker's condition on their own
   action to a different action the listener is considering. When interpreting the agent's own
   answer for the user, preserve what was found or done, its limits, and the decision or reply
   actually sought. If the draft leaves that ask implicit, state it only when the task and the
   agent's own position support it. Otherwise leave it open in the clarification.
3. If an unresolved point could change the listener's decision or action, provide the supported
   relay and a separate, specific question addressed to whoever can resolve it. Keep the question
   pending even when that person is currently unavailable. Do not ask the listener to decide what an
   ambiguous speaker meant. Ask whether a speaker's condition applies to the listener's action when
   that scope is unknown. If the listener has no relevant next decision, omit unnecessary questions.

## Ground the understanding

- **One-way:** Deliver a relay containing the speaker's supported position. If a material point is
  unresolved, add a separate clarification with the question and its addressee. If the source
  already states the requested response and there is no material gap, end after the relay.
- **Two-way:** Use the listener's actual reply as evidence of understanding. When it reveals a
  material mismatch, identify the part misunderstood and explain the speaker's supported meaning to
  the listener. If the source does not resolve it, relay the listener's reading or question to the
  speaker, then relay the speaker's actual answer back. When the agent is the speaker, respond to
  the user directly. Check only the point needed for the next decision, preserving whether it
  remains a proposal or has become a decision. A relevant reply can show understanding even when the
  listener disagrees. Stop when the participants have enough shared understanding for the current
  purpose. If a reply is unavailable, leave the point open.

For skill updates or audits only, see the source map in [REFERENCE.md](references/REFERENCE.md) and
the observed results in [evaluation-notes.md](references/evaluation-notes.md).
