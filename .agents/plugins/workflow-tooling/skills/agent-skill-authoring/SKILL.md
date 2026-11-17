---
name: agent-skill-authoring
description: >
  Create, update, validate, and review Agent Skills for Codex and Claude Code.
  Use when the user asks to "create a skill", "make a new skill", "define a
  skill", "write SKILL.md", "improve a skill description", "set up skill
  directories", "add Codex openai.yaml metadata", "validate skill structure",
  apply SkillOpt-style evaluation, or distinguish standard Agent Skills
  requirements from Codex- or Claude Code-specific practices.
---

# Agent Skill Authoring

## Purpose

Create and review skills by separating four layers clearly:

1. **Agent Skills standard**: Format and validation rules from the shared specification
2. **Shared authoring practices**: Recommendations from standard-site authoring guidance and
   cross-product experience, not spec requirements
3. **Product-specific practices**: Conventions that apply only to Codex or only to Claude Code
4. **Evidence-based iteration**: Evaluation and review criteria for updating existing skills from
   measured results

Never present a product-specific convention or a recommended practice as if it were part of the
Agent Skills standard.

## Authoritative Sources

Use these sources in this order:

1. Agent Skills specification for cross-product format rules
2. Agent Skills standard-site authoring and evaluation guidance for recommended practice
3. Product documentation for Codex- or Claude Code-specific behavior
4. Product-maintained example repositories for implementation patterns
5. Research sources such as SkillOpt, and vendor model-prompting guides, for additional review
   rationale

Standard-site authoring guidance is authoritative for practice but adds no validation rules. Vendor
model-prompting guides describe one model on one harness; cite them as fixed-target evidence, never
as portable rules.

See [REFERENCE.md](references/REFERENCE.md) for the source map and cross-checking guidance.

## Working Model

Start each skill task by classifying the target: standard only, Codex only, Claude Code only, or
both Codex and Claude Code.

If the target product is unclear, default to:

1. A standard-compliant baseline
2. Shared practices that help multiple clients
3. Optional product-specific additions called out explicitly
4. Measured evaluation only for non-trivial updates or reviews

## Standard Baseline

This is the portable baseline that should remain true across products.

### Directory Structure

A skill requires `skill-name/SKILL.md`. The optional standard conventions are `scripts/`,
`references/`, and `assets/`; the specification also allows other files and directories.

### Frontmatter

Write YAML frontmatter at the top of `SKILL.md`. `name` and `description` are required. `license`,
`compatibility`, `metadata`, and `allowed-tools` are optional standard fields; `allowed-tools` is
experimental and client support varies.

`name` is 1-64 characters of lowercase alphanumeric characters and hyphens, with no leading,
trailing, or consecutive hyphen, and must match the parent directory name. `description` is a
non-empty string of 1-1024 characters. The specification recommends describing what the skill does
and when to use it. Assess that quality in review. `compatibility`, if present, is 1-500 characters.
`metadata`, if present, maps string keys to string values. See the field rules and validator scope
in [REFERENCE.md](references/REFERENCE.md).

Validate with:

```bash
uvx --from skills-ref agentskills validate ./skill-name
```

### Standard Progressive Disclosure

Put trigger-critical information in `name` and `description`, keep `SKILL.md` focused on the core
workflow, and move detail into `references/`, deterministic operations into `scripts/`, and
templates or output resources into `assets/`.

Specification-backed targets:

- Keep `SKILL.md` instructions under the recommended 5,000-token guidance when practical, and the
  file under 500 lines
- Use relative paths from the skill root when referencing bundled files
- Keep references close to `SKILL.md`; avoid deep reference chains

Two consequences worth applying deliberately:

- State *when* to load each supporting file. "Read `references/api-errors.md` if the API returns a
  non-200 status code" is loadable on demand; "see `references/` for details" is not.
- Put the rules that must hold for the whole task near the top of `SKILL.md`. Some clients truncate
  skill body during activation or after context compaction. Check behavior in the target client when
  the skill depends on instructions late in the file.

## Shared Practices for Codex and Claude Code

These are strong cross-client recommendations, not specification requirements unless stated
otherwise.

### Description Quality

Use `description` as the primary trigger surface.

Good descriptions:

- Say what the skill does
- Say when it should be used
- Include concrete user/task language
- Make scope boundaries obvious
- Front-load the key use case and trigger words

Clients can share a listing budget across skills and shorten descriptions or omit entries when the
budget fills. Put the key use case first and check the target client's listing behavior.

Do not force one house style as if it were required by the spec. Third-person phrasing, imperative
phrasing, and quote-heavy trigger lists can all be useful, but they are authoring choices.

Optimize a description by measurement, not intuition: label realistic should-trigger and
should-not-trigger prompts, hold part of them back, and select the wording with the best held-out
result. See [evaluation-workflow.md](references/evaluation-workflow.md).

