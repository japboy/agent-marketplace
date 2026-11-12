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

Help a particular listener understand the speaker's plan well enough for their next decision.
Grounding through actual replies is a way to correct a material misunderstanding when a reply is
available.

## Establish the source and listener

Use the remark or answer the user named; your own draft or prior answer can be the source. Ask for
the source if it cannot be identified. Find the listener's relevant knowledge, role, preferences,
and next decision from the current exchange, then accessible history, memory, or references when
needed. Ask for missing context only when it could change the meaning or next decision. Listener
context guides wording but does not establish the speaker's purpose, request, or authority. Check
who can reply to a material question.

## Separate the actions in the speaker's plan

Use the source in the context of the exchange. For every action material to the listener's next
decision, identify its **actor, action and object, purpose and means, state, condition or check,
decision owner, and requested response to this listener**. Attach a deadline to the action it
actually limits. Leave a field open when the evidence does not establish it. Keep the speaker's
goal-to-means link, including when it was explained earlier. Distinguish reported work, proposals,
decisions, completed actions, and requests. A condition on one action or the speaker's own planned
check does not become a condition or task for the listener's different action.

Before adapting, identify the wording or exchange that supports each request or question, including
who asks whom and when; do not rely on imperative grammar alone. Use earlier context to interpret it
without changing who asked or when. Keep this check internal. When a listener offers to do work and
the speaker responds by specifying a concrete task and object for that listener, carry it as an
indirect request, including its deadline if given. Conversely, the speaker's statement that *they*
will check or do something remains the speaker's action. The listener's role, plan, or silence does
not supply a request, permission, or delegated decision.

When interpreting your own answer, retain what you found or did, its limits, and the reply or
decision you actually seek. Do not invent an ask because the user has a next decision.

## Deliver a compact plan map

Use the labeled plan map whenever the speaker and listener have different material actions,
permission or decision ownership for the listener's action is unresolved, or an actual listener
reply shows a material mismatch. Otherwise use concise prose in the same order. Write the map with
short labels **in the listener's language** and natural, compact sentences.

- **Speaker's purpose and means:** State the speaker's established purpose and each source-supported
  goal-to-means link. Preserve whether a means changes, checks, or communicates the situation; do
  not present a report as a cause without source support.
- **Actions and state:** Without repeating the purpose and means, give each material action its own
  line: **who** does **what**, whether it is proposed, decided, or done, its condition, and any
  source-supported decision owner. For a pending check, state **who checks what** and **which action
  waits for it**.
- **Request to this listener:** Preserve the speaker's actual request or question, its addressee,
  scope, and deadline. If none is source-supported, write **none stated**. Keep a later reply
  separate from the earlier request. It may answer the speaker's question; preserve any offer,
  commitment, or action at its stated status. Put interpreter-added questions under **Interpreter's
  clarification**, not here; the speaker's own planned action is not a request.
- **Interpreter's clarification:** Only for a specific unresolved point that affects the next
  decision, address a question to whoever can answer or decide it; name a source-supported addressee
  or note if unknown. Keep it pending if they are unavailable. Missing instructions for the
  listener's separate task alone do not create a gap. Omit unsolicited procedural advice; mark
  requested advice as your own, never as a speaker instruction or permission.

The first three fields relay the speaker's source-supported position. The last field is yours and
must stay visibly separate. An action described as the speaker's plan is not an instruction to the
listener. In the simple-prose path, omit empty fields while preserving the same source boundary.
When the source is your own answer, speak directly to the user and localize the labels accordingly.

## Check and repair only what matters

Keep the named source and later listener reply separate; a later answer can resolve a source
question without rewriting the original request. Check the reply for a material mismatch before
passing it as an answer. Repair only a mismatch affecting the next decision, preserving the
speaker-versus-interpreter boundary. If a material question arises, answer it from the source when
possible; otherwise pass it to the person who can answer and relay their actual reply. If an answer
is unavailable, leave the question open. After any needed repair, relay an informed answer the
speaker sought. When you are the speaker, answer directly or use the listener's answer. Informed
disagreement can show understanding. If no material gap remains, add no explanation or new
suggestion. End when every material point is resolved or explicitly left open and available
requested answers have been relayed.

For skill updates or audits only, see the source map in [REFERENCE.md](references/REFERENCE.md) and
the observed results in [evaluation-notes.md](references/evaluation-notes.md).
