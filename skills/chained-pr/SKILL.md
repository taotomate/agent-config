---
name: chained-pr
description: Splits large changes (>400 lines) into chained PRs to protect reviewer focus. Supports Stacked PRs and Feature Branch Chain.
version: 1.1.0
author: TaoTomate
generator_model: nemotron-3-ultra-free
inherited_from: chained-pr/SKILL.md
migrated_by: skill-optimizer@1.0.0
model_tier: medium
---

## Context & Triggers
**When to use this skill:**
- A planned PR may exceed **400 changed lines**
- SDD forecasts `400-line budget risk: High` or `Chained PRs recommended: Yes`
- The user asks for chained PRs, stacked PRs, or reviewer load control
- Triggers: "chained PR", "stacked PR", "split PR", "large PR"


## Execution Phases


### 1. Diagnosis Phase
- Estimate changed lines and identify independent work units.
- If SDD has a `delivery_strategy`, use it. If not, ask the user for a strategy.
- Determine the strategy according to the decision table (see Data Structures).

### 2. Action Phase
- Create branches/PRs using the chosen strategy.
- Add Chain Context to each PR without replacing the repo template.
- In Feature Branch Chain: create a tracker PR as draft/no-merge; child PR #1 points to the tracker branch, subsequent ones to the immediate parent.

### 3. Verification Phase
- Verify each PR independently: CI/tests/docs/manual checks, rollback scope, clean diff.
- Keep the tracker PR as draft/no-merge until all child PRs are reviewed and merged.
- Ensure the diff only contains the current work unit (rebase/retarget if there is contamination).

## Guardrails (Critical Rules)
- **ALWAYS** split PRs > 400 lines unless a maintainer explicitly accepts `size:exception`.
- **ALWAYS** keep each PR reviewable within ≤60 minutes.
- **ALWAYS** include in each PR: start, end, previous dependencies, follow-up, and out-of-scope.
- **ALWAYS** include a dependency diagram marking the current PR with `📍`.
- **NEVER** mix chaining strategies after the user has chosen one.
- **NEVER** treat contaminated diffs as normal — retarget or rebase until only the current unit appears.

## Data Structures / Examples & Commands

### Strategy Decision Table

| Condition | Strategy |
|-----------|----------|
| PR ≤400 lines and focused | Single PR |
| PR >400, each fragment can land independently | Stacked PRs to main |
| PR >400, feature must integrate before main | Feature Branch Chain with tracker |
| Generated/vendor/migration diff cannot be split | Ask maintainer for `size:exception` |
| SDD provides `delivery_strategy` | Follow it before apply/PR creation |

### PR Body Format (Chain Context)
```markdown
## Chain Context
- **Strategy**: {Stacked PRs | Feature Branch Chain}
- **Order**: PR {N} of {M}
- **Depends on**: {PR #previous} | "None (root)"
- **Follow-up**: {PR #next} | "None (last)"
- **Out of scope**: {what is intentionally deferred}
- **Review budget**: {additions + deletions} lines
{📍 current PR marker}
```

### Useful Commands
```bash
# Create branch for chained PR
git checkout -b feat/my-feature-pr2 feat/my-feature-pr1

# Verify clean diff (only this PR's changes)
git diff main...HEAD

# Open PR pointing to the parent branch
gh pr create --base feat/my-feature-pr1 --title "feat(scope): description" --body "..."
```

## ⚠️ Migration Residue (Evolution Feedback)
- `references/chaining-details.md` — external documentation not migrated. Consider integrating as a separate reference.

## Troubleshooting
- *Contaminated diff*: Rebase against the correct base branch: `git rebase --onto <parent-branch> <old-base> <current-branch>`.
- *Chain merge conflicts*: Resolve in the oldest PR first, then rebase the dependents.
