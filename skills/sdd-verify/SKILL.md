---
name: sdd-verify
description: "Trigger: When the orchestrator launches you to verify a completed (or partially completed) change. Validate that implementation matches specs, design, and tasks."
license: MIT
version: "5.0.0"
author: TaoTomate
generator_model: mimo-auto
inherited_from: gentleman-programming/gentle-ai/skills/sdd-verify
model_tier: medium
---

## Purpose

Quality gate. Prove with real execution evidence that implementation is complete, correct, and behaviorally compliant. Static analysis alone is NOT enough.

## What You Receive

- Change name
- Artifact store mode (`engram | openspec | hybrid | none`)

## Execution and Persistence Contract

> Follow **Section B** (retrieval) and **Section C** (persistence) from `D:\TaoTomate.Dots\agent-config\shared\sdd-phase-common.md`.

- **engram**: Read available artifacts. Save as `sdd/{change-name}/verify-report`.
- **openspec**: Write to `openspec/changes/{change-name}/verify-report.md`.
- **hybrid**: Both.
- **none**: Return inline only.

## Decision Gates

Before starting, determine verification scope based on available artifacts:

| Available Artifacts | Verification Scope |
|---------------------|-------------------|
| Tasks only | Completeness only — verify task checkboxes. Skip correctness and coherence. |
| Tasks + Specs | Completeness + Correctness — verify tasks and spec scenarios. Skip design coherence. |
| Tasks + Specs + Design | Full — completeness, correctness, and coherence. |
| Specs + Design (no tasks) | Correctness + Coherence — verify specs and design match. Flag missing tasks as WARNING. |
| Nothing found | STOP — report "no artifacts found" and return. Do not guess. |

If orchestrator says "STRICT TDD MODE IS ACTIVE" → treat as authoritative, load `strict-tdd-verify.md`.

## Steps

### 1. Load Skills
Follow Section A from `D:\TaoTomate.Dots\agent-config\shared\sdd-phase-common.md`.

### 2. Discover Available Artifacts
Search engram/openspec for: tasks, specs, design, proposal. For each, note: exists (yes/no), has valid structure (yes/no).

**Structure validation:**
- tasks.md: must have `- [ ]` or `- [x]` checkboxes with hierarchical numbering
- specs: must have Given/When/Then scenarios or equivalent structured requirements
- design.md: must have Architecture Decisions section with Choice/Alternatives/Rationale

If a file exists but has invalid structure, treat it as "exists but degraded" — flag WARNING and proceed with what's usable.

### 3. Resolve TDD Mode
Search engram for `sdd/{project}/testing-capabilities`. If orchestrator injected "STRICT TDD", use that. Cache result.

### 4. Execute Verification (per Decision Gates)
Run only the checks your artifact scope supports. For each check:

- **Completeness**: read tasks.md, count total/completed/incomplete. CRITICAL if core tasks incomplete.
- **Correctness**: for each spec requirement, search codebase for implementation evidence. CRITICAL if requirement missing.
- **Coherence**: for each design decision, verify approach was used and file changes match. WARNING on deviations.
- **TDD Compliance** (Strict TDD only): load `strict-tdd-verify.md` Step 5a.
- **Tests**: follow `references\test-execution.md`. CRITICAL on failures.

### 5. Spec Compliance Matrix
Cross-reference spec scenarios against test results. Statuses:
- ✅ COMPLIANT — test exists and passed
- ❌ FAILING — test exists but failed (CRITICAL)
- ❌ UNTESTED — no test found (CRITICAL)
- ⚠️ PARTIAL — test passes but covers partial scenario (WARNING)
- ➖ SKIPPED — artifact missing, check not performed

### 6. Persist Report
Follow Section C. artifact: `verify-report`, topic_key: `sdd/{change-name}/verify-report`.

### 7. Return Summary
Write report following `references\report-template.md`. Include which dimensions were skipped and why.

## Guardrails

- ALWAYS read actual source code — don't trust summaries
- ALWAYS execute tests — static analysis alone is not verification
- A scenario is COMPLIANT only only when a covering test PASSED
- Compare against SPECS first, DESIGN second
- Be objective — report what IS, not what should be
- DO NOT fix issues — only report. Orchestrator decides.
- If artifacts are missing, verify what you can and report gaps — don't guess
- If Strict TDD active, load `strict-tdd-verify.md` — all steps mandatory
- If Strict TDD NOT active, NEVER load `strict-tdd-verify.md`