### Resource Selection

Use resource directories intentionally:

- `scripts/`: deterministic helpers, reusable automation, or fragile sequences
- `references/`: long or topic-specific guidance that should load on demand
- `assets/`: templates, boilerplate, icons, fonts, sample outputs, or other output-side artifacts
- Extra directories: allowed when they clearly serve the skill, but document them explicitly from
  `SKILL.md`
- Scripts that read or write files should keep path inputs finite and verify resolved paths stay
  inside the intended base

### Writing Style and Instruction Calibration

Use direct, concrete language. Encode procedural rules, tool policies, output constraints, and known
failure modes when they are supported by evidence. Show positive examples of the wanted behavior
rather than lists of prohibitions. Imperative or infinitive phrasing is usually effective, but do
not treat second person or alternative phrasing as an automatic spec violation.

Every line of an active skill is a recurring context cost, so include only what changes behavior.
For each instruction, ask whether the agent would get this wrong without it. If not, cut it.

- **Match specificity to fragility.** Be prescriptive where an operation is fragile or a sequence is
  mandatory. Where several approaches work, state the outcome and the reason instead of the steps,
  and leave the path to the agent.
- **Use observable verification.** Specify the check that demonstrates the outcome, such as a
  validator for a generated file or a test that exercises changed behavior. Run the applicable check
  before reporting success and report any required check that remains blocked. Use target runs to
  identify repeated rules and generic re-checks that can be removed.
- **State success criteria and stopping conditions.** Define the requested deliverables and the
  evidence that each is complete. Continue through recoverable failures within scope and existing
  authorization. Report a blocker when the remaining work needs missing input or permission, or when
  the available checks cannot establish completion.
- **Reserve absolute language for invariants.** Keep always, never, must, and only for safety rules,
  required fields, and actions that must not happen.
- **Separate exhaustive generation from filtering.** Instructions to be conservative or to report
  only severe findings are followed literally and suppress recall. Ask for everything, then filter
  in a distinct phase.
- **Specify communication when the task needs it.** Set the intended length for user-facing outputs
  and name meaningful milestones for progress updates in long interactive work. If updates are
  missing, check what the client displays before changing the wording.
- **Watch for over-constraint.** When added rules stop improving results, delete instructions and
  check whether results hold.

For reusable content structures such as gotchas, output templates, checklists, validation loops, and
plan-validate-execute, see [instruction-patterns.md](references/instruction-patterns.md).

### Validation Beyond Syntax

Match each claim to its observable check. Use the validator for format, activation trials for
trigger changes, and representative tasks for behavior changes. Check that bundled references
resolve and exercise supporting scripts on representative inputs. Record the observed results and
any unverified product behavior in the validation notes.

## Codex-Specific Practices

Apply this section only when the skill targets Codex or both products.

### Codex Skill Discovery

Codex scans `.agents/skills` from the current working directory up to the repository root, plus user
skills in `$HOME/.agents/skills`, admin skills in `/etc/codex/skills`, and system skills bundled
with Codex. It follows symlinked skill folders, and `~/.codex/config.toml` can disable a skill with
`[[skills.config]]`.

Direct skill folders suit local authoring and repo-scoped workflows; plugins are the distribution
unit for reusable skills and app integrations.

By default, the initial skills list uses at most 2% of the model's context window, or 8,000
characters when the window is unknown. Codex shortens descriptions and may omit entries in large
lists. `skills.max_context_tokens` sets a custom budget up to 10,000 tokens.

### `agents/openai.yaml`

Codex supports product-specific metadata in `skill-name/agents/openai.yaml` for Codex-only UI
metadata, icons, brand color, default prompts, implicit invocation policy, and declared tool
dependencies. It is a Codex product extension, not part of the Agent Skills standard: a skill is
standard-compliant without it, and a Codex-focused skill is usually better with it.
`policy.allow_implicit_invocation` defaults to `true`; setting it to `false` still permits explicit
`$skill` invocation.

See [REFERENCE.md](references/REFERENCE.md) for the current representative `openai.yaml` fields.

### Codex Authoring Guidance

For Codex-focused skills:

- Keep the standard `SKILL.md` portable
- Put Codex-only UI or policy metadata in `agents/openai.yaml`
- Generate `openai.yaml` for new metadata. Edit the affected fields in an existing file to preserve
  its other interface, policy, and dependency settings
- Keep `default_prompt` short and aligned with the intended invocation
- Test prompts against the description to confirm explicit and implicit trigger behavior

Invoke the built-in Skill Creator with `$skill-creator` when available. To call its helpers
directly, use the bundled location under the active Codex home and verify each target is a regular
readable file. See [REFERENCE.md](references/REFERENCE.md) for the location and helper names.
Otherwise, create the files directly and run the portable validator.

## Claude Code-Specific Practices

