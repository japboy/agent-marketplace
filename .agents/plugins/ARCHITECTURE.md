# Plugin Collection Architecture

This document owns the structure and release invariants shared by every Plugin under
`.agents/plugins/`. Individual Skill workflows and runtime requirements remain owned by their
`SKILL.md`.

## Classification

| Plugin               | Install intent                                                      | Owned Skills                                                                                                                          |
| -------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `workflow-tooling`   | Maintain and extend agent workflows                                 | `agent-memory`, `agent-skill-authoring`, `handoff-context-summarization`                                                              |
| `software-delivery`  | Refine plans and record delivered changes                           | `git-commit-creation`, `github-issue-plan-refinement`                                                                                 |
| `language-quality`   | Research terminology and improve Japanese output                    | `japanese-naturalization`, `term-translation-research`                                                                                |
| `design-engineering` | Reconstruct design systems from evidence                            | `design-system-reverse-engineering`                                                                                                   |
| `web-engineering`    | Review Web implementation, tests, analytics, and state architecture | `web-design-standards-review`, `frontend-test-value-assessment`, `web-architecture-pattern-application`, `xstate-architecture-review` |

Plugin names express install intent in approximately two words. The marketplace already establishes
the agent context, so Plugin names do not use an `agent-` prefix.

## Canonical package shape

```text
<plugin>/
├── .codex-plugin/plugin.json
├── .claude-plugin/plugin.json
└── skills/
    └── <skill>/
        ├── SKILL.md
        └── scripts|references|assets|evals (when needed)
```

- Both manifests describe the same package version and physical `skills/` directory.
- Codex-only interface metadata stays in `.codex-plugin/plugin.json`.
- Claude-only schema declarations stay in `.claude-plugin/plugin.json`.
- Marketplace entries do not copy version, description, or publisher metadata from Plugin manifests.
- Each Skill directory is complete and uses relative references within its own root. Optional
  references to another Skill by name do not create a file or installation dependency.

## Architecture contract

This document is the normative source for collection structure. Contributors and reviewers confirm
these states when changing a Plugin, Skill, catalog, or manifest; the repository does not duplicate
them in a cross-product validator.

A Plugin release is ready only when all of these states are true:

1. `Owned`: every Skill name is unique across the collection.
2. `SelfContained`: no file in a Plugin is a symlink and no runtime file path escapes the Plugin
   root.
3. `Described`: both manifests agree on common release metadata.
4. `Cataloged`: both marketplaces expose the same ordered Plugin set and point to the owning
   directories.
5. `RightsStateKnown`: every distribution artifact agrees with the repository-wide licensing state.
   The current `LicenseUndecided` state contains no license files, metadata, or Skill terms.
6. `Reviewed`: the complete change has been reviewed against this architecture contract, and the
   applicable Agent Skills, Codex Plugin, and Claude strict validators pass.

Do not publish or install a release from an intermediate state.

## Change review

For every collection change:

1. Confirm each Skill appears under exactly one owning Plugin listed in `Classification`.
2. Confirm every Plugin matches `Canonical package shape` and contains only physical files.
3. Keep the Codex and Claude catalogs in the same Plugin order and point both entries to the owning
   `./.agents/plugins/<plugin>` directory.
4. Keep `name`, `version`, `description`, `author`, `homepage`, `repository`, and `keywords`
   equivalent across the two Plugin manifests; keep product-only fields in their owning manifest.
5. Confirm every Plugin, manifest, catalog, and bundled Skill agrees with the licensing state in the
   repository `ARCHITECTURE.md`.
6. Run the repository and product validators in `Release validation` before release.

## Release validation

Run the complete read-only repository gate:

```bash
mise run check
```

Validate every Codex Plugin:

```bash
for plugin in workflow-tooling software-delivery language-quality design-engineering web-engineering; do
  uv run --with pyyaml python ~/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py ".agents/plugins/$plugin"
done
```

Validate the Claude marketplace and every Claude Plugin:

```bash
claude plugin validate . --strict
for plugin in workflow-tooling software-delivery language-quality design-engineering web-engineering; do
  claude plugin validate ".agents/plugins/$plugin" --strict
done
```

## Authoring quality

The repository-level dprint gate inspects physical Markdown, JSON, and YAML under this directory;
Vale inspects its physical Markdown directly. Generated discovery projections never become the
input. dprint owns deterministic structure, Vale owns non-correcting prose policy, and the official
Agent Skills validator owns Skill format validation. The topology and cross-product metadata rules
above remain review-owned architecture contracts.

Formatting exceptions are local proof obligations. The literal reviewer prompt inside
`software-delivery` is range-ignored because its helper extracts and sends those exact bytes at
runtime. Four nested-fence templates in `design-system-reverse-engineering` are range-ignored
because recursive formatting removes bracketed placeholders or collapses significant ASCII-diagram
line breaks. Their outer four-backtick fences keep the embedded three-backtick examples valid and
keep the entire template in Vale's code-block exclusion. Other fenced Markdown examples may be
canonicalized.
