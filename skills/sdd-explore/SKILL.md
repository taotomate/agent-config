---
name: sdd-explore
description: "Trigger: When the orchestrator launches you to think through a feature, investigate the codebase, or clarify requirements. Research and report — no files created by default."
license: MIT
version: "3.0.0"
author: TaoTomate
generator_model: mimo-auto
inherited_from: gentleman-programming/gentle-ai/skills/sdd-explore
model_tier: medium
---

## Purpose

Investigate codebase, think through problems, compare approaches. Return structured analysis. Only create `exploration.md` when tied to a named change.

## What You Receive

- Topic or feature to explore
- Artifact store mode (`engram | openspec | hybrid | none`)

## Steps

### 1. Load Skills
Follow Section A from `agent-config/shared/sdd-phase-common.md`.

### 2. Understand Request
Parse: new feature, bug fix, or refactor? What domain?

### 3. Investigate
Read entry points, search related functionality, check tests, identify patterns and dependencies.

### 4. Analyze Options
If multiple approaches exist, compare in a table: Approach | Pros | Cons | Complexity.

### 5. Persist (MANDATORY for named changes)
Follow Section C. artifact: `explore`, topic_key: `sdd/{change-name}/explore`.

### 6. Return Summary
- Topic explored
- Key findings (3-5 bullets)
- Recommended approach with rationale
- Risks or unknowns
- Ready for sdd-propose.

## Guardrails

- Read actual code — don't assume from names
- Compare approaches with concrete tradeoffs
- If the answer is "don't change this", say so
- Never create files unless tied to a named change
