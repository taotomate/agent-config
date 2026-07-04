# Components Reference

Every file and directory in agent-config, explained.

## Root Files

| File | Purpose | Loaded by |
|------|---------|-----------|
| `AGENTS.md` | MiMoCode entry point (~25 lines). Points to `agents/base.md`. | MiMoCode (auto) |
| `CLAUDE.md` | Claude Code entry point (~25 lines). Points to `agents/base.md`. | Claude Code (auto) |
| `GEMINI.md` | Gemini CLI entry point (~25 lines). Points to `agents/base.md`. | Gemini CLI (auto) |
| `README.md` | Installation, load map, structure overview | Human reference |
| `CHANGELOG.md` | Version history and migration notes | Human reference |
| `skills-report.md` | Auto-generated catalog of all 370 skills with versions and line counts | Human reference |
| `.gitignore` | Excludes temp files, caches, OS artifacts | Git |

## `agents/` — Agent Configurations

| File | Lines | Purpose |
|------|-------|---------|
| `base.md` | ~250 | **Source of Truth.** Universal rules, behavior, personality, anti-filler, engram, SDD protocol. All agents load this. |
| `claude-code.md` | ~25 | Claude-specific overrides only. Inherits everything from base.md. |
| `gemini-cli.md` | ~55 | Gemini-specific overrides. Includes anti-verbose and anti-filler behavioral rules. |
| `antigravity.md` | ~35 | Mission Control specifics for Antigravity platform. |

**Rule:** If a setting applies to all agents, put it in `base.md`. If it's platform-specific, put it in the platform file. Never duplicate.

## `.config/` — Runtime Configuration

| File | Purpose |
|------|---------|
| `GOVERNANCE_PROTOCOL.md` | Delegation checklist, anti-patterns, failure handling (Black Box Protocol). Loaded on failure or before delegating. v2.0.0. |
| `skill-registry.md` | Auto-generated index of all 370 skills with triggers. Maps situations → skills. v2.1.0. |
| `error_log.md` | Runtime error log. Appended to by agents on failure. |

## `shared/` — Reference Documents

These are **not loaded into LLM context** automatically. They exist for human reference and for specific triggers.

| File | Purpose |
|------|---------|
| `VISION.md` | Philosophy and historical context. Why this system exists. Human-only. |
| `routing.md` | Model assignment by layer (L1/L2/L3). When to use scripts vs agents. |
| `audit-framework.md` | 7 axioms + 12 premises for auditing agent configurations. |
| `skill-style-guide.md` | Standards for writing SKILL.md files (body budget: 180-450 tokens). |
| `trigger-rules.md` | 3-tier trigger system: advisory → strong → strongest. |
| `template_skill.md` | Template for creating new skills. |
| `engram-convention.md` | Engram naming rules. |
| `persistence-contract.md` | SDD persistence modes. |
| `openspec-convention.md` | OpenSpec structure. |
| `distillation-protocol.md` | How to extract final technical decisions from sessions. |
| `skill-resolver.md` | How skills are resolved and loaded. |
| `sdd-phase-common.md` | Common rules for SDD phases. |
| `global_error_log.md` | Cross-project error history. |

## `skills/` — 370 Skills

Each skill is a directory with a `SKILL.md` file. Skills are context-triggered, not auto-loaded.

### Structure of a Skill

```
skills/<skill-name>/
  SKILL.md              Main skill file (loaded when triggered)
  references/           Detailed docs (extracted from SKILL.md to stay under budget)
  scripts/              Executable scripts (Python, bash, JS)
  examples/             Usage examples
  templates/            Output templates
```

### Skill Categories (sample)

| Category | Examples |
|----------|----------|
| SDD Workflow | sdd-init, sdd-design, sdd-spec, sdd-apply, sdd-verify, sdd-archive |
| Code Quality | auditor, double-blind-review, error-miner, code-reviewer-* |
| AI/ML | accelerate, axolotl, pytorch-fsdp, vllm, tensorrt-llm |
| Bioinformatics | alphafold, ensembl, uniprot, pubmed, chembl |
| Productivity | slack, notion, telegram, apple-notes, obsidian |
| Creative | ascii-art, baoyu-comic, manim-video, stable-diffusion |
| DevOps | docker-management, fastapi, build-mcp-server |

### Skill Loading

Skills are discovered via `.config/skill-registry.md`. The registry maps trigger phrases to skill paths. When a trigger matches the current context, the agent loads the corresponding `SKILL.md`.

## `tools/` — Utilities

| File | Purpose |
|------|---------|
| `skill_catalog.py` | Scan, hash, deduplicate, version-track skills. Generates skill-registry.md. |

### Usage

```bash
# Scan and generate registry
python tools/skill_catalog.py --scan skills/ --active-agent-config skills/ --update-registry .config/skill-registry.md

# Dry run (scan only, no write)
python tools/skill_catalog.py --scan skills/ --active-agent-config skills/
```

## `backups/` — Config Snapshots

Auto-generated snapshots of previous config versions. Used for rollback.

## `hermes-profiles/` — Hermes Worker Profiles

SOUL.md profiles for different Hermes worker modes: chat-fast, vision, research.

## `vault/` — Archived Skills

Skills that are deprecated or moved to archive. Contains code-reviewer-go, code-reviewer-python, code-reviewer-typescript.

## `project-templates/` — Templates for New Projects

Contains `AGENTS.md` template for bootstrapping new projects.

## Load Priority

When an agent starts, it loads in this order:

1. Entry point (AGENTS.md / CLAUDE.md / GEMINI.md) — ~25 lines
2. `agents/base.md` — ~250 lines (universal rules)
3. Platform-specific overrides (e.g., `agents/gemini-cli.md`) — ~55 lines
4. `.config/skill-registry.md` — once per session (skill discovery)
5. Skills on demand — when trigger matches
6. `.config/GOVERNANCE_PROTOCOL.md` — on failure only
