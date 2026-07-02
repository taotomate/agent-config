---
name: work-unit-commits
description: Plans commits as reviewable work units. For implementation, commit splitting, chained PRs, or keeping tests/docs with code.
version: 1.1.0
author: TaoTomate
generator_model: nemotron-3-ultra-free
inherited_from: work-unit-commits/SKILL.md
migrated_by: skill-optimizer@1.0.0
model_tier: medium
---

## Context & Triggers
**When to use this skill:**
- Decide what belongs in each commit or PR
- Split a feature into reviewable work units
- Prepare commits before opening a PR
- Convert a large feature into chained or stacked PRs
- Triggers: "split commits", "work unit", "reviewable commits", "plan commits"


## Execution Phases


### 1. Diagnosis Phase
- Identify independent work units in the total change.
- Estimate lines changed per unit.
- If SDD `sdd-tasks` produced a Review Workload Forecast, consult it:
  - **Low risk**: keep work-unit commits within a single PR.
  - **Medium risk**: commit per work unit, monitor lines before PR.
  - **High risk**: follow SDD `delivery_strategy`.

### 2. Action Phase
- For each unit: build the smallest independent unit.
- Include verification (tests/docs) in the same unit.
- Commit with a Conventional Commit message that explains the result, not the file list.
- If the PR approaches 400 lines, promote commits/groups to chained PRs.

### 3. Verification Phase
- Each commit must pass the checklist (see Data Structures).
- The repo must make sense applying only that commit.
- Rollback must be possible without reverting unrelated work.

## Guardrails (Critical Rules)
- **ALWAYS** commit per work unit (deliverable behavior, fix, migration, or docs).
- **NEVER** commit by file type (e.g. "models", then "services", then "tests" if none work alone).
- **ALWAYS** keep tests with the code they verify (same commit).
- **ALWAYS** keep docs with the user-visible change (same unit).
- **ALWAYS** tell a story — the reviewer must understand why each commit exists from its diff and message.
- **ALWAYS** make each commit a candidate for a chained PR if the change grows.

## Data Structures / Examples & Commands

### Pre-Commit Checklist
- [ ] The commit has a clear purpose.
- [ ] The repo still makes sense applying only this commit.
- [ ] Tests or docs for this unit are included when applicable.
- [ ] Rollback is reasonable without reverting unrelated work.
- [ ] The message explains the result, not the file list.

### Split Examples
| Weak split | Better split (per work unit) |
|------------|------------------------|
| `add models` | `feat(auth): add token validation domain model and tests` |
| `add services` | `feat(auth): wire token validation into login flow` |
| `add tests` | Tests included with each behavior commit |
| `update docs` | Docs included with the user-visible change |

### Commands
```bash
# Review the story before committing
git diff --stat
git diff --cached --stat

# Check recent commit style
git log --oneline -5
```

## Troubleshooting
- *PR approaches 400 lines*: Promote commits or groups to chained PRs.
- *Contaminated diff*: Rebase against main and verify only the current unit appears.
- *Commit message too long*: Separate into title (<50 chars) + body (explanation of why).
