# Agent Marketplace Architecture

This document owns repository-level architecture. Plugin package invariants are owned by
`.agents/plugins/ARCHITECTURE.md`.

## Purpose

The repository distributes the same physical Agent Skills to Claude Code and Codex. A Plugin
directory is the package, installation, versioning, and source of truth boundary. Product catalogs
and manifests describe that boundary but do not duplicate its Skill files.

## Project structure

```text
.
├── .agents/
│   └── plugins/
│       ├── ARCHITECTURE.md
│       ├── marketplace.json            # Codex catalog
│       └── <plugin>/
│           ├── .codex-plugin/plugin.json
│           ├── .claude-plugin/plugin.json
│           └── skills/<skill>/...
├── .claude-plugin/
│   └── marketplace.json                # Claude Code catalog
├── mise-tasks/
│   ├── hooks-install                   # Repository-local Git hook setup
│   └── skills-check                    # Full or affected Agent Skills validation
├── styles/
│   └── AgentMarketplace/               # Repository-owned Vale rules
├── tests/
│   └── vale/                           # Vale parser-scope fixtures
├── .github/workflows/quality.yml       # Separate format, prose, and Skill CI gates
├── hk.pkl                              # Git hook events and staged-file selection
├── .vale.ini                           # Repository-owned prose style entrypoint
├── dprint.json                         # Deterministic structured-file formatting
├── mise.toml                           # Native mise tools and declarative tasks
├── renovate.json5                      # Finite dependency-update policy
└── README.md
```

## Data flow

```text
.agents/plugins/<plugin>/skills/*
             │
             ├── .codex-plugin/plugin.json
             │        └── .agents/plugins/marketplace.json
             │
             └── .claude-plugin/plugin.json
                      └── .claude-plugin/marketplace.json
```

Both catalogs resolve their sources from the repository root and point to the same
`./.agents/plugins/<plugin>` directories. Installed products copy or cache those self-contained
directories; no installed Plugin depends on a path outside its own root.

```text
Repository Markdown/JSON/YAML ── dprint check/fmt ── structural state
Repository Markdown ───────────── Vale check ─────── prose policy
Plugin-owned SKILL.md ── skills-ref ───────── Agent Skills format
Plugin topology ──────── architecture review ─ dual-marketplace contract
```

Dependency declarations converge into two ordinary update states regardless of their manager:

```text
GitHub Actions / mise / Python / custom declarations ── weekly Renovate ── major PR ─ manual review
                                                                  └── non-major PR ─ CI ─ automerge
uv.lock ───────────────────────── weekly lock-file maintenance PR ─────────────── manual review
```

For Agent Skill validation, the two finite entry paths converge before invoking the validator:

```text
pre-commit ── hk staged files ─┐
                               ├─ mise run skills-check ── uv run --locked agentskills validate
manual / CI ── all Skill roots ┘
```

## Invariants

- `.agents/plugins/<plugin>/` is the physical SSOT for every distributed Skill.
- Every Skill has exactly one owning Plugin and retains its own `SKILL.md`, scripts, references,
  assets, and evaluation fixtures.
- A Plugin contains both product manifests. Their common identity, version, description, publisher,
  repository, and keywords remain equivalent.
- Catalogs are thin routing and classification layers. They expose the same ordered Plugin set and
  use explicit repository-relative source paths.
- Plugin directories contain physical files, not symlinks or references to a former canonical Skill
  tree.
- Cross-Plugin semantic recommendations may be optional, but runtime file references never cross a
  Plugin root.
- `.agents/skills/` and `.claude/skills/`, if generated for local authoring, are disposable
  projections. They are ignored by Git and never used for package installation.
- Licensing state does not define Plugin grouping. The repository, Plugin manifests, catalogs, and
  Skill frontmatter represent one repository-wide state described in `Licensing state`.
- `mise-tasks/` owns thin, executable adapters around locked repository tools. Substantial
  automation belongs in `apps/`, reusable language APIs belong in `packages/`, and child Git
  submodules belong in `repos/`.
- Root `mise.toml` owns pinned development tools, direct single-command tasks, and the declarative
  read-only quality-gate graph. The repository has no Node.js runtime or JavaScript package-manager
  dependency.
- Root `hk.pkl` owns Git hook events and staged-file filtering. Its read-only pre-commit step passes
  changed paths as separate arguments to the same mise task used for full validation; the task maps
  them to unique owning Skill roots. A completely deleted Skill is absent and requires no format
  validation, while any remaining root is validated as a whole. The step explicitly disables fixing
  and stashing, so validation never mutates the working tree.
- Document quality has two explicit owners: dprint owns deterministic Markdown, JSON,
  JSONC-compatible Renovate JSON5, and YAML formatting, while the repository Vale style owns
  Markdown prose policy without automatic correction. `renovate.json5` deliberately uses the JSONC
  subset of JSON5 and is explicitly associated with dprint's JSON plugin. The official Agent Skills
  reference CLI owns Skill format validation.
- Vale follows its native repository layout: `.vale.ini` is the root entrypoint, `styles/` is the
  `StylesPath`, and `tests/vale/` owns integration fixtures. The entrypoint selects only the
  repository-owned `AgentMarketplace` style; no external Vale package or `vale sync` step
  contributes policy. None belongs to an application or language workspace.
- Tool versions, remote artifacts, checksums, and supported platforms are finite repository state.
  mise resolves the independent dprint, Vale, and hk CLI versions from the native root `mise.toml`;
  its Aqua backend verifies upstream release checksums. uv resolves `skills-ref` from the root
  development dependency group and lockfile. CI, hooks, and local commands use the same state.
