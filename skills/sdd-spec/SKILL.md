---
name: sdd-spec
description: "Trigger: When the orchestrator launches you to write or update specs for a change. Create delta specifications with Given/When/Then scenarios."
license: MIT
version: "4.0.0"
author: TaoTomate
generator_model: mimo-auto
inherited_from: gentleman-programming/gentle-ai/skills/sdd-spec
model_tier: medium
---

## Purpose

Write delta specifications based on the proposal. Each affected domain gets a spec with Given/When/Then scenarios and RFC 2119 keywords.

## What You Receive

- Change name
- Artifact store mode (`engram | openspec | hybrid | none`)

## Decision Gates

| Available | Action |
|-----------|--------|
| Proposal with Capabilities section | Use Capabilities to map New → full spec, Modified → delta spec. |
| Proposal without Capabilities | Infer from "Affected Areas". Flag that explicit mapping is preferred. |
| Proposal + existing specs | Read existing specs first. Write deltas that modify them. |
| Proposal only (no existing specs) | Write full specs for all affected domains. |
| Nothing found | STOP — cannot write specs without proposal. |

## Steps

### 1. Load Skills
Follow Section A from `D:\TaoTomate.Dots\agent-config\shared\sdd-phase-common.md`.

### 2. Discover Context
Search for: proposal, existing specs in `openspec\specs\`. Validate:
- proposal.md: must have Affected Areas or Capabilities
- existing specs: must have structured requirements

### 3. Identify Domains
Per Decision Gates above. Map proposal sections to spec domains.

### 4. Write Delta Specs
Each spec MUST include:
- **Capability**: what this domain provides
- **Scenarios**: Given/When/Then format, one per behavior
- **Requirements**: RFC 2119 keywords (MUST/SHALL/SHOULD/MAY)
- **Edge cases**: error states, boundary conditions
- **Out of scope**: what this change does NOT touch

### 5. Persist (MANDATORY)
Follow Section C. artifact: `spec`, topic_key: `sdd/{change-name}/spec`.

### 6. Return Summary
- Domains covered: {list}
- Total scenarios: {N}
- New capabilities: {N}
- Modified capabilities: {N}
- Existing specs read: {list or "none"}
- Ready for sdd-design or sdd-tasks.

## Guardrails

- Scenarios MUST be testable
- Use RFC 2119 keywords precisely
- Don't repeat existing specs — write only deltas
- If proposal has no Capabilities section, infer from "Affected Areas" but flag it
- Apply `rules.specs` from `openspec/config.yaml` if present
