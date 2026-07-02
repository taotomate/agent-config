# Architecture

How agent-config works as a system.

## Design Principle

**One system, many platforms.** A single Source of Truth (`agents/base.md`) drives all AI agents. Platform files are thin overrides, not duplicates.

```
┌─────────────────────────────────────────────────┐
│                  User's Project                  │
│                                                  │
│  AGENTS.md ──┐                                  │
│  CLAUDE.md ──┤──▶ agents/base.md ◀── GEMINI.md │
│  GEMINI.md ──┘         │                        │
│                        ▼                        │
│              ┌─────────────────┐                │
│              │  Shared rules   │                │
│              │  Behavior       │                │
│              │  Personality    │                │
│              │  Anti-filler    │                │
│              │  Engram/SDD     │                │
│              └────────┬────────┘                │
│                       │                         │
│          ┌────────────┼────────────┐           │
│          ▼            ▼            ▼           │
│   claude-code.md  gemini-cli.md  antigravity.md│
│   (overrides)     (overrides)    (overrides)   │
│          │            │            │           │
│          └────────────┼────────────┘           │
│                       ▼                         │
│              ┌─────────────────┐                │
│              │  .config/       │                │
│              │  skill-registry │                │
│              │  governance     │                │
│              └────────┬────────┘                │
│                       │                         │
│                       ▼                         │
│              ┌─────────────────┐                │
│              │  skills/        │                │
│              │  370 SKILL.md   │                │
│              └─────────────────┘                │
└─────────────────────────────────────────────────┘
```

## Layer Model

The system follows a 3-layer architecture (defined in `shared/VISION.md`):

| Layer | Purpose | Files |
|-------|---------|-------|
| **L1 — Planning** | Design, architecture, complex analysis | `agents/base.md`, `shared/VISION.md`, `shared/audit-framework.md` |
| **L2 — Orchestration** | Task routing, error handling, coordination | `.config/GOVERNANCE_PROTOCOL.md`, `.config/skill-registry.md`, `agents/claude-code.md` etc. |
| **L3 — Execution** | Concrete work (scripts, code, tests) | `skills/*/SKILL.md`, `tools/skill_catalog.py`, `execution/` |

### Model Assignment by Layer

| Layer | Primary Model | Fallback |
|-------|--------------|----------|
| L1 (Planning) | Gemini Pro / Opus | Sonnet |
| L2 (Orchestration) | Gemini Flash / Sonnet | Haiku |
| L3 (Execution) | Python scripts | Local models (Ollama) |

See `shared/routing.md` for full routing rules.

## Data Flow

```
1. Agent starts
   → Reads entry point (AGENTS.md / CLAUDE.md / GEMINI.md)
   → Entry point loads agents/base.md
   → base.md loads platform-specific overrides

2. Skill discovery
   → Agent reads .config/skill-registry.md (once per session)
   → Registry maps triggers → skill paths
   → When trigger matches, agent loads skills/<name>/SKILL.md

3. Governance
   → On failure: loads .config/GOVERNANCE_PROTOCOL.md
   → Follows delegation checklist
   → Black Box Protocol: Freeze → Snapshot → Recovery

4. Audit
   → Self-audit triggers fire from base.md
   → Check against 7 axioms (shared/audit-framework.md)
   → Findings logged or escalated
```

## Key Relationships

- **base.md** is the universal config. All platforms inherit from it.
- **Platform wrappers** (claude-code.md, gemini-cli.md) only override what differs.
- **Skills** are context-triggered, not auto-loaded. The registry tells the agent which skill matches which situation.
- **Governance** is a safety net, not a workflow. It only activates on failure or delegation.
- **Audit framework** is the meta-system — it validates the configuration itself.
- **VISION.md** is philosophy for humans. Agents do NOT load it.

## Evolution

The system evolved from:
- **v4.7**: Per-platform full configs (duplicated rules, drift between platforms)
- **v5.0**: Universal base + thin wrappers (single source of truth, no drift)

See `CHANGELOG.md` for full migration details.
