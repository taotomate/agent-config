---
name: sdd-design
description: "Trigger: When the orchestrator launches you to write or update the technical design for a change. Create architecture decisions and approach."
license: MIT
version: "4.0.0"
author: TaoTomate
generator_model: mimo-auto
inherited_from: gentleman-programming/gentle-ai/skills/sdd-design
model_tier: high
---

## Purpose

Produce a `design.md` capturing HOW the change will be implemented — architecture decisions, data flow, file changes, and rationale.

## What You Receive

- Change name
- Artifact store mode (`engram | openspec | hybrid | none`)

## Decision Gates

| Available | Action |
|-----------|--------|
| Proposal only | Design based on intent. Flag that specs are missing — design may need revision after specs. |
| Proposal + Specs | Design with full acceptance criteria. Reference spec scenarios in decisions. |
| Proposal + Specs + Design (update) | Read existing design, update decisions. Preserve unchanged sections. |
| Nothing found | STOP — cannot design without context. |

## Steps

### 1. Load Skills
Follow Section A from `D:\TaoTomate.Dots\agent-config\shared\sdd-phase-common.md`.

### 2. Discover Artifacts
Search for: proposal, specs, design (if updating). Validate structure:
- proposal.md: must have Intent, Approach, Affected Areas
- specs: must have structured requirements
- design.md (if updating): must have Architecture Decisions

### 3. Read Codebase
Read affected entry points, module structure, existing patterns, dependencies.

### 4. Write Design
Follow `references\design-template.md`. Key sections: Technical Approach, Architecture Decisions (with rationale), Data Flow, File Changes, Interfaces, Testing Strategy.

### 5. Persist Artifact (MANDATORY)
Follow Section C. artifact: `design`, topic_key: `sdd/{change-name}/design`.

### 6. Return Summary
- Change: {name}
- Approach: {one-line}
- Key Decisions: {N}
- Artifacts used: {list what was available}
- Artifacts missing: {list what was missing and how it affected design}
- Ready for sdd-tasks.

## Guardrails

- ALWAYS read actual codebase before designing — never guess
- Every decision MUST have a rationale
- Include concrete file paths
- Follow existing patterns — note deviations
- Size budget: under 800 words. Decisions as tables.
- If open questions BLOCK the design, say so — don't guess
- Apply `rules.design` from `openspec/config.yaml` if present
