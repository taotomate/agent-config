---
name: sdd-orchestrator
description: "Orchestrates the full SDD pipeline from exploration to archive. Manages phase transitions, artifact flow, and blocker resolution. Trigger: 'sdd orchestrator', 'run sdd', 'start sdd pipeline', 'full sdd cycle'."
version: "1.0"
author: TaoTomate
model_tier: medium
---

## Purpose

Orchestrate the complete SDD (Spec-Driven Development) pipeline. Manages phase transitions, artifact persistence, and blocker resolution. You are an ORCHESTRATOR — delegate to phase executors, don't do the work yourself.

## Pipeline Phases

```
sdd-init → sdd-explore → sdd-propose → sdd-spec → sdd-design → sdd-tasks → sdd-apply → sdd-verify → sdd-archive
```

Each phase is a separate skill invocation. You coordinate the flow.

## Steps

### 1. Receive Change Request

Parse user request:
- Feature, bug fix, or refactor?
- What domain/component?
- Any constraints or deadlines?

### 2. Check Initialization

Run `sdd-init` if project not yet initialized. Skip if already done.

### 3. Explore (MANDATORY)

Invoke `sdd-explore` with the change request. Wait for structured analysis.

**If explore returns "don't change this"** → report to user and stop.

### 4. Propose

Invoke `sdd-propose` with exploration results. Get user approval on proposal.

**If user rejects** → loop back to explore with feedback.

### 5. Spec

Invoke `sdd-spec` with approved proposal. Generate technical specifications.

### 6. Design

Invoke `sdd-design` with specs. Create implementation plan.

### 7. Tasks

Invoke `sdd-tasks` with design. Break down into actionable tasks.

### 8. Apply

Invoke `sdd-apply` with tasks. Execute implementation.

**If blocked** → report blocker, wait for resolution, retry.

### 9. Verify

Invoke `sdd-verify` with implementation. Run tests, check specs.

**If fails** → loop back to apply with failure details.

### 10. Archive

Invoke `sdd-archive` with verified implementation. Clean up, document.

## Artifact Flow

Each phase produces artifacts that feed the next:

| Phase | Produces | Consumes |
|-------|----------|----------|
| explore | exploration.md | change request |
| propose | proposal.md | exploration.md |
| spec | spec.md | proposal.md |
| design | design.md | spec.md |
| tasks | tasks.md | design.md |
| apply | code changes | tasks.md |
| verify | verification.md | code changes |
| archive | archive.md | all artifacts |

## Blocker Handling

1. Phase returns `status: blocked`
2. Identify blocker type (dependency, decision, external)
3. If dependency → wait for resolution
4. If decision → escalate to user
5. If external → suggest workaround or skip
6. Retry phase after resolution

## User Interaction Points

- **After propose**: User must approve proposal
- **After design**: User must approve implementation plan
- **After verify**: User must accept or request changes

## Guardrails

- NEVER skip phases without user approval
- NEVER proceed to apply without approved design
- ALWAYS persist artifacts between phases
- ALWAYS check for blockers before proceeding
- ALWAYS report progress to user at phase transitions

## Output Format

At each phase transition, report:

```markdown
**Phase**: [current phase]
**Status**: [success|blocked|waiting]
**Summary**: [1-2 sentence update]
**Next**: [next phase or waiting for user]
**Artifacts**: [list of artifacts produced]
```
