---
name: agent-config-readme
description: Load map, structure guide, and installation instructions for the agent configuration system.
version: 5.0.0
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

# 2. For MiMoCode — done. It reads AGENTS.md automatically.
#    Just open a project inside or symlink AGENTS.md to the project root.

# 3. For Claude Code — symlink or copy CLAUDE.md to your project root
cp agent-config/CLAUDE.md /path/to/your/project/CLAUDE.md

# 4. For Gemini CLI — symlink or copy GEMINI.md to your project root
cp agent-config/GEMINI.md /path/to/your/project/GEMINI.md

# 5. For Antigravity — copy agents/antigravity.md to your antigravity config dir
#    (check your Antigravity docs for the expected path)
```

### What each agent reads

| Agent | Reads | Then loads |
|-------|-------|------------|
| MiMoCode | `AGENTS.md` (root) | `agents/base.md` |
| Claude Code | `CLAUDE.md` (root) | `agents/base.md` + `agents/claude-code.md` |
| Gemini CLI | `GEMINI.md` (root) | `agents/base.md` + `agents/gemini-cli.md` |
| Antigravity | Config dir | `agents/base.md` + `agents/antigravity.md` |

### After install

- Skills are in `skills/` — the agent discovers them via `.config/skill-registry.md`
- Governance is in `.config/GOVERNANCE_PROTOCOL.md` — loaded on failure or delegation
- VISION.md is human reference only — agents do NOT load it

## Load Map

### Automatic (always loaded)

| File | Loaded by | Purpose |
|------|-----------|---------|
| `AGENTS.md` | MiMoCode | Entry point |
| `CLAUDE.md` | Claude Code | Entry point |
| `GEMINI.md` | Gemini CLI | Entry point |
| `agents/base.md` | All agents | Universal rules, behavior, engram, SDD |

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
| `shared/engram-convention.md` | Engram naming rules |
| `shared/persistence-contract.md` | SDD persistence modes |
| `shared/openspec-convention.md` | OpenSpec structure |
| `shared/audit-framework.md` | How to audit this system |
| `shared/skill-style-guide.md` | Standards for writing SKILL.md files (body budget, structure, quality gates) |
| `shared/trigger-rules.md` | Documentation of the 3-tier trigger system (advisory/strong/strongest) |
| `shared/template_skill.md` | Template for new skills |

## Structure

```
agent-config/
  AGENTS.md                  MiMoCode entry point (thin)
  CLAUDE.md                  Claude Code entry point (thin)
  GEMINI.md                  Gemini CLI entry point (thin)
  README.md                  This file

  agents/
    base.md                  Source of Truth (all universal rules)
    claude-code.md           Claude-specific overrides
    gemini-cli.md            Gemini-specific overrides
    antigravity.md           Antigravity-specific overrides

  shared/
    VISION.md                Philosophy (human reference)
    routing.md               Model routing by layer
    engram-convention.md     Engram naming rules
    persistence-contract.md  SDD persistence modes
    openspec-convention.md   OpenSpec structure
    audit-framework.md       Audit framework
    template_skill.md        Skill template
    errors_learned.md        Error log

  skills/                    33+ skills (SDD, workflow, meta)
  .config/
    GOVERNANCE_PROTOCOL.md   Delegation + failure handling
    skill-registry.md        Skill index for orchestrator
    error_log.md             Runtime error log

  tools/
    skill_catalog.py         Scan, hash, deduplicate, version-track skills

  backups/                   Auto-generated config snapshots
```

## Versioning

| Component | Version | Last updated |
|-----------|---------|-------------|
| agents/base.md | 5.0.0 | 2026-07-02 |
| Entry points (CLAUDE/GEMINI/AGENTS) | 5.0.0 | 2026-07-02 |
| GOVERNANCE_PROTOCOL | 2.0.0 | 2026-07-02 |
| skill-registry | 2.1.0 | 2026-07-02 |
| skill-optimizer | 3.2.0 | 2026-07-02 |
| shared/VISION.md | 3.2 | 2026-06-03 |
| shared/routing.md | 2.1 | 2026-06-23 |

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