Apply this section only when the skill targets Claude Code or both products.

Claude Code follows the Agent Skills open standard, then adds Claude Code-only features such as
invocation control, dynamic context injection, subagent execution, hooks, model/effort overrides,
and additional discovery locations.

Important distinctions:

- For portable skills, keep the standard `name` and `description` baseline
- For Claude Code-only skills, Claude Code treats all frontmatter fields as optional and recommends
  `description` so Claude knows when to use the skill
- For personal and project skill directories, frontmatter `name` can set the slash command, and the
  directory name also invokes it. Plugin skills keep the plugin namespace and use `name` for the
  last segment when set. See [REFERENCE.md](references/REFERENCE.md) for other layouts
- Skills live under `~/.claude/skills/`, project `.claude/skills/`, `<plugin>/skills/`, and
  enterprise-managed locations

Claude Code-specific frontmatter includes `when_to_use`, `argument-hint`, `arguments`,
`disable-model-invocation`, `user-invocable`, `disallowed-tools`, `model`, `effort`, `context`,
`agent`, `background`, `hooks`, `paths`, and `shell`. Use them when the target needs Claude Code
behavior. The standard's experimental `allowed-tools` field pre-approves matching tools during the
invoking turn in Claude Code.

Claude Code context accounting:

- `description` and `when_to_use` are combined for the listing and truncated at a configurable
  default of 1,536 characters per entry. Keep the key use case first.
- By default, the listing budget scales at 1% of the model's context window. On overflow, Claude
  Code drops descriptions starting with the least-invoked skills, so a rarely used skill loses its
  trigger text first.
- After auto-compaction, only the first 5,000 tokens of each re-attached skill survive, within a
  combined 25,000-token budget filled from the most recently invoked skill. Place durable rules near
  the top of `SKILL.md`.

