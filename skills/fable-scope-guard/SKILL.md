---
name: fable-scope-guard
description: Prevent scope creep. Use when implementing features, fixing bugs, or making changes. Ensures you only do what the task requires.
version: 1.0.0
author: TaoTomate
generator_model: opencode-go/qwen3.7-plus
inherited_from: fablever
---

# Fable Scope Guard

**Trigger:** Before implementing any change, fixing any bug, or making any modification.

**Purpose:** Prevent scope creep. Ensure you only do what the task requires.

## Rules

1. **Don't add features beyond what the task requires.** A bug fix doesn't need surrounding cleanup.
2. **Don't add error handling for scenarios that cannot happen.** Validate only at real system boundaries.
3. **Don't create README or documentation files unless asked.**
4. **Prefer editing an existing file over creating a new one.**
5. **Don't refactor "while you're at it".** If it's not in the task, don't do it.

## Check

Before delivering, ask:
- Did I do exactly what was asked?
- Did I add anything extra "because it's good practice"?
- Did I refactor something unrelated?

If yes to any of the last two → remove it.

## Example

**Task:** "Fix the login button not working"

** Wrong:**
- Fix login button
- Also update the CSS to use Tailwind
- Also add loading state
- Also add error handling for network failures
- Also write tests

**✅ Right:**
- Fix login button
- Verify it works
