---
name: agents-entry
description: Entry point for OpenCode, MiMoCode, and other agents that load AGENTS.md. Thin pointer to base instructions with Fable 5 behavioral upgrades.
version: 5.3.0
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
- Fable enforcement: `plugins/fable-profile` (hooks) + `tools/fable-mcp` (verification)

## OpenCode specific

OpenCode uses this AGENTS.md as its primary configuration source. When OpenCode loads this file:

1. It inherits all rules from `agents/base.md` (v5.3.0 with Fable upgrades)
2. Skills are discovered via `.config/skill-registry.md` (389 skills)
3. Governance protocol activates on failures
4. Fable hooks activate automatically (auto-backup, turn discipline, operating cadence)
5. Fable MCP server available for verification (fable_lint, fable_status, get_fable_profile)
6. No additional configuration needed — this file is the complete entry point

## MiMoCode specific

MiMoCode automatically loads AGENTS.md from the project root. It inherits base.md rules and discovers skills via the registry.

## Fable 5 Upgrades (v5.3.0+)

This configuration includes Fable 5 behavioral upgrades:

### Behavioral (base.md)
- **Task Discipline**: Ordered task lists with dependency tracking, priority markers, nested subtasks
- **Turn Discipline**: No ending on promises — only on results or clear blockers
- **Operating Cadence**: Scale tool calls to complexity (1 vs 3-5 vs 5-15)
- **Ground Every Claim**: Audit claims against tool results, evidence ledger
- **Mistake Handling**: Acknowledge without collapse, fix immediately
- **Autonomy Calibration**: Proceed on reversible actions, ask on destructive

### Mechanical (plugins/fable-profile)
- 4 hooks: auto-backup, operating cadence tracking, turn discipline check, session start reminder
- Pre-write backup + post-write verification + rollback on failure

### Verification (tools/fable-mcp)
- 3 tools: `fable_lint` (7 rules), `fable_status`, `get_fable_profile`
- HTTP server on port 3456

### On-demand (skills/fable-*)
- `fable-scope-guard` — Prevent scope creep
- `fable-delivery-gate` — Acceptance check before delivering
- `fable-evidence-done` — Verify claims against tool results
- `fable-review` — Adversarial review with 4 lenses
- `fable-seed` — Initialize Fable working style