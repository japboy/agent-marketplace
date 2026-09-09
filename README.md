# Agent Marketplace

A personal marketplace for Agent Skills and tools, currently offering reusable Skills for Claude
Code and Codex, including installation through Agent Package Manager (APM).

## Overview

| Plugin                  | Purpose                                            |
| ----------------------- | -------------------------------------------------- |
| `workflow-tooling`      | Maintain and extend agent workflows                |
| `software-delivery`     | Refine plans and record delivered changes          |
| `language-quality`      | Research terminology and improve Japanese output   |
| `design-engineering`    | Reconstruct design systems from evidence           |
| `web-engineering`       | Review Web implementation, tests, and architecture |
| `software-architecture` | Apply documented architecture patterns             |

## Installation

### Codex

```bash
codex plugin marketplace add japboy/agent-marketplace
codex plugin add workflow-tooling@agent-marketplace
```

### Claude Code

```bash
claude plugin marketplace add japboy/agent-marketplace
claude plugin install workflow-tooling@agent-marketplace
```

### APM

Run these commands in the consuming project with APM 0.30.0:

```bash
apm marketplace add japboy/agent-marketplace
apm install workflow-tooling@agent-marketplace --target claude,codex
```

APM reads the generated Claude-compatible catalog and installs the same physical Skills into
`.claude/skills/` and `.agents/skills/`. Select only the targets you use. Choose one installation
method for each Skill in a project to avoid duplicate discovery. APM deploys Skills by their Skill
names; native Plugin-qualified invocations are not preserved. Runtime prerequisites documented in
each Skill still apply; this distribution does not certify other agent runtimes.

Commit the consumer's `apm.yml`, `apm.lock.yaml`, and deployed Skill files. Use `apm install
--frozen` to reproduce the locked installation. These consumer artifacts do not belong in this
producer repository.

Replace `workflow-tooling` with any Plugin listed above. Start a new session after installation so
the product discovers the bundled Skills.

## Architecture pattern migration

`architecture-pattern-application` is now owned by `software-architecture`. It replaces
`web-engineering:web-architecture-pattern-application` and includes both route-state product
analytics and monorepo workspace layout. Install `software-architecture` to use these patterns;
update explicit invocations to `software-architecture:architecture-pattern-application`.

## Maintaining the marketplace

Root `apm.yml` owns the publisher metadata and ordered package catalog. Edit that file, then run:

```bash
mise run marketplace-build
mise run format
mise run check
```

Commit `apm.yml` and both generated catalogs together. Do not edit the catalog JSON files by hand.
Plugin manifests continue to own package metadata and point to their physical `skills/` directory.
APM is pinned through mise; catalog generation uses its standard offline generator.

`marketplace-check` detects catalog drift without writing files. `apm-test` installs every generated
catalog source in a temporary consumer for Claude and Codex, checks Skill contents, and replays the
lockfile. See [the distribution architecture](ARCHITECTURE.md#apm-distribution) for generator
semantics and known diagnostics.
