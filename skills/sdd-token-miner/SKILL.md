-----
name: sdd-token-miner
description: >
  Guides the user through obtaining and managing free LLM credits from various providers.
  Ensures the "LLM Proxy Service Arsenal" is always stocked with low-cost or free tokens.
  Trigger: "buscar créditos", "token miner", "renovar tokens", "free tokens", "minar tokens".
license: MIT
metadata:
  author: gentleman-programming
  version: "1.1"
---

## Rules
1. **Diversity**: Always prioritize providers with generous free tiers (Google, Groq).
2. **Efficiency**: Recommend Flash/Small models for high-volume tasks (research, distillation).
3. **Safety**: Never store raw API keys in this file. Use environment variables or system-specific secrets.

## Provider Configuration Guide

### 1. Google AI Studio (Gemini)
- **Site**: [aistudio.google.com](https://aistudio.google.com)
- **Why**: 1500 RPM on Gemini 1.5 Flash (Free Tier).
- **Steps**:
  1. Login with any Google account.
  2. Click "Get API key".
  3. Create API key in new/existing project.

### 2. Groq Cloud (Llama/Mixtral)
- **Site**: [console.groq.com](https://console.groq.com)
- **Why**: Fastest inference in the market, great free tier.
- **Steps**:
  1. Login/Signup.
  2. Go to "API Keys".
  3. Create key.

### 3. Together AI
- **Site**: [together.ai](https://together.ai)
- **Why**: Access to almost all Open Source models (Llama 3, Qwen, DBRX).
- **Steps**:
  1. Sign up for $5-$25 initial credit.
  2. Copy API key from settings.

### 4. OpenRouter
- **Site**: [openrouter.ai](https://openrouter.ai)
- **Why**: Unified API for all models. Best for tracking multi-model usage.
- **Steps**:
  1. Sign up.
  2. Create "Key" with specific permissions/limits.

### 5. Anthropic Console
- **Site**: [console.anthropic.com](https://console.anthropic.com)
- **Why**: Highest intelligence (Claude 3.5 Sonnet).
- **Steps**:
  1. Sign up.
  2. Check for free initial credits in "Billing".

## Pro Tip
Use the `sdd-telemetry` skill to monitor which provider gives you the best "Intelligence per Dollar" ratio.
