# Monorepo and Workspace Layout

A design lens for making project topology understandable through directory conventions and
verifiable through workspace and build metadata.

## Status

This reference defines a design pattern for monorepo and workspace layout. Its five topology axes,
decision flow, and defaults are design recommendations, not an ecosystem standard or a measured
claim that one layout always reduces cognitive load.

Official examples, recommendations, and mechanisms are identified separately below. Source IDs link
to primary references in the source register; the register states exactly what each supports. An
example directory name is not a mandatory tool constraint.

## When to Apply

Use this pattern when choosing workspace member locations, reviewing a monorepo structure,
distinguishing `apps/`, `packages/`, `crates/`, and `src/`, or planning a repository reorganization.
It does not select a build tool, require a monorepo, or replace language-specific package rules.

## Core Thesis

Choose the aspects of project topology that the filesystem should communicate. Use manifests, build
definitions, and dependency graphs to declare or infer the machine-readable relationships and verify
that they agree with the documented directory meanings.

Directory placement alone does not enforce dependency direction, publication, deployment, ownership,
or architectural isolation. Those require the corresponding metadata and checks.

## Five Topology Axes

| Axis            | Question                                                  | Example                                           | Limitation                                                                                          |
| --------------- | --------------------------------------------------------- | ------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| Boundary        | Where does a project or build unit begin?                 | A package manifest or Bazel `BUILD` file          | Different tools define different units; a package and a build target are not interchangeable.       |
| Unit Kind       | What kind of unit or artifact is collected?               | `packages/`, `crates/`, `src/`, `tests/`, `docs/` | `src/` contains source files in many layouts; it need not contain workspace members.                |
| Role / Taxonomy | What does the unit do?                                    | `apps/`, `libs/`, `services/`, `tools/`           | Names need a repository-local definition. An Elixir application need not be independently deployed. |
| Domain / Scope  | What business capability or ownership area does it serve? | `commerce/cart/`, `identity/auth/`                | A grouping directory need not itself be a project.                                                  |
| Relationship    | Which units depend on or consume others?                  | Manifest dependencies and build graph edges       | A directory tree cannot represent every graph edge.                                                 |

These axes are an analytical vocabulary for this pattern. For concrete boundary examples, Cargo uses
member directories containing `Cargo.toml` [S07]; Bazel packages are rooted at `BUILD` or
`BUILD.bazel` files and contain targets [S14].

### Resolve the Meaning of `packages/`

`packages/` can collect all workspace units, including applications, or mean reusable units paired
with `apps/`. Declare which meaning the repository uses. Likewise, `crates/` expresses a Rust
package grouping without distinguishing binary and library roles; a Cargo workspace member is a
package, not necessarily a single crate.

Do not infer deployability solely from the directory name. Inspect entry points, build targets,
publication configuration, and deployment configuration before recommending a move.

## Two Layout Strategies

The following names describe design choices, not mutually exclusive classes of tools.

**Workspace-first:** choose visible member containers and configure membership to match them.

```text
repo/
├── packages/
│   ├── core/
│   └── cli/
└── workspace manifest
```

**Repository-first:** retain a useful existing or domain-oriented topology and describe its units
with metadata at the appropriate locations.

```text
repo/
├── commerce/
│   └── checkout/
│       └── BUILD
└── tools/
    └── release/
        └── BUILD
```

Both need conventions. Cargo member paths [S07], Gradle project descriptors [S11], Go workspace
paths [S10], and build targets [S14], [S15] demonstrate mechanisms for expressing topology; their
existence does not dictate which human-facing taxonomy to choose.

Metadata-based mapping can be a primary design in a new repository as well as a migration aid. Do
not characterize Bazel or Pants as merely escape hatches. In this pattern, the reason to use
flexibility is a concrete requirement, such as preserving useful language conventions or expressing
domain boundaries, rather than flexibility for its own sake.

## Verified Ecosystem Examples and Mechanisms

This table describes the linked documentation, not the prevalence of layouts across the ecosystem.

