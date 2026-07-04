---
name: branch-pr
description: >
  PR creation workflow for Agent Teams Lite following the issue-first enforcement system.
  Trigger: When creating a pull request, opening a PR, or preparing changes for review.
version: "2.1"
author: gentleman-programming
generator_model: gemini-1.5-pro
inherited_from: branch-pr/SKILL.md
migrated_by: skill-migrator@1.0.0
model_tier: medium
---

## Context & Triggers
**When to use this skill:**
- Creating a pull request for any change.
- Preparing a branch to be pushed and reviewed.
- Helping a contributor open a PR.


## Execution Phases


### 1. Diagnosis Phase
- Verify the issue to link has the `status:approved` label.

### 2. Action Phase
- Create a branch following the naming convention: `type/description`.
- Implement changes using conventional commits.
- Run `shellcheck` on modified scripts.
- Open the PR using the repository's corresponding PR template.
- Add exactly ONE `type:*` label.

### 3. Verification Phase
- Wait for automated checks to pass in the repository.

## Guardrails (Critical Rules)
- **ALWAYS** link an approved issue to EACH pull request, no exceptions.
- **ALWAYS** add exactly ONE `type:*` label to the PR.
- **NEVER** push or assume merge is possible without automated validations passing.
- **NEVER** use `Co-Authored-By` from AI assistants in commits.

## Data Structures / Examples & Commands

### Branch Naming Convention
Strict regex: `^(feat|fix|chore|docs|style|refactor|perf|test|build|ci|revert)\/[a-z0-9._-]+$`
**Format:** `type/description` (e.g. `feat/user-login`, `fix/zsh-glob-error`).

### PR Body Format
```markdown
Closes #<issue-number>

| File | Change |
|------|--------|
| `path/to/file` | What changed |

- [x] Scripts run without errors: `shellcheck scripts/*.sh`
- [x] Manually tested the affected functionality
- [x] Skills load correctly in target agent
```
*(Must use `.github/PULL_REQUEST_TEMPLATE.md`)*

### Conventional Commits
Regex: `^(build|chore|ci|docs|feat|fix|perf|refactor|revert|style|test)(\([a-z0-9\._-]+\))?!?: .+`
**Format:** `type(scope): description` or `type: description` (the `!` indicates a breaking change).

### Execution Commands
```bash
git checkout -b feat/my-feature main
shellcheck scripts/*.sh
git push -u origin feat/my-feature
gh pr create --title "feat(scope): description" --body "Closes #N"
gh pr edit <pr-number> --add-label "type:feature"
```

## ⚠️ Migration Residue (Evolution Feedback)
*(All information has been successfully mapped)*

## Troubleshooting

- **`gh pr create` fails**: Verify `gh auth status` and that you're on the correct branch. Ensure the PR template exists at `.github/PULL_REQUEST_TEMPLATE.md`.
- **Labels not found**: Run `gh label list` to verify available labels. Use an existing `type:*` label — do not create new ones.
- **Issue not found or wrong label**: Confirm the issue number is correct and has `status:approved`. If the label is missing, request human to add it.
