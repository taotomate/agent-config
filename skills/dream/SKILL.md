---
name: dream
description: "Scan session traces, extract persistent knowledge, remove outdated entries. Self-improvement through memory consolidation."
version: 1.0.0
author: TaoTomate
generator_model: mimo-auto
inherited_from: mimocode/dream + custom extensions
---

# Dream — Knowledge Extraction & Consolidation

## When to Use

- After completing a significant task or session
- When memory feels stale or cluttered
- Before starting work that builds on prior sessions
- Periodically (weekly recommended) for maintenance

## Purpose

Dream scans recent session traces and:
1. **Extracts** persistent knowledge into project memory
2. **Removes** outdated or superseded entries
3. **Consolidates** related findings into coherent blocks
4. **Promotes** patterns from notes to permanent memory

## Workflow

### 1. Scan Recent Sessions

```
Scope: Last N sessions or since last dream
Sources:
- Session checkpoints (checkpoint.md)
- Notes (notes.md)
- Task progress (tasks/*/progress.md)
- Conversation history
```

### 2. Extract Knowledge

For each session, identify:

| Type | What to Extract | Target |
|------|-----------------|--------|
| Decision | Architecture, design, tool choices | MEMORY.md → Decisions |
| Bug fix | Root cause, solution, prevention | MEMORY.md → Learnings |
| Pattern | Naming, structure, conventions | MEMORY.md → Patterns |
| Preference | User style, constraints | MEMORY.md → Preferences |
| Discovery | Non-obvious codebase insights | MEMORY.md → Discoveries |

### 3. Evaluate for Persistence

Ask for each extracted item:

- **Is this still relevant?** — Will it matter in future sessions?
- **Is this unique?** — Not already captured elsewhere?
- **Is this actionable?** — Can it guide future behavior?
- **Is this stable?** — Not likely to change soon?

If NO to any → skip or defer to notes.

### 4. Consolidate Memory

```
MEMORY.md structure:

## Rules
- [Project-specific rules]

## Architecture Decisions
- [Key decisions and rationale]

## Patterns
- [Established conventions]

## Learnings
- [Bug fixes, gotchas, insights]

## Preferences
- [User style, constraints]
```

### 5. Prune Outdated

Remove from MEMORY.md:
- Superseded decisions (replaced by newer ones)
- Temporary patterns (no longer used)
- Resolved issues (bug fixes that are now obvious)
- Stale preferences (user changed their mind)

### 6. Report

```markdown
## Dream Report

### Extracted
- [N] decisions promoted to memory
- [N] learnings captured
- [N] patterns documented

### Pruned
- [N] outdated entries removed
- [N] superseded decisions cleaned

### Updated
- MEMORY.md: [size change]
- Notes: [items cleared]
```

## Access Protocol

### Read
```
MEMORY.md — project knowledge base
notes.md — temporary scratchpad
tasks/*/progress.md — task history
```

### Write
```
MEMORY.md — update with extracted knowledge
notes.md — clear processed items
```

## Anti-Patterns

- DO NOT extract trivial or one-off items
- DO NOT duplicate existing memory entries
- DO NOT remove entries without verification
- DO NOT dream during active task execution
- DO NOT skip the evaluation step

## Cadence

- **After major tasks**: Extract immediately
- **Weekly**: Full consolidation
- **Before compaction**: Emergency extraction
