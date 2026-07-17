---
name: gemini-cli-wrapper
description: Gemini CLI agent wrapper. Loads base.md for universal rules, adds Gemini-specific overrides.
version: 5.3.0
author: TaoTomate
generator_model: mimo-auto
inherited_from: agents/base.md
---

# Gemini CLI — Agent Instructions

**Load `agents/base.md` first. Everything there applies. This file adds only Gemini-specific overrides.**

## Identification

First line: `{provider}/{model} | gemini-cli.`

## Gemini-Specific Behavior

- Gemini CLI loads instructions from `GEMINI.md` at project root.
- Model switching mid-session is not supported. Use the model you're assigned for the full session.
- For SDD phases: run all phases inline. No native sub-agent support.
