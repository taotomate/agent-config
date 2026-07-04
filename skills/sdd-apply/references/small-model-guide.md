# Small Model Guide — sdd-apply

Load this when using a local/small model (tier: fast). It inlines the key logic from `sdd-phase-common.md` so the model doesn't need to resolve external references.

## Simplified Decision Gates

**Artifact check:**
- Has tasks? → Implement them
- No tasks? → STOP, report "no tasks found"

**Progress check:**
- Previous progress exists? → Skip completed tasks
- No progress? → Start from task 1

**TDD check:**
- Has test runner? → Run tests after each change
- No test runner? → Skip tests

## Inline Steps

1. Read tasks file (tasks.md)
2. For each unchecked task `- [ ]`:
   a. Read the task description
   b. Read specs if available (acceptance criteria)
   c. Write the code
   d. Mark task `[x]` when done
3. Save progress to engram: `sdd/{change-name}/apply-progress`
4. Report: what was implemented, what was missing

## Inline Guardrails

- Read specs before writing code
- Match existing code style
- If blocked → STOP, don't guess
- Never implement tasks not assigned to you
- Never silently deviate from design

## Example

Task: "Add input validation to user registration"

1. Read task: validate email format
2. Read spec: email must match RFC pattern
3. Find existing validation code in project
4. Write validation function matching existing style
5. Mark task `[x]`
6. Save progress
