---
name: auditor
description: Recovery and analysis protocol for system failures or guardrail violations.
version: 1.0.0
author: TaoTomate
generator_model: gemini-1.5-pro
inherited_from: auditor/SKILL.md
migrated_by: skill-migrator@1.0.0
model_tier: medium
---

## Context & Triggers
**When to use this skill:**
- When a script or running command returns an error `exit code != 0`.
- When a validation or linting process fails catastrophically.
- When the agent violated a guardrail defined in the active skill.

## Prerequisites
- Read access to error logs (e.g. `.tmp/last_error.log`, `.config/error_log.md`, or console output).

## Execution Phases


### 1. Capture (Snapshot)
Extract the exact error and context (last executed commands or output tokens). Do not guess the error.

### 2. Analysis (Mismatch Report)
Compare the error with the skill being executed:
- Was a parameter missing?
- Was a restriction from the `Guardrails` section violated?
- Does the environment fail the `Prerequisites`?

### 3. Categorization & Action
Classify the error and act accordingly:
- **LogicError (Recoverable):** The code or prompt has a fixable bug. *Action:* Apply the patch and re-execute. Record the learning in `directives/errors_learned.md`.
- **ContextOverflow (LLM Failure):** The agent lost the execution thread or hallucinated. *Action:* Clear context, summarize state, and retry with a more focused prompt.
- **SystemError (Fatal Failure):** Permission error, network outage, chronic missing dependencies. *Action:* Suspend execution and escalate to the Human Architect.

## Guardrails
- **DO NOT** attempt blind iterative patches (more than 3 retries without success indicates a fatal failure).
- **ALWAYS** document the root cause before proposing and applying a solution.

## Data Structures / Examples & Commands
N/A — This skill dictates a reasoning and cognitive orchestration process, not specific terminal commands.

## Troubleshooting
If the auditor itself fails while trying to read logs, abort all operations, create a `FATAL_CRASH.md` file, and request manual intervention.
