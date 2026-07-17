---
name: claude-code-entry
description: Entry point for Claude Code. Loads base instructions from agents/base.md.
version: 5.0.0
author: TaoTomate
generator_model: mimo-auto
inherited_from: agents/base.md + agents/claude-code.md
---

# Claude Code — Entry Point

**This file is a thin entry point. Claude Code loads this file automatically.**

## Loading order

1. Read `agents/base.md` — universal rules, behavior, engram, SDD
2. Read `agents/claude-code.md` — Claude-specific overrides
3. Both apply. If they conflict, platform overrides win.

## Quick reference

- Identity: `{provider}/{model} | claude-code.`
- Skills: load from `skills/` directory by trigger
- Governance: `.config/GOVERNANCE_PROTOCOL.md`
- Memory: Engram via MCP (always active)