| Ecosystem  | Documented layout or mechanism                                                                                                    | Evidence category and interpretation                                                           |
| ---------- | --------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| npm        | `workspaces` lists a `packages/a` member. [S01]                                                                                   | Official example; `packages/` is not established as mandatory.                                 |
| Yarn       | Root `workspaces` uses relative glob patterns, illustrated with `packages/*`. [S02]                                               | Documented mechanism and example.                                                              |
| pnpm       | `pnpm-workspace.yaml` selects locations with patterns, including `packages/*`, `components/**`, and exclusions. [S03]             | Documented mechanism; supported by pnpm does not mean supported by every consuming build tool. |
| Turborepo  | Its repository guidance uses `apps/*` and `packages/*`, allows explicit grouping patterns, and warns against `packages/**`. [S04] | Maintainer guidance; verify grouping with the selected package manager and Turbo version.      |
| Nx         | Describes a flat `packages/` layout and a grouped `apps/` + `libs/` layout; recommends scope-based library grouping. [S05]        | Official design guidance, not a requirement to reorganize every Nx repository.                 |
| uv         | Workspace example includes a root project and `packages/*`; members can be applications or libraries. [S06]                       | Official example and membership rules.                                                         |
| Cargo      | `members` accepts paths and globs, with `crates/*` among its examples. [S07]                                                      | Official example, not a universal `crates/` convention or requirement.                         |
| Dart Pub   | Official workspace example groups packages under `packages/`; root metadata selects them. [S08]                                   | Official example; glob support is version-dependent (documented for Dart 3.11+).               |
| Elixir Mix | `mix new --umbrella` example creates child applications under `apps/`. [S09]                                                      | Generator convention, not a universal deployable-versus-library distinction.                   |
| Go         | `go.work` uses module directories, illustrated by `./hello` and `./example/hello`. [S10]                                          | Multi-module development composition; does not imply a required monorepo container.            |
| Gradle     | Shows sibling subprojects, maps project paths to directories by default, and permits `projectDir` overrides. [S11]                | Default mapping plus explicit configuration.                                                   |
| Maven      | Aggregator POM modules are relative paths to project directories or POM files. [S12]                                              | Documented aggregation mechanism, not a mandated container name.                               |
| .NET       | Official testing tutorial places a library and its test project in sibling directories and adds both to a solution. [S13]         | Official example; it does not establish `src/` + `tests/` as a universal .NET layout.          |
| Bazel      | `BUILD` / `BUILD.bazel` establishes package boundaries; packages contain targets. [S14]                                           | Tool semantics; domain and role folder names remain design choices.                            |
| Pants      | `BUILD` files define addressable targets, including sources, tests, and executable artifacts. [S15]                               | Tool semantics; do not assume Bazel's package-boundary rules also apply to Pants.              |

## Decision Flow

1. **Inventory actual units and constraints.** Identify member discovery rules, language boundaries,
   generated directories, deployment units, publishing units, ownership, and existing consumers of
   paths. Distinguish repository membership from workspace membership.
2. **Start with the fewest meaningful axes.** If units have similar roles and remain easy to scan,
   one container such as `packages/` or a Rust-specific `crates/` can be enough. These are choices,
   not tool requirements.
3. **Add role grouping when it answers a real navigation question.** If deployable entry points and
   reusable units need to be distinguished, consider `apps/` plus `packages/` or `libs/`. Define
   where test support, tooling, and mixed-role units belong.
4. **Add domain or scope when related changes and ownership justify it.** For example,
   `packages/commerce/cart/` groups by business capability. Nx explicitly recommends grouping by
   scope [S05]; applying that recommendation to other tools is this pattern's synthesis.
5. **Preserve useful existing topology.** Evaluate relocation costs against the navigation benefit.
   An existing language convention or deliberate domain structure can justify explicit mappings.
6. **Validate the chosen topology.** Confirm that actual discovered members, build targets,
   dependency edges, and deployment/publication configuration agree with the proposed meanings. Use
   the project's supported tooling rather than treating a plausible directory tree as proof.

