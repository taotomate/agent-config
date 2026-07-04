---
name: governance-protocol
description: Delegation, failure handling, and resilience rules for the agent ecosystem.
version: 2.0.0
author: TaoTomate
generator_model: mimo-auto
inherited_from: gentleman-programming/gentle-ai/.atl/GOVERNANCE_PROTOCOL.md + custom extensions
---

# Governance Protocol

Governs delegation, sub-agent creation, and failure handling. Prevents infinite delegation and improvisation.

## 1. Delegation Checklist

Before creating a sub-agent or invoking a skill:

- [ ] Is the task atomic or does it need breakdown first?
- [ ] Does a SKILL.md exist for this function? If not, create one using the template in `shared/template_skill.md`.
- [ ] Are all skill prerequisites satisfied?
- [ ] Does this inflate context without need? If yes → defer to a phase boundary.

## 2. Anti-Patterns (NEVER do these)

| Anti-pattern | Why it's wrong | Correct action |
|-------------|---------------|----------------|
| Reading 4+ files to "understand" inline | Inflates context, no structure | Run sdd-explore phase |
| Writing across multiple files inline | No review boundary | Defer to sdd-apply phase |
| Running tests/builds inline | Mixes verification with implementation | Defer to sdd-verify phase |
| Reading files then editing inline | Two phases blended | Do both in the same phase |
| Retrying without understanding root cause | Produces same error | Freeze → Snapshot → Recovery |

## 3. Delegation Decision Matrix

| Action | Inline | Defer |
|--------|--------|-------|
| Read 1-3 files to decide/verify | Yes | — |
| Read 4+ files to explore | — | sdd-explore phase |
| Read as preparation for writing | — | same phase as the write |
| Write atomic (one file, mechanical) | Yes | — |
| Write with analysis (multiple files) | — | sdd-apply phase |
| Bash for state (git, gh) | Yes | — |
| Bash for execution (test, build) | — | sdd-verify phase |

## 4. Agent/Task Schema

Every delegated execution must declare:
- **ID**: name of the function or sub-agent
- **Layer**: Executive (writes/executes) or Planning (reads/designs)
- **Guardrails**: know the skill's constraints before operating

## 5. Black Box Protocol (Failure Handling)

On ANY error (L3/Script or L2/Hallucination), the system does NOT improvise:

### Step 1: Freeze
Stop chain execution immediately. Do not attempt partial fixes.

### Step 2: Snapshot
Capture the current state:
- Script error: read `.tmp/last_error.log`
- Model error: capture the malformed output and the prompt that produced it
- Write both to `.config/error_log.md` with timestamp, model signature, and task type

### Step 3: Recovery
Invoke the `auditor` skill to analyze the failure and generate a structured correction plan BEFORE any blind repair attempts.

### Step 4: Log
Append to `shared/errors_learned.md`:
- What failed
- Root cause
- What was learned
- What rule needs to be added or adjusted

## 6. Escalation Rules

| Error type | Escalation |
|-----------|------------|
| Script fails validation | Fix script → re-run tests → do NOT continue until green |
| Model produces wrong output | Log → review harness → reassign model via `shared/routing.md` |
| User corrects a violation | Stop → log in `.config/error_log.md` → re-read rules → resume |
| Paid API failure | ASK user before retrying. No autonomous paid loops. |

## 7. Financial Guard

Any task involving paid APIs (Vision, Bulk Search, high-tier LLMs):
- Request confirmation BEFORE retrying failed loops
- Never loop autonomously on paid endpoints
- Log token consumption for audit
