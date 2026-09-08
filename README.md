# Agent Marketplace

A personal marketplace for Agent Skills and tools, currently offering reusable Skills for Claude
Code and Codex.

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

Replace `workflow-tooling` with any Plugin listed above. Start a new session after installation so
the product discovers the bundled Skills.

## Architecture pattern migration

`architecture-pattern-application` is now owned by `software-architecture`. It replaces
`web-engineering:web-architecture-pattern-application` and includes both route-state product
analytics and monorepo workspace layout. Install `software-architecture` to use these patterns;
update explicit invocations to `software-architecture:architecture-pattern-application`.
