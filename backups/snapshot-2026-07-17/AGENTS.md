---
name: agents-entry
description: Entry point for OpenCode, MiMoCode, and other agents that load AGENTS.md. Thin pointer to base instructions.
version: 5.1.0
author: TaoTomate
generator_model: mimo-auto
inherited_from: agents/base.md
---

# Agent Entry Point

**This file is a thin entry point. OpenCode, MiMoCode, and similar agents load this automatically.**

## Loading order

1. Read `agents/base.md` — universal rules, behavior, engram, SDD
2. Read the platform-specific wrapper if available:
   - Claude Code: `agents/claude-code.md`
   - Gemini CLI: `agents/gemini-cli.md`
   - Antigravity: `agents/antigravity.md`
   - OpenCode: no additional wrapper needed (base.md is sufficient)
   - MiMoCode: no additional wrapper needed (base.md is sufficient)
3. Both apply. If they conflict, platform overrides win.

## Quick reference

- Identity: `{provider}/{model} | {platform}.`
- Skills: load from `skills/` directory by trigger (see `.config/skill-registry.md`)
- Governance: `.config/GOVERNANCE_PROTOCOL.md`
- Memory: Engram via MCP (always active)

## OpenCode specific

OpenCode uses this AGENTS.md as its primary configuration source. When OpenCode loads this file:

1. It inherits all rules from `agents/base.md`
2. Skills are discovered via `.config/skill-registry.md`
3. Governance protocol activates on failures
4. No additional configuration needed — this file is the complete entry point

## MiMoCode specific

MiMoCode automatically loads AGENTS.md from the project root. It inherits base.md rules and discovers skills via the registry.
