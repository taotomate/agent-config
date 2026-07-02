# Load Flow

How agents discover, load, and use agent-config files.

## Startup Sequence

```
Agent starts
    │
    ▼
┌──────────────────────────┐
│ 1. Entry Point           │
│    AGENTS.md / CLAUDE.md │
│    / GEMINI.md           │
│    (~25 lines, thin)     │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│ 2. base.md               │
│    Universal rules       │
│    Behavior              │
│    Personality           │
│    Anti-filler           │
│    Engram/SDD protocol   │
│    (~250 lines)          │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│ 3. Platform overrides    │
│    claude-code.md        │
│    gemini-cli.md         │
│    antigravity.md        │
│    (25-55 lines each)    │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│ 4. Skill registry        │
│    .config/              │
│    skill-registry.md     │
│    (once per session)    │
└──────────┬───────────────┘
           │
           ▼
     Agent ready
```

## Skill Discovery

Skills are NOT loaded at startup. They are discovered via the registry and loaded on demand.

```
User says something
    │
    ▼
Agent checks trigger phrases in skill-registry.md
    │
    ├── Match found? → Load skills/<name>/SKILL.md
    │
    └── No match? → Continue without skill
```

### Trigger Types (from shared/trigger-rules.md)

| Type | Behavior | Example |
|------|----------|---------|
| **Advisory** | Suggests skill, asks user | "I could use the auditor skill for this" |
| **Strong** | Loads automatically when context matches | SDD phases load by workflow position |
| **Strongest** | Loads immediately, no question | Governance on failure |

### Registry Format

```markdown
| Trigger | Skill | Path |
|---------|-------|------|
| Set up and use 1Password CLI | 1password | `skills/1password/SKILL.md` |
| Build fully-integrated 3-statement models | 3-statement-model | `skills/3-statement-model/SKILL.md` |
```

The trigger column is a phrase. When the agent's context contains words matching the trigger, it considers loading that skill.

## On-Demand Loads

These files are NOT part of the startup sequence. They load only when needed:

| File | When it loads |
|------|---------------|
| `skills/*/SKILL.md` | When trigger in registry matches current context |
| `.config/GOVERNANCE_PROTOCOL.md` | On ANY error, or before creating a sub-agent |
| `shared/audit-framework.md` | When running a self-audit |
| `shared/routing.md` | When deciding model assignment |
| `shared/VISION.md` | Never by agents (human reference only) |

## Governance Load

```
Error occurs
    │
    ▼
┌──────────────────────────┐
│ Load GOVERNANCE_PROTOCOL │
│                          │
│ 1. Delegation checklist  │
│ 2. Anti-pattern check    │
│ 3. Black Box Protocol:   │
│    Freeze → Snapshot     │
│    → Recovery            │
└──────────────────────────┘
```

## Context Budget

Each loaded file consumes context window tokens. The system is designed to minimize this:

| Component | Approximate tokens |
|-----------|-------------------|
| Entry point | ~100 |
| base.md | ~1,000 |
| Platform override | ~200 |
| Skill registry (headers only) | ~200 |
| One SKILL.md | ~300-600 |
| Governance protocol | ~400 |
| **Total startup** | **~1,500** |
| **With one skill** | **~1,800-2,100** |

This is why skills are loaded on demand, not all at startup.

## Platform Differences

### MiMoCode
- Reads `AGENTS.md` from project root
- Loads `agents/base.md` via inheritance
- Discovers skills from `.config/skill-registry.md`

### Claude Code
- Reads `CLAUDE.md` from project root
- Loads `agents/base.md` + `agents/claude-code.md`
- Claude-specific overrides apply after base rules

### Gemini CLI
- Reads `GEMINI.md` from project root
- Loads `agents/base.md` + `agents/gemini-cli.md`
- Has extra anti-verbose/anti-filler rules (4 behavioral overrides)

### Antigravity
- Reads from config directory (not project root)
- Loads `agents/base.md` + `agents/antigravity.md`
- Mission Control specifics
