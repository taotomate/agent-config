---
name: sdd-onboard
description: "Trigger: When the orchestrator launches you to onboard a user through the full SDD cycle. Guided walkthrough of SDD using the user's real codebase."
license: MIT
version: "2.0.0"
author: TaoTomate
generator_model: mimo-auto
inherited_from: gentleman-programming/gentle-ai/skills/sdd-onboard
model_tier: medium
---

## Purpose

Guided end-to-end walkthrough of SDD using the user's real codebase. One phase at a time with explanation.

## What You Receive

- Artifact store mode (`engram | openspec | hybrid | none`)

## Steps

### 1. Load Skills
Follow Section A from `agent-config/shared/sdd-phase-common.md`.

### 2. Detect Context
Run sdd-init logic: detect stack, testing capabilities, persistence mode. If not initialized, do it now.

### 3. Walk Through Phases
For each phase in order: explore → propose → spec → design → tasks → apply → verify → archive:
1. Explain what this phase does and why it exists
2. Execute the phase on a real small change (suggest a simple one if user has none)
3. Show the output and explain key decisions
4. Ask: "Questions before we continue?"

### 4. Return Summary
- Phases completed: {list}
- Change created: {name or "practice run"}
- Key learnings: {what the user should remember}
- Next: try a real change with `/sdd-new`.

## Guardrails

- Use a SMALL, REAL change — not a toy example
- Explain the WHY behind each phase, not just the WHAT
- Let the user steer — if they want to skip ahead, let them
- If the user gets stuck, explain the concept, don't just do it for them
