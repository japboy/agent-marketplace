# Instruction Patterns

Choose the patterns that help the skill deliver an observable result. The
[Agent Skills authoring guide](https://agentskills.io/skill-creation/best-practices) explains how to
calibrate control and write reusable instructions.

## Calibrating Control

Match instruction specificity to task fragility, and calibrate each part of a skill independently.

- **Give the agent freedom** when multiple approaches are valid and the task tolerates variation.
  For flexible instructions, explaining *why* is more effective than a rigid directive, because an
  agent that understands the purpose makes better context-dependent decisions.
- **Be prescriptive** when operations are fragile, consistency matters, or a specific sequence must
  be followed. State the exact command and say that it must not be modified.
- **Provide defaults, not menus.** When several tools or approaches could work, pick one default and
  mention alternatives briefly. Options presented without a clear default are a common cause of
  wasted agent steps.
- **Favor procedures over declarations.** Teach how to approach a class of problems rather than what
  to produce for one instance. Specific details such as output templates, constraints, and tool
  names are still valuable; it is the *approach* that should generalize.

## Gotchas Sections

Often the highest-value content in a skill: concrete, environment-specific facts that defy
reasonable assumptions. These are corrections to mistakes the agent will otherwise make, not general
advice.

```markdown
## Gotchas

- The `users` table uses soft deletes. Queries must include `WHERE deleted_at IS NULL` or results
  will include deactivated accounts.
- The `/health` endpoint returns 200 as long as the web server is running, even if the database
  connection is down. Use `/ready` for full service health.
```

Keep gotchas in `SKILL.md` where the agent reads them before hitting the situation. A separate
reference file works only if the skill states when to load it; for non-obvious issues the agent may
not recognize the trigger.

When an agent makes a mistake that has to be corrected by hand, adding the correction here is one of
the most direct ways to improve the skill.

## Templates for Output Format

Provide a concrete template rather than describing the format in prose; agents pattern-match well
against structures. Short templates can live inline in `SKILL.md`. Longer templates, or templates
needed only in some cases, belong in `assets/` and should be referenced from `SKILL.md` so they load
on demand.

## Checklists for Multi-Step Workflows

An explicit checklist helps the agent track progress and avoid skipping steps, especially when steps
have dependencies or validation gates.

```markdown
Progress:

- [ ] Step 1: Analyze the form (run `scripts/analyze_form.py`)
- [ ] Step 2: Create field mapping (edit `fields.json`)
- [ ] Step 3: Validate mapping (run `scripts/validate_fields.py`)
```

## Validation Loops

Name the artifact or state that must be checked, the relevant test, validator, or source of truth,
and what counts as a pass. Correct actionable failures within the authorized scope and rerun the
relevant check. Include checks that exercise the requested result. For example, compare preserved
issue links with the release notes when rewriting a changelog.

Complete the task when the requested deliverable or state and its required checks are satisfied. If
a required check cannot run, report the missing evidence and the blocker. Continue independent,
authorized work while a user decision or required permission is pending.

## Plan-Validate-Execute

For batch or destructive operations, have the agent write an intermediate plan in a structured
format, validate that plan against a source of truth, and only then execute.

```markdown
1. Extract form fields: `python scripts/analyze_form.py input.pdf` -> `form_fields.json`
2. Create `field_values.json` mapping each field name to its intended value
3. Validate: `python scripts/validate_fields.py form_fields.json field_values.json`
4. If validation fails, revise `field_values.json` and re-validate
5. Fill the form: `python scripts/fill_form.py input.pdf field_values.json output.pdf`
```

The essential ingredient is step 3: a validator that checks the plan against the source of truth and
emits errors specific enough for the agent to self-correct.

## Bundling Reusable Scripts

When comparing execution traces across evaluation runs, watch for the agent independently
reinventing the same logic each time (building a chart, parsing a format, validating output). That
is the signal to write a tested script once and bundle it in `scripts/`.

## Sourcing Skill Content

Skills generated purely from an LLM's general knowledge produce vague procedures ("handle errors
appropriately"). Ground the skill in real expertise instead:

- **Extract from a hands-on task.** Complete a real task with an agent, then extract the reusable
  pattern. Pay attention to the steps that worked, the corrections that had to be made, the
  input/output formats, and the project-specific context that had to be supplied.
- **Synthesize from project artifacts.** Internal runbooks, style guides, API specifications, code
  review comments, version control history, and real failure cases outperform generic reference
  material, because they capture the actual schemas, failure modes, and recovery procedures.