Claude Code supports dynamic context injection with `` !`command` `` and ` ```! ` fenced command
blocks. Treat this as Claude Code-specific behavior, use `${CLAUDE_SKILL_DIR}` for bundled files,
keep commands deterministic, and account for settings that can disable skill shell execution.

Use `context: fork` for actionable tasks that can run without the main conversation history. The
fork normally runs in the background with a narrower tool set. Set `background: false` when the
invoking turn needs the result or the task requires a tool unavailable in the background. See
[REFERENCE.md](references/REFERENCE.md) for exceptions.

When a skill delegates, state which independent work warrants delegation and bound its scope.
Measure `model` and `effort` overrides on the target task. Check for a missing success criterion,
tool-selection rule, or verification step before raising effort.

For detailed Claude Code checks, use [validation-checklist.md](references/validation-checklist.md).

## Update Review

Use this section when updating or reviewing an existing skill. The axes combine standard-site
evaluation guidance with SkillOpt, which treats a skill as an external, trainable text state for a
fixed target model and harness. Use them for review discipline; none of them are format
requirements.

For non-trivial updates, check these axes:

- **Fixed target**: Record the product and harness version, model, effort, and evaluator. When the
  target changes, rerun the unchanged skill there before testing edits against it.
- **Evidence**: Base edits on representative prompts, trajectories, logs, outputs, verifier results,
  or reviewer judgments.
- **Success/failure separation**: Repair systematic failures and preserve reusable success patterns
  without merging anecdotal one-offs into rules.
- **Bounded edits**: Prefer small add/delete/replace changes over rewrites, and treat deletion as a
  first-class edit rather than a cleanup step.
- **Validation gate**: Compare the previous and candidate skill on representative or held-out
  prompts before accepting behavior changes.
- **Explicit review state**: Classify a behavior-changing candidate as `provisional` until the
  validation gate passes, then as `accepted` or `rejected`. A provisional update may be distributed
  when an immediate correction is required, but do not claim that it improves behavior and keep its
  follow-up evaluation explicit.
- **Cost accounting**: Record token count and duration alongside quality for both sides. A large
  token increase for a small quality gain is a reason to reject an edit, not a neutral trade.
- **Rejected edits**: Record rejected changes and why, when that will help future reviews.
- **Record/runtime separation**: Put changelogs, evaluation notes, rejected edits, and decision
  records in `references/`; promote only validated runtime rules into `SKILL.md`.
- **Traceability**: Keep the evidence behind accepted changes recoverable without turning history
  into task instructions.
- **Generalization**: Encode reusable procedures, tool policies, applicability conditions, output
  constraints, and failure modes, not task-specific answers.
- **Transfer**: If the skill claims portability, test or document each intended product or harness.
- **Compactness**: Keep runtime instructions inspectable; keep bulky evidence and reviewer rationale
  out of activation-time instructions.

For the full checklist, use [validation-checklist.md](references/validation-checklist.md). This
skill demonstrates the maintenance-record subset with [CHANGELOG.md](references/CHANGELOG.md),
[evaluation-notes.md](references/evaluation-notes.md),
[rejected-edits.md](references/rejected-edits.md), and
[decision-records.md](references/decision-records.md). Its `evals/evals.json` cases cover portable
creation, a standards review, and an update supported by one anecdote. Recorded runs and their
limits are in the evaluation notes.

## Creation Workflow

Follow this workflow unless the task is narrowly scoped enough to skip parts of it.

### Step 1: Clarify the Target

Identify whether the skill targets standard Agent Skills only, Codex, Claude Code, or both Codex and
Claude Code.

### Step 2: Collect Concrete Use Cases

Gather real user requests that should trigger the skill, and near-miss requests that should not. Ask
what a user would actually say and where the boundary against adjacent skills falls.

Ground the content in real expertise rather than general knowledge: extract the pattern from a task
actually completed with an agent, or synthesize it from project artifacts such as runbooks, schemas,
review comments, and past failures. Skills written from general knowledge alone produce vague
procedures.

### Step 3: Plan Reusable Resources

For each representative task, determine the core workflow, identify repeated or fragile operations,
and decide whether they belong in `scripts/`, `references/`, `assets/`, or another clearly justified
directory.

### Step 4: Create the Baseline Skill

Create the portable baseline first: the skill directory, `SKILL.md`, only the resource directories
actually needed, then validation against the standard.

For a Codex-focused skill, use the built-in Skill Creator when available or create the portable
baseline directly.

### Step 5: Add Product-Specific Extensions

Only after the baseline is sound:

- Add `agents/openai.yaml` for Codex if needed
- Add Claude Code frontmatter or plugin structure only when the target requires Claude Code-specific
  behavior

### Step 6: Validate and Test

Validate in layers:

1. Standard syntax and naming
2. Shared trigger and resource quality
3. Codex-specific metadata if targeting Codex
4. Claude Code behavior if targeting Claude Code
5. Evidence, boundedness, validation, and traceability for non-trivial updates

### Step 7: Iterate

Update the skill after real use: strengthen or narrow the description, move long detail into
references, add scripts for repeated work, remove dead files and unused directories, delete
instructions that changed nothing, and preserve evidence for accepted and rejected changes.

## Evaluation and Iteration

Seeing a skill trigger tells you the agent found it, not that it helped. Measure triggering and
output quality separately, and always against a baseline.

1. Collect realistic prompts, including near-miss prompts that should *not* trigger the skill
2. Run each prompt with the skill and again without it, or against the previous version, starting
   from a clean context every time
3. Record pass rate together with token count and duration for both sides
4. Accept a change when the quality gain justifies the added cost
5. Feed failed checks, reviewer notes, and execution traces into the next bounded revision

Until step 4 passes, label the candidate `provisional`; syntax validation alone does not change that
state to `accepted`.

Context left over from authoring a skill hides gaps in the written instructions. Evaluate in a fresh
session or subagent with minimal leaked context: pass the skill and a user-like request, do not tell
the evaluator which problem is suspected, and tighten the skill if success depended on hidden hints.

Execution traces are the most informative signal: ignored instructions are usually ambiguous, and
wasted steps usually trace to instructions that should be simplified or removed.

For test-case format, assertions, grading, benchmarks, and description trigger evaluation, see
[evaluation-workflow.md](references/evaluation-workflow.md).

## What to Avoid

- presenting Codex or Claude Code extensions as if they were part of the standard
- claiming extra directories are forbidden when the spec allows additional files
- forcing one naming style such as gerunds as if it were required
- treating writing-style preferences as hard validation errors unless the user asked for that
  convention
- duplicating detailed content across `SKILL.md` and `references/`
- accepting skill rewrites without evidence, bounded scope, or validation
- shipping optimizer/reviewer-only notes as runtime instructions unless they are intentionally
  useful to the agent
- promoting one vendor's model-specific prompting guidance into portable authoring rules
- judging a skill by quality alone, without the token and time cost it adds
- answering every observed failure with another rule until the skill is over-constrained

## Quick Reference

- **Portable compliance**: follow the Agent Skills standard first
- **Better Codex UX**: add `agents/openai.yaml`
- **Claude Code behavior**: add Claude Code frontmatter, dynamic context, or plugin layout
  explicitly
- **Both**: keep `SKILL.md` standard, then layer Codex and Claude Code additions without mixing them
  into the baseline
- **Update review**: require evidence, bounded edits, validation, cost accounting, and traceability
  before accepting behavioral changes

See [validation-checklist.md](references/validation-checklist.md) for a layered review checklist.

## Completion

Complete creation when the files and references exist, the standard validator passes, and observed
checks meet the requested outcome and applicable product behavior. Complete an update review when
its `provisional`, `accepted`, or `rejected` state follows from the recorded evidence. If a required
check is blocked, report the remaining work and the evidence needed to close it.
