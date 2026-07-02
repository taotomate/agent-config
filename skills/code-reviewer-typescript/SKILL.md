---
name: code-reviewer-typescript
description: "Code Review Rules for TypeScript and React files. Trigger: When reviewing .ts, .tsx, .js or .jsx files."
license: Apache-2.0
metadata:
  author: taotomate
  inherited_from: "gentleman-programming/gga/AGENTS.md"
  version: "1.1"
---

# Code Reviewer - TypeScript/React

## When to Use

Load this skill whenever you are acting as a Code Reviewer and the files being reviewed are TypeScript, React, or JavaScript files (`.ts`, `.tsx`, `.js`, `.jsx`).

## General Review Rules

REJECT the code if you find:
- Hardcoded secrets or credentials
- Empty catch blocks (silent error handling)
- Code duplication (violates DRY)
- `console.log` in production code

## TypeScript / React Specific Rules

REJECT if:
- `any` type is used
- `import * as React` → use `import { useState }` (named imports)
- `var()` or hex colors in className → use Tailwind utilities
- `useMemo`/`useCallback` without justification (React 19 Compiler handles this)
- Missing `"use client"` in client components

PREFER:
- `cn()` for conditional class merging
- Semantic HTML over divs
- Named exports over default exports

## Response Format

FIRST LINE must be exactly:
STATUS: PASSED
or
STATUS: FAILED

If FAILED, list: `file:line - rule violated - issue`