- Root `renovate.json5` owns dependency discovery and update policy. Its enabled manager list is
  exhaustive for the repository: native managers own GitHub Actions, mise, and PEP 621 declarations;
  custom regex managers own uv's required version, duplicated hk versions, and dprint plugin
  versions with their content digests.
- Ordinary dependency updates are created or updated only during the weekly Monday 00:00–03:59
  `Asia/Tokyo` window and have exactly two states across all managers: SemVer-major updates form one
  manual-review PR, while minor, patch, pin, digest, rollback, and bump updates form one non-major
  PR. Non-major PRs use Renovate-managed automerge only after required status checks pass; major PRs
  never automerge. Pre-1.0 minor and patch releases remain non-major by this policy.
- PyPI releases must be at least three days old before Renovate creates an update branch, matching
  uv's `exclude-newer` resolution policy. Lock-file maintenance uses the same weekly window in a
  separate manual PR. Dependency replacements also remain separate because Renovate does not combine
  replacement or lock-file-maintenance updates with ordinary dependency groups.
- Stable decisions are recorded in tracked architecture and documentation; local agent-memory state
  remains under the Git common directory.

## Licensing state

Licensing is explicit finite state rather than an inference from absent or inconsistent files:

- `LicenseUndecided` is the current state. The repository contains no repository- or Plugin-level
  `LICENSE` / `LICENSES.md` files, no `license` metadata in catalogs or manifests, and no `license`
  field or repository-originated license terms in bundled Skills.
- `LicenseDeclared` is a future state entered only by an explicit maintainer decision. That
  transition must update this architecture, every affected distribution artifact, and user-facing
  documentation together.

`LicenseUndecided` is not an open-source declaration or a grant of reuse rights. Copyright and
provenance records remain distinct from a license declaration. Any future third-party material must
retain notices required by its source terms; if those requirements conflict with the current state,
the material must not be added until the licensing decision is resolved.

## Command ownership

The root `pyproject.toml` owns Python metadata and dependencies, not repository task aliases. The
standard `[project.scripts]` table declares installed Python console entry points whose values are
Python object references; uv therefore requires the project to define a build system before those
entry points can be installed. This repository does not introduce a Python package and build backend
solely to wrap `agentskills`. Declarative repository commands instead belong to mise tasks: trivial
commands and dependency-only aggregates live in `mise.toml`, while non-trivial adapters remain mise
file tasks.

File tasks are thin executable adapters. They resolve the repository root independently of the
caller's working directory, use portable POSIX shell where practical, and orchestrate locked tools
without reimplementing their validation semantics. `skills-check` has exactly two invocation states:
without arguments it validates every Plugin-owned Skill in stable path order and fails when the
collection is empty; with changed-path arguments it validates the unique remaining owning Skill
roots and succeeds without work when none remain.

The resulting ownership is explicit: `pyproject.toml` and `uv.lock` pin `skills-ref`,
`mise-tasks/skills-check` owns its repository invocation, and `hk.pkl` owns Git event and file
selection policy. The `hooks-install` task invokes hk with its `--mise` option, so hook execution
resolves the pinned tool environment without depending on interactive shell activation.

## Validation

`mise run format-check`, `mise run prose-check`, and `mise run skills-check` are independent
read-only gates. The executable mise task enumerates every Plugin-owned Skill when called without
arguments; hk passes only staged paths under Skill roots during pre-commit. Both paths invoke the
locked official Agent Skills reference CLI. Cross-product directory, ownership, catalog, manifest,
and licensing-state rules are architecture review contracts owned by
`.agents/plugins/ARCHITECTURE.md`; no repository-specific marketplace validator enforces them. Codex
and Claude product validators remain release checks documented in `.agents/plugins/ARCHITECTURE.md`.

## Official references

- [pyproject.toml `[project.scripts]` specification](https://packaging.python.org/en/latest/specifications/pyproject-toml/#entry-points)
- [uv project configuration and build-system requirement](https://docs.astral.sh/uv/concepts/projects/config/#project-packaging)
- [hk configuration](https://hk.jdx.dev/configuration.html)
- [hk and mise integration](https://hk.jdx.dev/mise_integration.html)
- [mise TOML tasks](https://mise.jdx.dev/tasks/toml-tasks.html)
- [mise file tasks](https://mise.jdx.dev/tasks/file-tasks.html)
- [uv dependency groups](https://docs.astral.sh/uv/concepts/projects/dependencies/#dependency-groups)
- [Vale `.vale.ini` and `StylesPath`](https://vale.sh/docs/vale-ini)
- [Vale styles and rule layout](https://vale.sh/docs/styles)
- [Vale `BasedOnStyles`](https://vale.sh/docs/keys/basedonstyles)
- [dprint JSON Plugin](https://dprint.dev/plugins/json/)
- [dprint configuration and plugin associations](https://dprint.dev/config/)
- [dprint Pretty YAML Plugin](https://dprint.dev/plugins/pretty_yaml/)
- [Renovate configuration options](https://docs.renovatebot.com/configuration-options/)
- [Renovate regex custom manager](https://docs.renovatebot.com/modules/manager/regex/)
- [Renovate GitHub release-attachments datasource](https://docs.renovatebot.com/modules/datasource/github-release-attachments/)
- [Agent Skills specification](https://agentskills.io/specification)
- [Claude Code Plugins reference](https://code.claude.com/docs/en/plugins-reference)
- [GitHub repository licensing guidance](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository)
