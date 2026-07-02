# AI Agent Comparison — OpenCode vs Hermes Agent vs Google Antigravity (Jun 2026)

## Sources
- OpenCode: https://opencode.ai, https://github.com/opencode-ai/opencode (archived Sep 2025)
- Hermes Agent: https://hermes-agent.nousresearch.com/docs, https://github.com/NousResearch/hermes-agent
- Google Antigravity: https://antigravity.google, https://en.wikipedia.org/wiki/Google_Antigravity

---

## OpenCode (by AnomalyCo)

- **Type**: Open-source AI coding agent for terminal/IDE/desktop
- **Install**: `curl -fsSL https://opencode.ai/install | bash` / npm / brew / choco
- **GitHub**: 160K+ stars, 900+ contributors, 7.5M monthly devs
- **Repo**: https://github.com/opencode-ai/opencode (archived Sep 2025, read-only)
- **Language**: TypeScript
- **Modes**: TUI, desktop app, IDE extension (VS Code, Zed, etc.)
- **Privacy**: Does NOT store code or context data
- **ACP Support**: YES — has ACP Support section in docs (can act as ACP client)
- **Zen**: Curated/benchmarked models for coding agents
- **Subagents**: @general for complex tasks
- **2 agents**: build (full-access) + plan (read-only)
- **Model-agnostic**: Claude, GPT-4, Gemini, local models

## Hermes Agent (by Nous Research)

- **Type**: Self-improving autonomous AI agent with built-in learning loop
- **Install**: `curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash`
- **GitHub**: 188K+ stars, 32.4K forks, 11,146+ commits
- **Repo**: https://github.com/NousResearch/hermes-agent (active)
- **Language**: Python
- **Key differentiator**: "The only agent with a built-in learning loop"
- **ACP Support**: YES — full acp_adapter/ directory (server, session, tools, auth, events, permissions, provenance). Command: `hermes acp`
- **Skills**: Auto-creates skills from experience, self-improves during use
- **Memory**: FTS5 session search + Honcho user modeling
- **Cron**: Built-in scheduler with multi-platform delivery
- **Gateway**: Telegram, Discord, Slack, WhatsApp, Signal
- **Backends**: Local, Docker, SSH, Singularity, Modal, Daytona
- **Delegates**: Spawn isolated subagents for parallel workstreams
- **Runs on**: $5 VPS, GPU cluster, serverless (Modal/Daytona)

## Google Antigravity

- **Type**: AI-powered agentic IDE by Google
- **Launched**: May 2026 (v2 in beta)
- **URL**: https://antigravity.google
- **Wikipedia**: https://en.wikipedia.org/wiki/Google_Antigravity
- **Components**: IDE + CLI + SDK
- **Features**: Tab autocomplete, natural language code commands, context-aware agents
- **Engine**: Real Chromium underneath
- **Multi-model**: Supports multiple LLMs
- **Agent capabilities**: Plan, click, code, test, report across multiple windows
- **Status**: Closed-source product, no public GitHub repo
- **ACP Support**: NOT confirmed — no public documentation

---

## Which Can Orchestrate Which?

**Hermes Agent is the orchestrator.**

Capability | OpenCode | Hermes | Antigravity
-----------|----------|--------|------------
ACP Server | No | Yes (hermes acp) | Unknown
ACP Client | Yes | Yes | Unknown
Spawn subagents | Yes (@general) | Yes (delegate_task) | Unknown
Multi-agent orchestration | No | Yes | Unknown
Cron/scheduler | No | Yes (built-in) | No
Multi-platform messaging | No | Yes (Telegram, Discord, etc.) | No
Self-improving skills | No | Yes (built-in) | Unknown

Architecture: Hermes can spawn OpenCode as a subagent via ACP. Antigravity CLI (untested) could potentially connect to Hermes via ACP if it supports ACP client mode.

---

## Key Findings (Jun 2026)

1. OpenCode repo is archived (Sep 2025) — still active as product but GitHub is read-only
2. Hermes is the most capable orchestrator — ACP server + cron + multi-platform + self-improving
3. Antigravity is Google's newest agentic IDE — very recent (May 2026), closed-source, CLI untested
4. ACP is the bridge — both OpenCode and Hermes support ACP, making interop possible
5. User (Manu) has all 3 — uses Antigravity IDE (v2 beta), has Hermes running, OpenCode available
6. **Manu's desired architecture**: Hermes (OWL) as orchestrator → delegates to Antigravity CLI + OpenCode as coding subagents, each with their own LLM
7. **Hermes ACP server is active but unused** — needs to be connected to OpenCode/Antigravity CLI
8. **Next concrete step**: Test `antigravity --acp` or equivalent, test `opencode --acp`, connect both to Hermes ACP server

## Session Notes (2026-06-09)

- Hermes `acp_adapter` directory confirmed: entry.py, server.py, auth.py, events.py, tools.py, session.py, permissions.py, provenance.py, edit_approval.py
- `hermes acp` command starts the ACP server
- OpenCode ACP support confirmed in docs
- Antigravity CLI — user has it installed but NOT tested for ACP compatibility
- User's Playwright/RL browser method for web research is SUPERIOR to browser tool + curl — needs MCP setup
