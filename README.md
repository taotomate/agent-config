---
name: agent-config-readme
description: Load map, structure guide, and installation instructions for the agent configuration system.
version: 5.3.0
author: TaoTomate
generator_model: mimo-auto
inherited_from: custom
---

# agent-config

Source of truth for AI agent configuration. One system, many platforms.

## Quick Install (new environment)

```bash
# 1. Clone this repo
git clone <your-repo-url> agent-config

# 2. For OpenCode — read the README and follow install instructions
#    Tell OpenCode: "Read https://github.com/taotomate/agent-config/blob/main/README.md
#    and follow the install instructions for my platform"

# 3. For MiMoCode — done. It reads AGENTS.md automatically.
#    Just open a project inside or symlink AGENTS.md to the project root.

# 4. For Claude Code — symlink or copy CLAUDE.md to your project root
cp agent-config/CLAUDE.md /path/to/your/project/CLAUDE.md

# 5. For Gemini CLI — symlink or copy GEMINI.md to your project root
cp agent-config/GEMINI.md /path/to/your/project/GEMINI.md

# 6. For Antigravity — copy agents/antigravity.md to your antigravity config dir
#    (check your Antigravity docs for the expected path)
```

### What each agent reads

| Agent | Reads | Then loads |
|-------|-------|------------|
| OpenCode | `AGENTS.md` (root) | `agents/base.md` |
| MiMoCode | `AGENTS.md` (root) | `agents/base.md` |
| Claude Code | `CLAUDE.md` (root) | `agents/base.md` + `agents/claude-code.md` |
| Gemini CLI | `GEMINI.md` (root) | `agents/base.md` + `agents/gemini-cli.md` |
| Antigravity | Config dir | `agents/base.md` + `agents/antigravity.md` |

### After install

- Skills are in `skills/` — the agent discovers them via `.config/skill-registry.md`
- Governance is in `.config/GOVERNANCE_PROTOCOL.md` — loaded on failure or delegation
- VISION.md is human reference only — agents do NOT load it

## Agent Self-Configuration

When an agent reads this README, it should configure itself to use the full agent-config structure.

### Base path

All references resolve from: ``

### Required files (always loaded)

| File | Path | Purpose |
|------|------|---------|
| Entry point | `AGENTS.md` in project root | Thin wrapper, inherits from base |
| Source of Truth | `agents/base.md` | Universal rules, behavior, personality, SDD, engram |

### Skill discovery

| File | Path | Purpose |
|------|------|---------|
| Skill registry | `.config/skill-registry.md` | Maps triggers → skill paths (375 skills) |
| Skills directory | `skills/*/SKILL.md` | Individual skill definitions |

### On-demand files

| File | Path | When to load |
|------|------|--------------|
| Governance | `.config/GOVERNANCE_PROTOCOL.md` | On ANY error, or before creating sub-agents |
| Audit framework | `shared/audit-framework.md` | When running self-audit |
| Routing | `shared/routing.md` | When deciding model assignment |
| Style guide | `shared/skill-style-guide.md` | When creating/refactoring skills |
| SDD common | `shared/sdd-phase-common.md` | When executing SDD phases |

### Platform overrides (optional)

| File | Path | When to load |
|------|------|--------------|
| Claude Code | `agents/claude-code.md` | Only if platform is Claude Code |
| Gemini CLI | `agents/gemini-cli.md` | Only if platform is Gemini CLI |
| Antigravity | `agents/antigravity.md` | Only if platform is Antigravity |

### Full directory tree

```

├── AGENTS.md                    # MiMoCode/OpenCode entry point
├── CLAUDE.md                    # Claude Code entry point
├── GEMINI.md                    # Gemini CLI entry point
├── README.md                    # This file
├── CHANGELOG.md                 # Version history
├── skills-report.md             # Auto-generated skill catalog
├── sync-agent-config.bat        # Sync script for projects
│
├── agents/
│   ├── base.md                  # SOURCE OF TRUTH — load this
│   ├── claude-code.md           # Platform override
│   ├── gemini-cli.md            # Platform override
│   └── antigravity.md           # Platform override
│
├── shared/
│   ├── VISION.md                # Human reference only
│   ├── routing.md               # Model routing rules
│   ├── audit-framework.md       # 7 axioms for auditing
│   ├── skill-style-guide.md     # SKILL.md standards
│   ├── sdd-phase-common.md      # SDD protocol
│   └── skill-resolver.md        # Skill injection protocol
│
├── skills/                      # 375 skills — load on trigger
│   └── */SKILL.md
│
├── .config/
│   ├── skill-registry.md        # Skill index — load once per session
│   ├── GOVERNANCE_PROTOCOL.md   # Failure handling — load on error
│   └── error_log.md             # Runtime errors
│
├── tools/
│   └── skill_catalog.py         # Registry generator
│
├── docs/                        # Human reference only
│   ├── architecture.md
│   ├── components.md
│   ├── load-flow.md
│   └── contributing.md
│
├── hermes-profiles/             # Hermes worker profiles
│
└── backups/                     # Config snapshots
```

