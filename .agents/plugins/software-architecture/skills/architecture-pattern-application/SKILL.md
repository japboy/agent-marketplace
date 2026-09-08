---
name: architecture-pattern-application
description: >
  Apply documented architecture patterns to design and review decisions. Use for
  monorepo or workspace directory layout, package placement and topology, or
  route-state product analytics, URL-state contracts, measurement manifests,
  and warehouse semantic models. Select only matching catalogue patterns;
  unrelated architecture and build-tool configuration are outside this skill.
metadata:
  author: "Yu Inao"
  author_email: "84360+japboy@users.noreply.github.com"
  copyright: "Copyright (c) 2026 Yu Inao."
  version: "0.2.0"
---

# Architecture Pattern Application

## Purpose

Use this skill to apply a documented design pattern to a concrete architectural problem. Keep
pattern-specific assumptions in the selected reference rather than treating them as universal
architecture rules.

The expected output is an architectural decision, critique, or pattern proposal that selects and
applies the relevant reference pattern from this catalogue.

## Architectural Axioms

Apply these axioms consistently:

- Declarative
- Self-describing
- Deterministic
- Explicit state
- Finite state
- Self-documenting
- Exhaustive
- Predictable

Prefer designs where important behavior is derived from explicit models instead of scattered
procedural side effects.

## Working Model

Start by identifying the architectural level of the user's question:

- conceptual model
- information architecture
- application state
- repository or workspace topology
- runtime boundary
- data or observability model
- operational contract
- governance or review policy

Then load only the reference files needed for that level. Do not import one reference pattern's
assumptions into unrelated architecture decisions.

Match the request to catalogue entries before assessing evidence. If no entry matches, return one
`not-applicable` result with the reason and stop without generic architecture advice.

For each matched pattern, choose exactly one applicability state:

- `applicable`: the project evidence is sufficient to apply this pattern.
- `defer`: a required project fact is missing. Name the missing fact and the artifact that can
  resolve it; stop recommendations for this pattern only.

A deferred pattern does not suppress another pattern's supported recommendation. Keep evidence
scoped to the decision it supports; if a missing fact is also required by another pattern, assess
that dependency explicitly rather than assuming the other decision is ready.

## Reference Catalog

Match the task against this catalogue before loading references. When a request spans both entries,
assess each separately and keep their evidence and applicability states distinct.

| Reference                                                                          | Use when                                                                                                                                                                                   |
| ---------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [Route-State-Based Product Analytics](references/route-state-product-analytics.md) | The task involves product analytics, tracking, declarative instrumentation, route transition logs, URL-as-state, IA-aligned route design, or DWH semantic modeling from web behavior logs. |
| [Monorepo / Workspace Layout](references/monorepo-workspace-layout.md)             | The task concerns directory layout, workspace member placement, unit versus role versus domain grouping, or filesystem and build metadata consistency across ecosystems.                   |

## Review Stance

When applying a pattern:

1. Separate project facts, documented tool constraints, examples or conventions, and pattern
   recommendations. Cite the selected reference and the supporting primary source for tool claims.
2. Identify which reference pattern is being applied.
3. Keep each reference pattern's scope explicit.
4. Avoid applying a pattern merely because it is available.
5. Surface tradeoffs, missing evidence, and unknowns explicitly.
6. Prefer declarative, self-describing models over scattered procedural conventions.

## Output Shape

For each matched pattern, return a separate result labeled with its name. With multiple matches,
retain every result, including when all are deferred; do not collapse them into one overall state.

For each `applicable` result, prefer this structure:

1. **Decision**: the recommended architecture or review outcome
2. **Why**: the architectural rationale
3. **Reference**: the catalogue pattern and source links supporting the decision
4. **Model**: the explicit states, contracts, boundaries, or schemas involved
5. **Risks**: ambiguity, coupling, refactoring hazards, or semantic drift
6. **Checklist**: concrete validation questions
7. **Applicability State**: `applicable`

Keep the answer grounded in the actual project artifacts when reviewing a real codebase.

For each `defer` result, include only the pattern name, applicability state, reason, missing fact,
and resolving artifact. This restriction applies to that result, not the entire response.

When no catalogue entry matches, return only `not-applicable` and the reason.
