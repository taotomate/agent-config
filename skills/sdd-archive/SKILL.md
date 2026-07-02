---
name: sdd-archive
description: "Trigger: When the orchestrator launches you to archive a change after implementation and verification. Close the change and persist final state."
license: MIT
version: "3.0.0"
author: TaoTomate
generator_model: mimo-auto
inherited_from: gentleman-programming/gentle-ai/skills/sdd-archive
model_tier: fast
---

## Purpose

Close a completed change. Merge delta specs into main specs, archive the change folder, save lineage.

## What You Receive

- Change name
- Artifact store mode (`engram | openspec | hybrid | none`)

## Steps

### 1. Load Skills
Follow Section A from `agent-config/shared/sdd-phase-common.md`.

### 2. Verify Completion
Confirm verify-report exists and verdict is PASS or PASS WITH WARNINGS. If FAIL, refuse to archive — report back.

### 3. Merge Specs (openspec/hybrid)
For each delta spec in `openspec/changes/{change-name}/specs/`:
- Read the delta
- Merge into `openspec/specs/{domain}/spec.md`
- Resolve conflicts in favor of the new behavior

### 4. Archive Change Folder (openspec/hybrid)
Move `openspec/changes/{change-name}/` to `openspec/changes/archive/YYYY-MM-DD-{change-name}/`.

### 5. Save Archive Report
Follow Section C. artifact: `archive-report`, topic_key: `sdd/{change-name}/archive-report`.
Include: change summary, all artifact IDs, final spec versions, verification verdict.

### 6. Return Summary
- Change: {name}
- Status: ARCHIVED
- Specs merged: {N domains}
- Artifact lineage: {list of observation IDs}
- Session complete.

## Guardrails

- NEVER archive a change with FAIL verdict
- Preserve all artifact IDs for traceability
- Use today's date in ISO format for archive folder name
- The archive is an AUDIT TRAIL — never modify archived changes
