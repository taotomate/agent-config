---
name: code-reviewer-go
description: "Code Review Rules for Go files. Trigger: When reviewing .go files."
license: Apache-2.0
metadata:
  author: taotomate
  inherited_from: "gentleman-programming/gga/AGENTS.md"
  version: "1.1"
---

# Code Reviewer - Go

## When to Use

Load this skill whenever you are acting as a Code Reviewer and the files being reviewed are Go files (`.go`).

## General Review Rules

REJECT the code if you find:
- Hardcoded secrets or credentials
- Empty catch blocks (silent error handling)
- Code duplication (violates DRY)
- `fmt.Println()` or similar standard print in production code (should use structured logger)

## Go Specific Rules

REJECT if:
- Exported functions without doc comments
- Ignored errors (no `_ = err`)
- Naked returns in long functions

## Response Format

FIRST LINE must be exactly:
STATUS: PASSED
or
STATUS: FAILED

If FAILED, list: `file:line - rule violated - issue`
