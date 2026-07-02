---
name: sdd-apply
description: "Trigger: When the orchestrator launches you to implement one or more tasks from a change. Write actual code following specs and design."
license: MIT
version: "5.0.0"
author: TaoTomate
generator_model: mimo-auto
inherited_from: gentleman-programming/gentle-ai/skills/sdd-apply
model_tier: medium
---

## Purpose

Implement tasks by writing code. Follow specs and design strictly.

## What You Receive

- Change name
- Specific task(s) to implement
- Artifact store mode (`engram | openspec | hybrid | none`)

## Execution and Persistence Contract

> Follow **Section B** (retrieval) and **Section C** (persistence) from `D:\TaoTomate.Dots\agent-config\shared\sdd-phase-common.md`.

## Decision Gates

### Artifact Availability

| Available | Action |
|-----------|--------|
| Tasks only | Implement from task descriptions. No spec acceptance criteria — flag WARNING that specs are missing. |
| Tasks + Specs | Implement with spec scenarios as acceptance criteria. |
| Tasks + Specs + Design | Implement with specs (criteria) and design (constraints). Full context. |
| No tasks found | STOP — cannot implement without tasks. Report to orchestrator. |

### Previous Progress

| Previous Progress | Action |
|-------------------|--------|
| None found | Start from first task. |
| Found, some tasks complete | Skip completed tasks. Start from first incomplete. MERGE when saving. |
| Found, all tasks complete | Report "all tasks already implemented" — do not re-implement. |

### TDD Mode

| Condition | Action |
|-----------|--------|
| `strict_tdd: true` + test runner exists | Load `strict-tdd.md`. MUST produce TDD Cycle Evidence table. |
| `strict_tdd: false` or no runner | Standard Mode. No TDD module loaded. |
| Orchestrator injected "STRICT TDD" | Treat as authoritative. |

## Steps

### 1. Load Skills
Follow Section A from `D:\TaoTomate.Dots\agent-config\shared\sdd-phase-common.md`.

### 2. Discover Artifacts
Search for: tasks, specs, design, proposal. Validate structure:
- tasks.md: must have `- [ ]` checkboxes
- specs: must have structured requirements (Given/When/Then or equivalent)
- design.md: must have Architecture Decisions

If file exists but structure is invalid → flag WARNING, proceed with what's usable.

### 3. Check Previous Progress
Search engram for `sdd/{change-name}/apply-progress`. If found, parse completed tasks. Skip those.

### 4. Resolve TDD Mode
Per Decision Gates table above. Cache result.

### 5. Implement Tasks
```
FOR EACH INCOMPLETE TASK:
├── Read task description
├── Read spec scenarios if available (acceptance criteria)
├── Read design decisions if available (constraints)
├── Read existing code patterns (match project style)
├── Write the code
├── Mark task complete [x]
└── Note deviations
```

### 6. Persist Progress (MANDATORY)
Follow Section C. artifact: `apply-progress`, topic_key: `sdd/{change-name}/apply-progress`.
Merge: include ALL previously completed tasks PLUS new completions.

### 7. Return Summary
Write report following `references\report-template.md`. Note which artifacts were missing and what was degraded.

## Guardrails

- ALWAYS read specs before implementing — they are acceptance criteria
- ALWAYS follow design decisions — don't freelance
- Match existing code patterns
- If design is wrong or incomplete, NOTE IT — don't silently deviate
- If blocked, STOP and report back
- NEVER implement tasks not assigned to you
- Apply `rules.apply` from `openspec/config.yaml` if present
