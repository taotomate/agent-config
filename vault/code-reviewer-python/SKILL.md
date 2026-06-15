---
name: code-reviewer-python
description: "Code Review Rules for Python files. Trigger: When reviewing .py files."
license: Apache-2.0
metadata:
  author: taotomate
  inherited_from: "gentleman-programming/gga/AGENTS.md"
  version: "1.1"
---

# Code Reviewer - Python

## When to Use

Load this skill whenever you are acting as a Code Reviewer and the files being reviewed are Python files (`.py`).

## General Review Rules

REJECT the code if you find:
- Hardcoded secrets or credentials
- Empty catch blocks (silent error handling)
- Code duplication (violates DRY)
- `print()` in production code (should use `logger`)

## Python Specific Rules

REJECT if:
- Missing type hints on public functions
- Bare `except:` without specific exception
- `print()` instead of `logger`

## Response Format

FIRST LINE must be exactly:
STATUS: PASSED
or
STATUS: FAILED

If FAILED, list: `file:line - rule violated - issue`
