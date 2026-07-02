# Contributing

How to add skills, modify configs, and maintain agent-config.

## Adding a New Skill

### 1. Create the skill directory

```bash
mkdir skills/<skill-name>
```

### 2. Create SKILL.md

Use `shared/template_skill.md` as starting point. Follow `shared/skill-style-guide.md` for budget.

**Required structure:**

```markdown
---
name: <skill-name>
description: <one-line description>
version: <semver>
---

# <Skill Name>

<What this skill does — 1-2 sentences>

## When to use

<Trigger conditions>

## Steps

<1. Do this>
<2. Then this>
<3. Finally this>

## Guardrails

<Constraints and safety rules>
```

**Budget:** 180-450 tokens in SKILL.md body. If you need more, extract to `references/`.

### 3. Extract detail (if needed)

If SKILL.md exceeds 450 tokens:

```
skills/<skill-name>/
  SKILL.md              Condensed version (steps + guardrails)
  references/           Detailed docs
    troubleshooting.md
    examples.md
    api-reference.md
```

### 4. Regenerate registry

```bash
python tools/skill_catalog.py --scan skills/ --active-agent-config skills/ --update-registry .config/skill-registry.md
```

### 5. Commit

```bash
git add skills/<skill-name>/ .config/skill-registry.md
git commit -m "feat(skills): add <skill-name>"
```

## Modifying Agent Config

### Rules

1. **Universal changes** → edit `agents/base.md`
2. **Platform-specific changes** → edit the platform file (e.g., `agents/gemini-cli.md`)
3. **Never duplicate** — if it applies to all agents, it goes in base.md only
4. **Entry points stay thin** — AGENTS.md, CLAUDE.md, GEMINI.md should be ~25 lines max

### Testing Changes

After modifying agent configs, verify:

1. Each entry point still points to `agents/base.md`
2. No broken references (grep for old paths)
3. Skills still load correctly
4. Governance protocol still triggers on failure

## Modifying Shared Documents

Shared docs (`shared/`) are reference documents, not loaded into LLM context.

| Document | Who maintains it |
|----------|-----------------|
| `VISION.md` | Human only |
| `audit-framework.md` | Human + audit triggers |
| `skill-style-guide.md` | When skill standards change |
| `trigger-rules.md` | When trigger system changes |
| `routing.md` | When model assignments change |
| `distillation-protocol.md` | When extraction rules change |

**Sync rule:** If you update `shared/` in agent-config, also sync to `D:\Engram_SDD\shared\` (or vice versa). Dual maintenance causes drift.

## Updating the Skill Registry

The registry is auto-generated. Never edit `.config/skill-registry.md` manually.

```bash
# Full rebuild
python tools/skill_catalog.py --scan skills/ --active-agent-config skills/ --update-registry .config/skill-registry.md

# Dry run (check without writing)
python tools/skill_catalog.py --scan skills/ --active-agent-config skills/
```

## Versioning

Follow semver for all versioned files:

| Component | Current | How to bump |
|-----------|---------|-------------|
| agents/base.md | 5.0.0 | Major changes to universal rules |
| Platform wrappers | 5.0.0 | When base.md changes |
| GOVERNANCE_PROTOCOL | 2.0.0 | Changes to delegation or failure handling |
| skill-registry | 2.1.0 | Auto-incremented on regeneration |
| Individual skills | Varies | Per skill's own versioning |

## Anti-Patterns

Don't do these:

| Anti-pattern | Correct approach |
|-------------|-----------------|
| Duplicating rules across platform files | Put universal rules in base.md only |
| Editing skill-registry.md by hand | Run skill_catalog.py |
| Putting detailed docs in SKILL.md | Extract to references/ subdirectory |
| Loading VISION.md into agent context | Keep as human reference only |
| Syncing shared/ manually | Use a script or verify both sides |

## Audit Checklist

Before merging changes, verify:

- [ ] No duplicate rules across files
- [ ] SKILL.md files under 450 tokens
- [ ] Registry regenerated after skill changes
- [ ] No broken references (grep for old paths like `.atl/`)
- [ ] Governance protocol unchanged unless intentionally modified
- [ ] Shared docs synced if modified
