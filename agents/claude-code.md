---
name: claude-code-wrapper
description: Claude Code agent wrapper. Loads base.md for universal rules, adds Claude-specific behavior.
version: 5.0.0
author: TaoTomate
generator_model: mimo-auto
inherited_from: agents/base.md
---

# Claude Code — Agent Instructions

**Load `agents/base.md` first. Everything there applies. This file adds only Claude-specific overrides.**

## Identification

First line: `{provider}/{model} | claude-code.`

## Claude-Specific Behavior

- You are running as Claude Code. Your tool set includes: Read, Write, Edit, Bash, Glob, Grep, Agent (sub-agents).
- When spawning sub-agents via Agent tool, always pass context="full" for state-critical work, context="none" for isolated exploration.
- For SDD phases that need deep reasoning, prefer spawning a sub-agent over doing it inline when context is getting large.

## Platform Notes

- Claude Code supports hooks (pre/post). The startup hook runs `gentle-ai skill-registry refresh --quiet`.
- Sub-agents run in their own context window. Pass essential context explicitly in the prompt.
- File paths: Claude Code resolves from the project root. Use relative paths.
