---
name: agents-entry
description: Entry point for MiMoCode and other agents that load AGENTS.md. Thin pointer to base instructions.
version: 5.0.0
author: TaoTomate
generator_model: mimo-auto
inherited_from: agents/base.md
---

# Agent Entry Point (MiMoCode + others)

**This file is a thin entry point. MiMoCode and similar agents load this automatically.**

## Loading order

1. Read `agents/base.md` — universal rules, behavior, engram, SDD
2. Read the platform-specific wrapper if available:
   - Claude Code: `agents/claude-code.md`
   - Gemini CLI: `agents/gemini-cli.md`
   - Antigravity: `agents/antigravity.md`
   - MiMoCode: no additional wrapper needed (base.md is sufficient)
3. Both apply. If they conflict, platform overrides win.

## Quick reference

- Identity: `{provider}/{model} | {platform}.`
- Skills: load from `skills/` directory by trigger (see `.config/skill-registry.md`)
- Governance: `.config/GOVERNANCE_PROTOCOL.md`
- Memory: Engram via MCP (always active)
