---
name: skill-registry
description: Creates or updates the compact skill registry (skill-registry.md) by scanning available skills and indexing project conventions.
version: 1.1.0
author: TaoTomate
generator_model: gemini-1.5-pro
inherited_from: skill-registry/SKILL.md
migrated_by: skill-migrator@1.0.0
model_tier: fast
---

## Context & Triggers
**When to use this skill:**
- After installing or removing skills in the user's or project's environment.
- When setting up a new project (as an integrated part of `sdd-init`).
- When the human explicitly asks "update skills", "update registry", or "skill registry".


## Execution Phases


### 1. Diagnosis Phase
- Recursively scan for `SKILL.md` files in global locations (e.g. `~/.gemini/skills/`, `~/.claude/skills/`, `~/.config/opencode/skills/`) and local project locations (e.g. `{project-root}/.service/skills/`).
- Scan the project root for convention files (e.g. `CONSTITUTION.md`, `CLAUDE.md`, `.cursorrules`).
- If a conventions index file (`CONSTITUTION.md`) is found, read it to extract all referenced file paths.

### 2. Action Phase
- Extract metadata from discovered skills (`name` and `trigger`) by reading each `SKILL.md` file's frontmatter.
- Generate a **Compact Rules** block for each skill, extracting only the actionable constraints and skipping noise.
- Format the full result in Markdown tables (see Data Structures section).

### 3. Verification Phase
- Compulsorily write the compiled result to `{project-root}/.config/skill-registry.md`.
- If the `mem_save` tool is available (Engram MCP integration), invoke it to persist the registry content to persistent memory using `topic_key: "skill-registry"`.
- Display a concise console summary indicating how many user skills and project conventions were indexed.

## Guardrails (Critical Rules)
- **ALWAYS** skip `sdd-*`, `_shared`, and `skill-registry` directories during scanning. They do not contain "actionable code skills", but orchestrator meta-protocols. Injecting them would waste tokens uselessly.
- **NEVER** exceed 15 lines per "Compact Rules" block. They must be strict directives ("Do X", "Never Y"), without tutorials, motivation explanations, or long code examples.
- **ALWAYS** write the physical file `.config/skill-registry.md`, regardless of whether Engram database persistence fails, does not exist, or is disabled.

## Data Structures / Examples & Commands

### Expected "Compact Rules" Format
*Example for a React 19 skill:*
```markdown
### react-19
- Do NOT use useMemo/useCallback — the React Compiler handles memoization automatically.
- Use the use() hook for promises/context.
- Server Components by default, use 'use client' only for state/interactivity hooks.
- `ref` is now a regular prop, do not use forwardRef.
```

### Final `skill-registry.md` File Format
The generated file should look like this:

```markdown
# Skill Registry
**Exclusive use of the Delegator.**

## User Skills
| Trigger | Skill | Path |
|---------|-------|------|
| "create PR" | branch-pr | ~/.gemini/skills/branch-pr/SKILL.md |

## Compact Rules

### branch-pr
- Rule 1
- Rule 2

## Project Conventions
| File | Path | Notes |
|------|------|-------|
| CONSTITUTION.md | /path/to/CONSTITUTION.md | Index |
```
