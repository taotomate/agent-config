---
name: sdd-propose
description: "Trigger: When the orchestrator launches you to create or update a proposal for a change. Write a structured change proposal with approach and alternatives."
license: MIT
version: "3.0.0"
author: TaoTomate
generator_model: mimo-auto
inherited_from: gentleman-programming/gentle-ai/skills/sdd-propose
model_tier: high
---

## Purpose

Create a change proposal with clear intent, affected areas, approach, alternatives, and rollback plan.

## What You Receive

- Change name or topic
- Artifact store mode (`engram | openspec | hybrid | none`)

## Steps

### 1. Load Skills
Follow Section A from `agent-config/shared/sdd-phase-common.md`.

### 2. Read Context
In engram: retrieve project context and any existing artifacts. In openspec: read `openspec/specs/` and `openspec/config.yaml`. In none: use what the orchestrator provided.

### 3. Write proposal.md
Structure:
- **Intent**: what problem, why now
- **Affected Areas**: list of domains/modules/capabilities
- **Capabilities**: new and modified (maps to specs later)
- **Approach**: chosen strategy with rationale
- **Alternatives considered**: why rejected
- **Rollback plan**: how to undo if it fails
- **Risks**: known risks and mitigations
- **Out of scope**: what this change does NOT do

### 4. Persist (MANDATORY)
Follow Section C. artifact: `proposal`, topic_key: `sdd/{change-name}/proposal`.

### 5. Return Summary
- Change: {name}
- Approach: {one-line}
- Alternatives: {N considered}
- Risks: {N identified}
- Ready for sdd-spec.

## Guardrails

- Every proposal MUST have a rollback plan
- Be specific about affected areas — no vague "general improvements"
- If the change is too large, suggest splitting into smaller changes
- Apply `rules.proposal` from `openspec/config.yaml` if present
