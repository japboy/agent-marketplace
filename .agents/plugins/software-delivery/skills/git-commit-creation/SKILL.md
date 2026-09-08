---
name: git-commit-creation
description: >
  Create authorized, atomic Git commits with repository-compliant messages and
  current-agent attribution. Use only when the user explicitly asks to create a
  commit or to commit already-scoped changes. Do not use for requests limited to
  staging, status inspection, commit planning, or drafting a message.
---

# Git Commit Creation

## Contract

Create one [atomic commit][atomic-commits] containing one logical change, only for an explicit user
request with a finite file or hunk scope. Resolve the repository, branch, scope, message policy, and
agent attribution before mutation. Preserve unrelated staged and unstaged changes; do not re-request
authorization already supplied.

Under this skill's house policy, stop on `main`, `master`, or repository-declared protected
branches. Branch creation or switching requires separate authorization. At any step, stop if
authorization, scope, or attribution is missing; resume only when the blocking condition is
resolved.

## Workflow

### 1. Inspect Without Mutation

- Read applicable repository instructions. Inspect the root, branch, worktree, and index with `git
  rev-parse --show-toplevel`, `git branch --show-current`, `git status --short --branch`, `git
  diff`, and `git diff --staged`. Record pre-existing staged content and remaining changes.
- Resolve `HEAD` with `git rev-parse --verify HEAD`. Record its OID when it exists; otherwise
  confirm an unborn branch before treating the next commit as a root commit. Other errors require
  diagnosis.

### 2. Establish the Staged Scope

- Stage only authorized paths or hunks using explicit path arguments; do not stage a whole file when
  authorization covers only part of its changes. Include pre-existing staged changes only when the
  user explicitly included them.
- Run `git diff --staged --check` and inspect `git diff --staged`. Proceed only if the staged diff
  is non-empty, contains one logical change, and matches the authorized scope. If unrelated staged
  content cannot be separated while preserving user work, ask how to scope the commit.

### 3. Commit and Verify

- Prepare the message using the policy below. Immediately before committing, confirm the recorded
  HEAD and reviewed staged diff still match. Reassess any changes before proceeding.
- Pass the message through a file with `git commit -F <message-file>`, preserving actual newlines.
- Check `git rev-list --parents -n 1 HEAD`: the new commit must have exactly one parent equal to the
  recorded OID, or no parents for an unborn branch. Verify the committed diff matches the reviewed
  staged diff and the full message contains the required attribution exactly once.
- Inspect `git status --short --branch` and report the new OID, summary, and remaining changes.
  Report failures or mismatches without claiming completion or altering unrelated work.

## Message

Follow repository instructions first. The following defaults are house policy, not Git requirements:

- Use [Conventional Commit-style](https://www.conventionalcommits.org/en/v1.0.0/) titles:
  `<type>(<scope>): <subject>`; omit an uninformative scope. Use a concise imperative subject
  without a trailing period, aiming for a title of 50 characters or fewer.
- Use `feat` for features, `fix` for bug fixes, `refactor` for code restructuring without behavior
  changes, `docs` for documentation, `test` for tests, and `chore` for maintenance.
- Omit the body when the title suffices. Otherwise separate it with a blank line and use concise `-`
  bullets under useful `Problem:`, `Change:`, and `Rationale:` sections. Add `Alternatives:` only
  for meaningful rejected options or trade-offs. Omit empty sections and repeated points; wrap at
  about 72 columns where practical.
- Include relevant issue references or breaking-change footers when applicable.
- Append exactly one current runtime-supplied attribution block, verbatim, after other footers. For
  Codex, use `Co-authored-by: Codex <noreply@openai.com>` unless the runtime supplies a different
  block. For other runtimes, require their supplied attribution; if unavailable, request it before
  committing. Do not invent identities, copy illustrative signatures, or combine runtime signatures.

## Sources

- [Git commit documentation source](https://github.com/git/git/blob/master/Documentation/git-commit.adoc)
  describes index-based commits, message files, and short titles separated from bodies by a blank
  line.
- [Git contribution guidance](https://github.com/git/git/blob/master/Documentation/SubmittingPatches)
  explains imperative subjects and motivation; these are Git project conventions.
- [GitHub co-author documentation](https://docs.github.com/en/pull-requests/committing-changes-to-your-project/creating-and-editing-commits/creating-a-commit-with-multiple-authors)
  documents co-author trailers; requiring agent attribution is this skill's house policy.

[atomic-commits]: https://github.com/git/git/blob/master/Documentation/SubmittingPatches#separate-commits
