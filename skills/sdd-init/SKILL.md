---
name: sdd-init
description: "Trigger: When user wants to initialize SDD in a project, or says 'sdd init', 'openspec init'. Detects stack, conventions, testing capabilities, bootstraps persistence."
license: MIT
version: "4.0.0"
author: TaoTomate
generator_model: mimo-auto
inherited_from: gentleman-programming/gentle-ai/skills/sdd-init
model_tier: medium
---

## Purpose

Initialize SDD context in a project. Detect stack, conventions, testing capabilities. Bootstrap persistence backend. You are an EXECUTOR — do the work yourself, no sub-skills.

## What You Receive

- Artifact store mode (`engram | openspec | hybrid | none`)

## Steps

### 1. Detect Project Context
Read package.json, go.mod, pyproject.toml, etc. Identify stack, conventions, architecture patterns.

### 2. Detect Testing Capabilities
Follow `references/testing-capabilities.md` for detection logic and format. This is MANDATORY — cache results for downstream phases.

### 3. Resolve Strict TDD Mode
Priority chain: (1) system prompt marker, (2) openspec/config.yaml strict_tdd, (3) if test runner exists → default true, (4) no test runner → false. Do NOT ask user interactively.

### 4. Initialize Persistence
- **engram**: Save project context + testing capabilities. Do NOT create openspec/.
- **openspec**: Create openspec/ structure (config.yaml, specs/, changes/, changes/archive/). Generate config.yaml with detected context.
- **hybrid**: Both.
- **none**: Return context inline.

### 5. Build Skill Registry
Scan `*/SKILL.md` across skill directories. Read frontmatter triggers. Write `.config/skill-registry.md`. If engram available, also save to engram.

### 6. Persist Project Context (MANDATORY)
Save to engram (`sdd-init/{project-name}`) and/or openspec config.yaml. Never skip.

### 7. Return Summary
Follow `references/return-templates.md` for the appropriate mode template.

## Guardrails

- NEVER create placeholder spec files — specs come from sdd-spec during changes
- Detect real tech stack, don't guess
- NEVER behave as orchestrator — execute directly
- If openspec/ exists, report and ask before overwriting
- Keep config.yaml context concise (max 10 lines)
- ALWAYS persist testing capabilities — downstream phases depend on it
- If TDD requested but no test runner, set strict_tdd: false and explain
