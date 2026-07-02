---
name: sdd-tasks
description: "Trigger: When the orchestrator launches you to create or update the task breakdown for a change. Break design into atomic, completable tasks."
license: MIT
version: "3.0.0"
author: TaoTomate
generator_model: mimo-auto
inherited_from: gentleman-programming/gentle-ai/skills/sdd-tasks
model_tier: medium
---

## Purpose

Break the design into atomic tasks organized by phase. Each task must be completable in one session.

## What You Receive

- Change name
- Artifact store mode (`engram | openspec | hybrid | none`)

## Steps

### 1. Load Skills
Follow Section A from `agent-config/shared/sdd-phase-common.md`.

### 2. Analyze Design
Identify: files to create/modify/delete, dependency order, testing requirements per component.

### 3. Write tasks.md
Organize by phase (Infrastructure → Implementation → Testing). Each task:
- Clear description of WHAT to do
- Which files are affected
- Acceptance criteria (maps to spec scenarios)
- Dependencies on other tasks

Number hierarchically: 1.1, 1.2, 2.1, etc.

### 4. Persist (MANDATORY)
Follow Section C. artifact: `tasks`, topic_key: `sdd/{change-name}/tasks`.

### 5. Return Summary
- Total tasks: {N}
- Phases: {list}
- Estimated complexity: Low/Medium/High
- Critical path: {which tasks are sequential dependencies}
- Ready for sdd-apply.

## Guardrails

- Tasks must be atomic — completable in one session
- Each task maps to at least one spec scenario
- Don't skip testing tasks — every implementation task needs a corresponding test task
- Keep tasks small enough to verify independently
- Apply `rules.tasks` from `openspec/config.yaml` if present
