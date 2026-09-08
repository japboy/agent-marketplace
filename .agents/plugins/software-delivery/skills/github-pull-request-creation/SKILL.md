---
name: github-pull-request-creation
description: >
  Create GitHub pull requests or draft their titles and descriptions from the
  final diff, change rationale, and verification evidence. Use when asked to
  open a PR, prepare a PR description, or rewrite an existing PR description.
  Do not use for commit-only tasks, code reviews, or issue plan refinement.
---

# GitHub Pull Request Creation

## Contract

Produce a concise explanation for a reviewer who has not read the conversation, with observable
verification items. Follow applicable repository instructions and PR templates, including language
and attribution; this skill's English text does not prescribe the PR language.

A request to create a PR authorizes publication within that scope. A request for text alone ends
with the prepared title and body. Preserve unrelated work; commit creation, implementation changes,
review loops, and merging are separate responsibilities, not automatic effects of this skill.

## Workflow

### 1. Establish the Evidence

- Resolve the target repository, base and head branches, final PR diff, and existing PR, if any. Use
  the base-to-head comparison from their merge base; exclude uncommitted or unpushed changes from
  claims about the published PR. Resolve an ambiguous target before publication.
- Read applicable PR instructions and templates. Gather the problem, constraints, and decisions from
  the user, linked issues, or project records, and collect actual verification results.
- Separate known reasons from missing context. Do not infer motivation from code alone. Ask only
  when missing context materially prevents an accurate description; prepare the supported parts.

### 2. Write for the Reviewer

- Lead with the concrete problem and resulting behavior. Add a before/after example when useful.
- Prefer why over what over how: explain non-obvious motivation, constraints, or trade-offs that
  affect review. Include implementation detail only when it helps assess correctness or risk.
- Describe the final change, not commit chronology, file inventories, or abandoned conversation
  plans. Rewrite the title and body when scope changes.
- Scale length to complexity. A small change usually needs one short paragraph and verification
  items. Omit empty headings, repeated explanations, and alternatives without review value.
- Honor the repository template while expressing these facts in its relevant sections. These writing
  rules are house policy, not mandatory GitHub formatting.

### 3. Record Verification

- Include a Markdown task list describing conditions or actions and their expected observable
  outcomes. For documentation or configuration, use externally inspectable properties.
- Mark an item `[x]` only when evidence shows that check succeeded for the described change. Leave
  unrun, failed, or blocked checks `[ ]` and briefly state their status and reason.
- Name what a test demonstrates; a command or "tests passed" alone does not describe a scenario.
  Include commands or result links when useful, without claiming coverage they do not establish.
- Missing verification does not prevent preparing the body. Do not silently turn a proposed test
  into a completed one or hide a failed check.

### 4. Deliver Within Scope

- For a text-only request, return the title and body without pushing or publishing.
- For authorized creation or editing, use the resolved target and prepared text. Check for an
  existing PR before creating one; reuse its URL and edit only when the request covers editing.
  Preserve unrelated human-authored content when editing an existing description.
- Pass multiline text through a structured argument or a body file, preserving actual newlines.
  Follow the user's draft/ready intent. Do not re-request authorization already supplied.
- Read back the published title, body, base, head, and draft state. Correct mismatches within the
  authorized scope and report the PR URL and outstanding checks. If a create call has an uncertain
  result, inspect existing PRs before retrying to avoid duplicates.

## Sources

- [GitHub review guidance](https://github.com/github/docs/blob/main/content/pull-requests/concepts/helping-others-review-your-changes.md)
  supports focused changes that reviewers can understand.
- [GitHub CLI implementation](https://github.com/cli/cli/blob/trunk/pkg/cmd/pr/create/create.go)
  accepts explicit title, body file, base, head, and draft options for PR creation.
