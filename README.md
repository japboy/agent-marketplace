# Agent Marketplace

A dual-format marketplace that distributes one physical set of Agent Skills to Claude Code and
Codex.

## Overview

| Plugin               | Purpose                                            |
| -------------------- | -------------------------------------------------- |
| `workflow-tooling`   | Maintain and extend agent workflows                |
| `software-delivery`  | Refine plans and record delivered changes          |
| `language-quality`   | Research terminology and improve Japanese output   |
| `design-engineering` | Reconstruct design systems from evidence           |
| `web-engineering`    | Review Web implementation, tests, and architecture |

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
