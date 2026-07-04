---
name: gemini-cli-entry
description: Entry point for Gemini CLI. Loads base instructions from agents/base.md.
version: 5.0.0
author: TaoTomate
generator_model: mimo-auto
inherited_from: agents/base.md + agents/gemini-cli.md
---

# Gemini CLI — Entry Point

**This file is a thin entry point. Gemini CLI loads this file automatically.**

## Loading order

1. Read `agents/base.md` — universal rules, behavior, engram, SDD
2. Read `agents/gemini-cli.md` — Gemini-specific overrides
3. Both apply. If they conflict, platform overrides win.

## Quick reference

- Identity: `{provider}/{model} | gemini-cli.`
- Skills: load from `skills/` directory by trigger
- Governance: `.config/GOVERNANCE_PROTOCOL.md`
- Memory: Engram via MCP (always active)