### Example: Role and Domain Together

```text
repo/
├── apps/
│   ├── web/
│   └── desktop/
├── packages/
│   ├── commerce/
│   │   ├── cart/
│   │   └── checkout/
│   └── identity/
│       └── auth/
└── tools/
```

This is a conceptual example, not a portable workspace configuration. Define whether `tools/`
contains members or standalone scripts. Keep grouping directories distinct from actual packages.
Configure every intended membership path explicitly or with supported globs. For Turborepo, its
maintainer guidance illustrates grouped paths such as `packages/features/*` and discourages
recursive `**` workspace patterns [S04]; do not copy pnpm's recursive-glob example blindly.

## Defaults and Tradeoffs

For a new repository without a contrary constraint, this pattern recommends choosing and documenting
a simple convention first, adding role or domain axes only when they communicate useful differences.
Metadata should make discovery and relationships precise; it should not be expected to explain all
organizational meaning without a convention.

This is a conditional design recommendation. Deeper grouping adds navigation and configuration
overhead; a flat directory may become difficult to scan; moving units can break path consumers.
Folder-based ownership can also become stale after team changes. Record which tradeoff motivates the
current choice and what evidence would justify revisiting it.

“Convention plus explicit metadata plus flexibility” is a useful synthesis of these examples, not a
sourced historical claim that convention over configuration has changed universally.

## Review Checklist

- [ ] Can a reader locate likely workspace units from the documented layout?
- [ ] Are grouping directories and actual project/package boundaries distinguishable?
- [ ] Are unit kind, source/test artifacts, role, and domain classified deliberately?
- [ ] Does `packages/` unambiguously mean all members or reusable units?
- [ ] Does each `apps/`, `libs/`, and `tools/` directory have one documented meaning?
- [ ] Is role or domain grouping justified by navigation, related changes, or ownership needs?
- [ ] Does the chosen tool and version support the required member paths and nesting?
- [ ] Do discovered members and dependency/build metadata agree with the intended layout?
- [ ] Are dependency restrictions enforced independently of directory names where needed?
- [ ] Is an unusual mapping or relocation supported by a concrete benefit and migration assessment?
- [ ] Are claimed requirements distinguished from official examples and local design preferences?

## Decision Template

```text
Decision: Adopt / retain / defer the proposed layout.
Context: Current units, tool versions, ownership, and migration constraints.
Axes: Boundary, unit kind, role, domain, and relationship responsibilities.
Directory meanings: Exact definitions and handling of mixed-role units.
Metadata: Member discovery, dependency declarations, and boundary checks.
Evidence: Relevant source IDs plus inspected repository paths/configuration.
Tradeoffs: Navigation benefit, configuration cost, and path compatibility.
Validation: Expected members and graph checks; unresolved evidence gaps.
```

## Source Register

Checked on **2026-09-08**. These are primary documentation or maintainer-owned source links. Nx was
also checked through Context7 (`/websites/nx_dev`). Other entries were read directly from the linked
official pages. Links to moving documentation and `main` are not immutable snapshots; recheck
version-specific behavior before making configuration changes.

