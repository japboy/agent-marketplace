# Agent Marketplace Architecture

This document owns repository-level architecture. Plugin package invariants are owned by
`.agents/plugins/ARCHITECTURE.md`.

## Purpose

The repository distributes the same physical Agent Skills to Claude Code and Codex. A Plugin
directory is the package, installation, versioning, and source of truth boundary. Product catalogs
and manifests describe that boundary but do not duplicate its Skill files. APM provides an
additional installation route using the same packages. Root `apm.yml` owns the marketplace
definition.

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
├── apm.yml                             # APM producer and catalog source of truth
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
apm.yml ── apm pack ─┬─ .agents/plugins/marketplace.json
                     └─ .claude-plugin/marketplace.json
                                  │
                                  └─ .agents/plugins/<plugin>/
                                       ├─ .codex-plugin/plugin.json
                                       ├─ .claude-plugin/plugin.json
                                       └─ skills/*
```

APM generates both catalogs from the ordered `marketplace.packages` declarations in `apm.yml`. Both
catalogs resolve their sources from the repository root and point to the same
`./.agents/plugins/<plugin>` directories. Installed products copy or cache those self-contained
directories; no installed Plugin depends on a path outside its own root.

```text
Repository Markdown/JSON/YAML ── dprint check/fmt ── structural state
Repository Markdown ───────────── Vale check ─────── prose policy
Plugin-owned SKILL.md ── skills-ref ───────── Agent Skills format
Plugin topology ──────── architecture review ─ package ownership contract
apm.yml ──────────────── apm pack --check-clean ─ generated catalog consistency
Generated catalog ────── isolated APM install ── Skill deployment and frozen replay
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
- Root `apm.yml` is the source of truth for marketplace identity, publisher, ordering, source paths,
  categories, and tags. Catalog JSON files are committed outputs of the pinned APM generator.
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
  its Aqua backend verifies upstream release checksums. APM uses mise's GitHub backend and its
  upstream release checksum verification. uv resolves `skills-ref` from the root development
  dependency group and lockfile. CI, hooks, and local commands use the same state.
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

`mise run format-check`, `mise run prose-check`, `mise run skills-check`, `mise run
marketplace-check`, and `mise run apm-test` are independent read-only gates. The executable mise
task enumerates every Plugin-owned Skill when called without arguments; hk passes only staged paths
under Skill roots during pre-commit. Both paths invoke the locked official Agent Skills reference
CLI. Cross-product directory, ownership, catalog, manifest, and licensing-state rules are
architecture review contracts owned by `.agents/plugins/ARCHITECTURE.md`; the repository does not
reimplement product schema validation. APM catalog drift and installation checks are automated.
Codex and Claude product validators remain release checks documented in
`.agents/plugins/ARCHITECTURE.md`.

## APM distribution

`apm.yml` is a producer manifest with a `marketplace:` block, not a consumer dependency aggregator.
Each local package source points to the existing Plugin root. No `.apm/` copy, per-Plugin APM
manifest, or dependency on this repository itself is required. Consumer manifests and lockfiles
remain in consuming projects; running `apm install` in this producer is not the authoring workflow.

`mise run marketplace-build` invokes the pinned APM 0.30.0 `apm pack --offline`. The official Claude
and Codex output profiles own serialization and product defaults. `mise run marketplace-check` uses
the native `--check-clean` gate to regenerate in memory and detect semantic JSON drift without
writing. dprint owns the committed formatting. Generation requires no network resolution because all
catalog sources are local. YAML anchors share the marketplace version and description between
package-level metadata and the explicit marketplace overrides needed to emit them in Claude JSON.

The native generator intentionally changes these presentation details from the hand-authored
catalogs:

- Codex `interface.displayName` equals `agent-marketplace`; the installed marketplace identifier
  remains `agent-marketplace`. APM does not support an independent display-name override.
- Claude catalog `$schema` and explicit `strict: true` are omitted. Claude's documented default is
  `strict: true`, so Plugin manifests retain authority for their component definitions.
- Plugin ordering, source paths, categories, Claude tags, and Codex `AVAILABLE` / `ON_INSTALL`
  policies are preserved. Individual Plugin versions remain owned by their manifests.

The APM integration gate copies the producer into a temporary directory and reads its generated
catalog to install every local package source in a separate consumer. It installs every entry for
Claude and Codex, compares each Skill's files with the source bytes, and repeats installation with
`--frozen`. No Skill scripts are executed. The test avoids `marketplace add`, which APM 0.30.0
writes to the user-level marketplace registry even when `APM_HOME` is set. Named marketplace
resolution was checked separately during migration. This proves packaging and deployment, not
successful execution of every Skill or support for other agent runtimes. Skills use bare names in
the deployed directories, so users should avoid installing the same Skill through both APM and a
native Plugin in one project.

APM warns that the existing Claude manifest SchemaStore URI is unrecognized, then classifies the
package by its supported Claude structure. Pack also warns about absent license metadata; this is
consistent with `LicenseUndecided` and must not be silenced by inventing license terms. Neither
warning prevents the verified distribution workflow.

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
- [APM marketplace authoring](https://microsoft.github.io/apm/reference/manifest-schema/#7-marketplace-authoring-block)
- [APM pack and read-only drift checks](https://microsoft.github.io/apm/reference/cli/pack/)
- [APM output profiles](https://github.com/microsoft/apm/blob/v0.30.0/src/apm_cli/marketplace/output_profiles.py)
- [APM output mapping](https://github.com/microsoft/apm/blob/v0.30.0/src/apm_cli/marketplace/output_mappers.py)
- [Claude marketplace strict default](https://code.claude.com/docs/en/plugin-marketplaces#strict-mode)