### Agent config template

For agents that support configuration files:

```yaml
# opencode.json / .claude/config.yaml / etc.
agent_config:
  base_path: "<path-to-your-agent-config-clone>"
  source_of_truth: "agents/base.md"
  skill_registry: ".config/skill-registry.md"
  governance: ".config/GOVERNANCE_PROTOCOL.md"
  skills_path: "skills/"
  shared_path: "shared/"
  inherit: true  # Load base.md via AGENTS.md inheritance
```

### Verification

Ask the agent: "What is your configuration source?" — it should reference `agents/base.md` from your local clone.

## Load Map

### Automatic (always loaded)

| File | Loaded by | Purpose |
|------|-----------|---------|
| `AGENTS.md` | OpenCode, MiMoCode | Entry point |
| `CLAUDE.md` | Claude Code | Entry point |
| `GEMINI.md` | Gemini CLI | Entry point |
| `agents/base.md` | All agents | Universal rules, behavior, SDD |

### By platform

| File | Platform | Purpose |
|------|----------|---------|
| `agents/claude-code.md` | Claude Code | Claude-specific overrides |
| `agents/gemini-cli.md` | Gemini CLI | Gemini-specific overrides |
| `agents/antigravity.md` | Antigravity | Mission Control specifics |

### By trigger (on demand)

| Path | When |
|------|------|
| `skills/*/SKILL.md` | When trigger in `.config/skill-registry.md` matches |
| `.config/GOVERNANCE_PROTOCOL.md` | On failure or before delegating |
| `.config/skill-registry.md` | Once per session at startup |

### Reference only (not loaded into LLM)

| File | Purpose |
|------|---------|
| `shared/VISION.md` | Philosophy and historical context |
| `shared/routing.md` | Model assignment by layer |
| `shared/audit-framework.md` | How to audit this system |
| `shared/skill-style-guide.md` | Standards for writing SKILL.md files (body budget, structure, quality gates) |
| `shared/sdd-phase-common.md` | SDD common protocol (loaded by 9 SDD skills) |
| `shared/skill-resolver.md` | Skill resolution protocol (loaded by judgment-day) |

### Documentation (human reference only)

| File | Purpose |
|------|---------|
| `docs/trigger-rules.md` | 3-tier trigger system (advisory/strong/strongest) |
| `docs/persistence-contract.md` | SDD persistence modes (engram/openspec/hybrid/none) |
| `docs/engram-convention.md` | Engram naming rules |
| `docs/openspec-convention.md` | OpenSpec structure |
| `docs/validation-framework.md` | Validation patterns for skills |
| `docs/distillation-protocol.md` | How to extract decisions from sessions |
| `docs/template_skill.md` | Template for new skills |

## Versioning

Versions read from actual file frontmatters on the `main` branch.

| Component | Version | Last updated |
|-----------|---------|-------------|
| agents/base.md | 5.3.0 | 2026-07-17 |
| agents/claude-code.md | 5.3.0 | 2026-07-17 |
| agents/gemini-cli.md | 5.3.0 | 2026-07-17 |
| agents/antigravity.md | 5.3.0 | 2026-07-17 |
| Entry points (CLAUDE/GEMINI/AGENTS) | 5.3.0 | 2026-07-17 |
| GOVERNANCE_PROTOCOL | 3.0.0 | 2026-07-04 |
| skill-registry | 2.1.0 | 2026-07-06 |
| shared/VISION.md | 3.2 | 2026-06-03 |
| shared/routing.md | 2.1 | 2026-06-23 |
| shared/skill-resolver.md | 1.0.0 | 2026-07-04 |
| shared/audit-framework.md | 1.0.0 | 2026-07-04 |
| shared/sdd-phase-common.md | unversioned | 2026-07-04 |
| shared/skill-style-guide.md | unversioned | 2026-07-04 |

## How to audit and maintain

When something changes, the self-audit triggers in `agents/base.md` fire automatically.

### Update skill registry (auto)

After adding/removing skills, regenerate the registry:

```bash
python tools/skill_catalog.py --scan skills/ --active-agent-config skills/ --update-registry .config/skill-registry.md
```

This scans all skills, deduplicates, and writes `.config/skill-registry.md` in one pass.

### Manual audit

```bash
python tools/skill_catalog.py --scan skills/ --active-agent-config skills/
```

Or load `shared/audit-framework.md` and check the 7 axioms:
Consistency, Economy, Traceability, Correctness, Completeness, Degradability, Evolvibility.

## Documentation

Detailed guides in `docs/`:

| Document | Purpose |
|----------|---------|
| `docs/architecture.md` | How the system fits together — layer model, data flow, key relationships |
| `docs/components.md` | Reference for every file and directory — what each does, who loads it |
| `docs/load-flow.md` | How agents discover and load configs — startup sequence, skill discovery, context budget |
| `docs/contributing.md` | How to add skills, modify configs, maintain the system |