| ID  | Primary source                                                                                                                                                                    | Claim supported / scope                                                                                                                                           |
| --- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| S01 | [npm CLI v11: Workspaces](https://docs.npmjs.com/cli/v11/using-npm/workspaces/#defining-workspaces)                                                                               | Explicit root `workspaces` configuration and `packages/a` example.                                                                                                |
| S02 | [Yarn: Workspaces](https://yarnpkg.com/features/workspaces#how-are-workspaces-declared)                                                                                           | Relative workspace glob patterns and `packages/*` example.                                                                                                        |
| S03 | [pnpm: Settings](https://pnpm.io/settings#packages)                                                                                                                               | Workspace package patterns, exclusions, and root inclusion.                                                                                                       |
| S04 | [Turborepo maintainer source: Repository Structure](https://github.com/vercel/turborepo/blob/main/skills/turborepo/references/best-practices/structure.md#directory-organization) | `apps/*` / `packages/*` configuration, explicit grouped paths, and warning about recursive wildcards. This is authored guidance, not a runtime source-code proof. |
| S05 | [Nx: Monorepo Folder Structure](https://nx.dev/docs/kb/folder-structure)                                                                                                          | Flat and grouped layouts and scope-based grouping advice.                                                                                                         |
| S06 | [uv: Using workspaces](https://docs.astral.sh/uv/concepts/projects/workspaces/)                                                                                                   | `packages/*` example, `pyproject.toml` membership, applications and libraries.                                                                                    |
| S07 | [Cargo Book: Workspaces](https://doc.rust-lang.org/cargo/reference/workspaces.html#the-members-and-exclude-fields)                                                                | Paths/globs, `crates/*` example, manifests, and automatic membership of in-workspace path dependencies.                                                           |
| S08 | [Dart: Pub workspaces](https://dart.dev/tools/pub/workspaces)                                                                                                                     | `packages/` example, explicit paths, glob version requirement, and nested workspace support.                                                                      |
| S09 | [Mix: mix new](https://mix.hexdocs.pm/Mix.Tasks.New.html#module-examples)                                                                                                         | Umbrella generator example and child application creation under `apps/`.                                                                                          |
| S10 | [Go: Multi-module workspace tutorial](https://go.dev/doc/tutorial/workspaces#create-the-workspace)                                                                                | `go.work` composition using module directory paths at different depths.                                                                                           |
| S11 | [Gradle: Multi-Project Builds](https://docs.gradle.org/current/userguide/multi_project_builds.html)                                                                               | Sibling/nested subprojects, default path mapping, and `projectDir` customization.                                                                                 |
| S12 | [Maven: POM Reference, Aggregation](https://maven.apache.org/pom.html#Aggregation)                                                                                                | Aggregation via relative module paths and distinction from inheritance.                                                                                           |
| S13 | [Microsoft: Unit testing C# with xUnit](https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-csharp-with-xunit#create-the-solution)                                 | Sibling library/test projects, solution membership, and a project reference example.                                                                              |
| S14 | [Bazel: Repositories, workspaces, packages, and targets](https://bazel.build/concepts/build-ref#packages)                                                                         | Package boundaries, subpackage exclusion, and targets within packages.                                                                                            |
| S15 | [Pants: Targets and BUILD files](https://www.pantsbuild.org/stable/docs/using-pants/key-concepts/targets-and-build-files)                                                         | Targets defined in `BUILD` files and path-based target addresses.                                                                                                 |

No source in this register establishes the five-axis framework, a universal repository taxonomy, or
a quantified productivity benefit. Those remain the explicitly labeled design synthesis above.

[S01]: https://docs.npmjs.com/cli/v11/using-npm/workspaces/#defining-workspaces
[S02]: https://yarnpkg.com/features/workspaces#how-are-workspaces-declared
[S03]: https://pnpm.io/settings#packages
[S04]: https://github.com/vercel/turborepo/blob/main/skills/turborepo/references/best-practices/structure.md#directory-organization
[S05]: https://nx.dev/docs/kb/folder-structure
[S06]: https://docs.astral.sh/uv/concepts/projects/workspaces/
[S07]: https://doc.rust-lang.org/cargo/reference/workspaces.html#the-members-and-exclude-fields
[S08]: https://dart.dev/tools/pub/workspaces
[S09]: https://mix.hexdocs.pm/Mix.Tasks.New.html#module-examples
[S10]: https://go.dev/doc/tutorial/workspaces#create-the-workspace
[S11]: https://docs.gradle.org/current/userguide/multi_project_builds.html
[S12]: https://maven.apache.org/pom.html#Aggregation
[S13]: https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-csharp-with-xunit#create-the-solution
[S14]: https://bazel.build/concepts/build-ref#packages
[S15]: https://www.pantsbuild.org/stable/docs/using-pants/key-concepts/targets-and-build-files
