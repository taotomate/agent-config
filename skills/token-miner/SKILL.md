---
name: token-miner
description: Guides the user through obtaining and managing free LLM credits from various providers. Ensures the "LLM Proxy Service Arsenal" is always stocked with low-cost or free tokens. Trigger: "find credits", "token miner", "renew tokens", "free tokens", "mine tokens".
version: "1.2"
author: TaoTomate
license: MIT
model_tier: fast
---

## Context & Triggers
**When to use this skill:**
- When the user needs free or low-cost LLM API tokens.
- When existing tokens are expired or running low.
- Triggers: "find credits", "token miner", "renew tokens", "free tokens", "mine tokens".


## Execution Phases


### 1. Diagnosis Phase
- Ask the user which provider they want to set up, or recommend based on need:
  - High volume, low cost → Google AI Studio (Gemini) or Groq
  - Model diversity → Together AI or OpenRouter
  - Maximum intelligence → Anthropic (Claude)

### 2. Action Phase
- Guide the user through the chosen provider's signup and key generation steps (see Data Structures).
- Confirm the key works by suggesting a test command.

### 3. Verification Phase
- Ask the user to store the key in an environment variable or secure config.
- Recommend running `telemetry` to track usage.

## Guardrails (Critical Rules)
- **ALWAYS** prioritize providers with generous free tiers (Google, Groq) for volume tasks.
- **ALWAYS** recommend Flash/Small models for high-volume tasks (research, distillation).
- **NEVER** ask the user to paste API keys into this SKILL.md file — use environment variables or system-specific secrets.
- **ALWAYS** direct users to the provider's official site for signup — never store credentials.

## Data Structures / Examples & Commands

### Provider Quick Reference

| Provider | Free Tier | Best For | Sign Up |
|----------|-----------|----------|---------|
| Google AI Studio | 1500 RPM Gemini 1.5 Flash | High volume, free | aistudio.google.com |
| Groq Cloud | Generous free tier | Fastest inference | console.groq.com |
| Together AI | $5-$25 initial credit | Open Source models | together.ai |
| OpenRouter | Pay-per-use, no minimum | Multi-model unified API | openrouter.ai |
| Anthropic | Initial free credits | Maximum intelligence | console.anthropic.com |

### Setup Steps

**Google AI Studio (Gemini):**
```bash
# 1. Go to https://aistudio.google.com
# 2. Login with any Google account
# 3. Click "Get API key" → Create in new/existing project
# 4. Set env var: $env:GEMINI_API_KEY="your-key"
```

**Groq Cloud:**
```bash
# 1. Go to https://console.groq.com
# 2. Login/Signup
# 3. Go to "API Keys" → Create key
# 4. Set env var: $env:GROQ_API_KEY="your-key"
```

## Troubleshooting
- *Key not working*: Verify the env var name matches what the provider expects. Restart the terminal after setting.
- *Quota exceeded*: Check the provider's free tier limits. Use telemetry to monitor consumption.
- *Provider down*: Use `token-miner` to find an alternative provider from the table above.
