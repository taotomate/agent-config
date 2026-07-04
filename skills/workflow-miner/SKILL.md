---
name: workflow-miner
description: "Discover repeated workflows and package them into reusable skills, subagents, or commands. Self-improvement through automation."
version: 1.1.0
author: TaoTomate
generator_model: mimo-auto
inherited_from: mimocode/distill + custom extensions
---

# Workflow-Miner — Workflow Discovery & Skill Creation

## When to Use

- When you notice the same steps repeated across sessions
- After completing a complex workflow manually
- When a task pattern emerges that could be automated
- Periodically to identify automation opportunities

## Purpose

Distill analyzes recent work and:
1. **Discovers** repeated manual workflows
2. **Evaluates** automation potential
3. **Packages** high-confidence candidates into skills
4. **Creates** reusable commands or subagents

## Workflow

### 1. Scan Recent Work

```
Scope: ALL available session history (cumulative, not just recent)
Sources:
- Conversation history (tool calls, sequences)
- Task completions
- Manual steps the user guided
- Workarounds or repeated corrections
- MEMORY.md patterns (already documented)
- Notes (scratch observations)

Counting: Accumulative across ALL sessions, not per-week.
If a pattern occurred 2 times in January and 3 times in March = 5 total.
```

### 2. Identify Patterns

Look for:

| Pattern Type | Signal | Example |
|--------------|--------|---------|
| Repeated sequence | Same 3+ steps in multiple sessions | "Always: read config → update version → commit" |
| Manual guidance | User repeats same instructions | "You always need to check X before Y" |
| Correction loop | User fixes same mistake repeatedly | "Don't forget to run tests first" |
| Tool chain | Same tools invoked in order | "git status → git add → git commit" |

### 3. Evaluate Automation Potential

For each pattern, assess:

| Criterion | Weight | Question |
|-----------|--------|----------|
| Frequency | 3x | How often does this occur? |
| Complexity | 2x | How many steps? |
| Error-prone | 2x | Does it often go wrong? |
| Time-consuming | 1x | How long does it take? |
| Standardizable | 1x | Is the workflow consistent? |

**Score**: Sum of weighted criteria. Threshold: 8+ for skill creation.

### 4. Classify Output Type

| Score | Output |
|-------|--------|
| 8-10 | Skill (full SKILL.md with workflow) |
| 5-7 | Command (reusable prompt template) |
| 3-4 | Note (document for future reference) |
| <3 | Skip (not worth automating) |

### 5. Create Artifact

#### For Skills (score 8+):
```
skills/{skill-name}/
├── SKILL.md           # Main instructions
└── references/        # Supporting docs
```

#### For Commands (score 5-7):
Add to `.config/commands.json`:
```json
{
  "{command-name}": {
    "template": "{workflow steps}",
    "description": "{what it does}",
    "agent": "build"
  }
}
```

#### For Notes (score 3-4):
Add to `shared/patterns.md`:
```markdown
## {Pattern Name}
- Frequency: {how often}
- Steps: {list}
- Automation potential: {low/medium/high}
```

### 6. Report

```markdown
## Distill Report

### Patterns Discovered
| Pattern | Frequency | Score | Output |
|---------|-----------|-------|--------|
| ... | ... | ... | skill/command/note |

### Created
- [N] new skills
- [N] new commands
- [N] patterns documented

### Recommendations
- [Actionable suggestion]
```

## Quality Gates

Before creating a skill, verify:

- [ ] Pattern occurs 3+ times
- [ ] Steps are deterministic (not ambiguous)
- [ ] No existing skill covers this
- [ ] Workflow is platform-agnostic
- [ ] Steps can be documented clearly

## Anti-Patterns

- DO NOT create skills for one-off tasks
- DO NOT duplicate existing skills
- DO NOT create overly specific skills
- DO NOT skip the scoring step
- DO NOT create skills during active work (defer)

## Integration

### With Dream
- Dream extracts knowledge → Distill extracts workflows
- Both contribute to MEMORY.md

### With SDD
- Distill findings can become SDD proposals
- Complex workflows → sdd-apply phases

### With Skill Registry
- New skills auto-register via `skill_catalog.py`
- Registry stays in sync automatically
