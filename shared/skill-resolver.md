---
name: skill-resolver
description: Universal protocol for resolving and injecting skills into sub-skills
version: 1.0.0
author: TaoTomate
generator_model: mimo-auto
inherited_from: custom
---

# Skill Resolver — Universal Protocol

Any service that **delegates work to sub-skills** MUST follow this protocol to resolve and inject relevant skills. This applies to the ATL orchestrator, double-blind-review, pr-review, and ANY future skill or workflow that launches sub-skills.

## Why This Exists

sub-skills are born with NO context about what skills exist. Without skill injection, an auditor reviewing a Next.js project won't know React 19 patterns, a Fix Skill won't follow project conventions, and a PR creator won't use the project's PR template.

## When to Apply

Before EVERY sub-skill launch that involves **reading, writing, or reviewing code**. Skip only for purely mechanical delegations (e.g., "run this test command").

## The Protocol

### Step 0: Resolve Model Tier for Delegation

Before loading skills, determine the **model tier** needed for this sub-skill:

| Delegation Type | Model Tier | Rationale |
|-----------------|------------|-----------|
| Architecture, design, complex analysis, proposal writing | `high` | Needs maximum reasoning capacity |
| Orchestration, routing, error handling, coordination, PR creation | `medium` | Balanced reasoning + speed |
| Code implementation, test writing, linting, refactoring, script execution | `fast` | Prefer scripts (L3); if LLM needed, use free cloud/local |

**Resolution order:**
1. Check sub-skill's frontmatter `model_tier` field (source of truth)
2. Fallback: infer from delegation type using table above
3. Default: `medium`

**Action:** Call `execution/resolve_model.py <tier>` to get the actual model string. Inject into sub-skill prompt:
```
## Model Configuration (auto-resolved)
MODEL_TIER: <tier>
MODEL: <resolved-model-string>
```

The sub-skill uses this to know its budget/constraints. If it needs to spawn further delegations, it repeats Step 0.

---

### Step 1: Obtain the Skill Registry (once per session)

The registry contains a **Compact Rules** section with pre-digested rules per skill (5-15 lines each). This is what you inject — NOT full SKILL.md paths.

Resolution order:
1. Already cached from earlier in this session? → use cache
2. `mem_search(query: "skill-registry", project: "{project}")` → `mem_get_observation(id)` for full content
3. Fallback: read `.config/skill-registry.md` from the project root if it exists
4. No registry found? → proceed without skills (but warn the user: "No skill registry found — sub-skills will work without project-specific standards. Run `skill-registry` to fix this.")

### Step 2: Match Relevant Skills

Match skills on TWO dimensions:

**A. Code Context** — what files will the sub-skill touch or review?

Map file patterns to skills from the registry (common examples — always defer to the registry's Trigger field as the source of truth):
- `.tsx`, `.jsx` → react skills
- `.ts` → typescript skills
- `app/**`, `pages/**` → nextjs/angular/framework skills
- `.py` → python/django skills
- `.go` → go skills
- `*.test.*`, `*.spec.*` → testing skills
- Style files → tailwind/css skills

Use the `Trigger` field in the registry's User Skills table to match. Skills whose triggers mention the relevant technology or file type are matches.

**B. Task Context** — what ACTIONS will the sub-skill perform?

| sub-skill action | Match skills with triggers mentioning... |
|-----------------|------------------------------------------|
| Create a PR | "PR", "pull request" |
| Write/review code | The specific framework/language |
| Create Jira tickets | "Jira", "epic", "task" |
| Write Notion docs | "Notion", "RFC", "PRD" |
| Write comments | "comment" |
| Run tests | "test", "vitest", "pytest", "playwright" |

### Step 3: Inject into sub-skill Prompt

From the registry's **Compact Rules** section, copy the matching skill blocks directly into the sub-skill's prompt:

```
## Project Standards (auto-resolved)

{paste compact rules blocks for each matching skill}
```

This goes BEFORE the sub-skill's task-specific instructions, so standards are loaded before work begins.

**Key rule**: inject the COMPACT RULES text, not paths. The sub-skill should NOT read any SKILL.md files — the rules arrive pre-digested in its prompt.

### Step 4: Include Project Conventions

If the registry has a **Project Conventions** section, and the sub-skill will work on the project's code, also add:

```
## Project Conventions
Read these files for project-specific patterns:
- {path1} — {notes}
- {path2} — {notes}
```

Project conventions are short references (paths + notes), so passing them is cheap. The sub-skill reads them only if relevant to its task.

## Token Budget

The compact rules section should add **50-150 tokens per skill** to a sub-skill's prompt. For a typical delegation matching 3-4 skills, that's ~400-600 tokens — negligible compared to the code the sub-skill will read.

If more than **5 skill blocks** match, keep only the 5 most relevant (prioritize code context matches over task context matches).

## Compaction Safety

This protocol is compaction-safe because:
- The registry lives in engram/filesystem, not in the orchestrator's memory
- Each delegation re-reads the registry if needed (Step 1 handles cache miss)
- Compact rules are copied into each sub-skill's prompt at launch time — even if the orchestrator forgets, the sub-skills already have the rules

## Feedback Loop

sub-skills MUST report their skill resolution status in their return envelope:

- `injected` — received `## Project Standards (auto-resolved)` from the orchestrator (ideal path)
- `fallback-registry` — no standards received, self-loaded from skill registry
- `fallback-path` — no standards received, loaded via `SKILL: Load` path
- `none` — no skills loaded at all

**Orchestrator self-correction rule**: if a sub-skill reports anything other than `injected`, the orchestrator MUST:
1. Re-read the skill registry immediately (it may have been lost to compaction)
2. Ensure ALL subsequent delegations include `## Project Standards (auto-resolved)`
3. Log a warning to the user: "Skill cache miss detected — reloaded registry for future delegations."

This prevents silent degradation where the orchestrator forgets skills after compaction and all subsequent sub-skills work without standards.

## Integration Points

- **ATL Orchestrator**: follows this protocol for ALL delegations (SDD and non-SDD)
- **double-blind-review**: follows this protocol before launching Auditor A, Auditor B, and Fix Skill
- **pr-review**: already has internal skill loading — should migrate to this protocol for consistency
- **Any future skill that delegates**: MUST reference this protocol

## Helper: execution/resolve_model.py

```bash
python execution/resolve_model.py <high|medium|fast> [--prefer-local]
```
Returns JSON: `{"status":"success","data":{"model":"...","tier":"..."},"error_log":""}`

Priority: free cloud (renewable) → local (on-demand via `--prefer-local`) → configured fallback.
No paid APIs used unless explicitly configured in `opencode.json`.
