---
name: web-research
description: "Web research and scraping when web_search is unavailable. Use when you need to find information on the internet, scrape provider pages, discover APIs, or research any topic. Covers: Google captcha avoidance, curl scraping limitations with modern SPAs, using LLMs as search proxies, GitHub topic scraping, and Playwright/MCP as the superior alternative."
version: 1.0.0
author: OWL
model_tier: medium
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [research, scraping, web, search, discovery]
    related_skills: [arxiv, blogwatcher, native-mcp]
---

## Execution Phases


**DRY-RUN RULE:** Before executing any destructive or external operation, first perform a dry-run to preview what will happen. Show the user what actions would be taken, then ask for confirmation before proceeding.
### 1. Preparation Phase
- Load references and verify prerequisites
- Resolve target scope

### 2. Action Phase
- Execute the main workflow (original content below preserves existing steps)

### 3. Verification Phase
- Verify output matches expected results

## Context & Triggers
**When to use this skill:**
- Triggers: "web-research", "use web-research"


# Web Research (No web_search Available)

When `web_search` tool is NOT available (common in some Hermes setups), use these techniques in priority order.


## Decision Tree: How to Search

```
Need to find something on the web?
│
├─ Is it a known URL or API endpoint?
│  └─ YES → curl directly (fastest)
│
├─ Is it a GitHub repo/topic?
│  └─ YES → curl raw.githubusercontent.com or GitHub topics page
│
├─ Is it a modern SPA (React/Next.js) page?
│  └─ YES → curl will FAIL (JS-rendered). Use browser tool or Playwright MCP.
│
├─ Is it Google search?
│  └─ YES → Google WILL captcha. Use alternatives below.
│
└─ General research / discovery?
   └─ Use LLM-as-search-proxy (see below)
```

## Technique 1: Direct API/Endpoint Scraping (Fastest)

For known URLs with server-rendered HTML:

```bash
# Works: static HTML pages, API endpoints returning JSON
curl -sL "https://example.com/page" -H "User-Agent: Mozilla/5.0"

# GitHub raw content (always works)
curl -sL "https://raw.githubusercontent.com/user/repo/main/README.md"

# GitHub topics (find curated lists)
curl -sL "https://github.com/topics/free-llm-api"
```

**LIMITATION**: Modern SPAs (React, Next.js, Vue) render everything via JavaScript. curl gets you a shell with `<div id="root"></div>` and no data. For these, you MUST use browser tool or Playwright.

## Technique 2: GitHub Topic Scraping (Best for Discovery)

GitHub topics are goldmines for curated lists:

```bash
# Find repos by topic
curl -sL "https://github.com/topics/free-llm-api"
curl -sL "https://github.com/topics/llm-api"
curl -sL "https://github.com/topics/openai-compatible"

# Then scrape the README of promising repos
curl -sL "https://raw.githubusercontent.com/USER/REPO/main/README.md"
```

This is how the `awesome-free-llm-apis` list was found in-session.

## Technique 3: LLM-as-Search-Proxy

When you need to discover unknown providers/services, query an LLM directly:

```python
import json, urllib.request

payload = json.dumps({
    'model': 'moonshotai/kimi-k2.6:free',  # or any available free model
    'messages': [{'role': 'user', 'content': 'List ALL free LLM API providers as of 2025-2026. For each: name, URL, free models, rate limits, needs API key. Be exhaustive.'}],
    'max_tokens': 5000,
    'temperature': 0.3
}).encode()

req = urllib.request.Request(
    'https://openrouter.ai/api/v1/chat/completions',
    data=payload,
    headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'}
)
resp = urllib.request.urlopen(req, timeout=60)
data = json.loads(resp.read())
print(data['choices'][0]['message']['content'])
```

**PITFALLS**:
- Free models have aggressive rate limits (429). Use paid models or add retry logic.
- LLMs may hallucinate URLs. Always verify links exist before using them.
- Cross-reference results from multiple LLMs for accuracy.
- Keep temperature low (0.3) for factual queries.

## Technique 4: Browser Tool (When Available)

The `browser` tool uses a real Chromium instance. It can handle:
- JavaScript-rendered SPAs
- Pages behind simple bot detection
- Login sessions (if already authenticated)

```python
# Navigate
browser_navigate(url="https://example.com")

# Get page content
browser_snapshot(full=True)

# Extract specific data via JS
browser_console(expression="document.querySelectorAll('a').length")
```

**PITFALLS**:
- Google WILL captcha the browser too (without residential proxies)
- Slow compared to curl
- Requires shadow DOM refs (@e1, @e2) not CSS selectors

## Technique 5: Playwright MCP (Superior — When Set Up)

**This is the best approach for serious web research.** Playwright controls a real browser programmatically:

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://example.com")
    page.wait_for_selector('.results')
    results = page.query_selector_all('.result__title a')
    for r in results:
        print(r.text_content(), '->', r.get_attribute('href'))
    browser.close()
```

**Advantages over browser tool**:
- No captchas when using your own browser profile/session
- CSS selectors (not shadow DOM refs)
- Can record and replay user actions
- Much faster for batch scraping

**Setup as MCP Server** (see `native-mcp` skill):
```yaml
mcp_servers:
  playwright:
    command: "npx"
    args: ["-y", "@your-playwright-mcp-server"]
    # OR run a custom Python MCP server wrapping Playwright
```

## Google Captcha Avoidance

Google will ALWAYS captcha automated requests. Alternatives:

| Method | Works? | Notes |
|--------|--------|-------|
| curl to google.com | ❌ | Instant captcha |
| browser tool to google.com | ❌ | Captcha without residential proxies |
| DuckDuckGo HTML | ⚠️ | Sometimes works, sometimes protected |
| Bing | ⚠️ | Less aggressive but still protected |
| Startpage | ⚠️ | Google results, less bot detection |
| **LLM proxy** | ✅ | Best alternative for discovery |
| **GitHub topics** | ✅ | Best for finding curated lists |
| **Direct provider APIs** | ✅ | Most reliable for structured data |

## Perplexity-Specific Pitfalls (2026)

**Perplexity is NOT reliably accessible:**

- **Browser**: Cloudflare blocks with "Performing security challenge" — cannot bypass without residential proxies
- **OpenRouter API** (`perplexity/sonar-pro`): Returns HTTP 402 (Payment Required) — not available on free tier
- **Direct API**: Requires a Perplexity API key (`PPLX_API_KEY`), which is separate from OpenRouter

**When user asks to "use Perplexity":**
1. Check if `PPLX_API_KEY` exists in secrets → use direct API if available
2. If not, fall back to LLM-as-search-proxy via OpenRouter (Gemini 2.5 Flash works well)
3. Use `curl` to GitHub raw READMEs for project-specific research
4. Use `browser_navigate` for GitHub topics/pages (works without login for public repos)
5. Tell the user Perplexity isn't available and what you used instead — don't just fail silently

## Multi-Source Fallback Pattern (Proven)

When researching a topic and primary source fails, execute ALL of these in parallel/rapid succession:

```
Source fails → immediately try next:
1. curl raw.githubusercontent.com/README.md (for known repos)
2. browser_navigate to GitHub topics/search
3. LLM proxy query (Gemini 2.5 Flash via OpenRouter)
4. browser_navigate to official site/docs
5. curl to specific API endpoints
```

**Key insight**: Never stop at one failure. The session that found the OpenCode/Antigravity/Hermes comparison used 4 different sources in sequence when Perplexity was blocked.

## Key Lesson: Be Proactive, Not Passive

**BAD**: "I searched Google and found nothing" → stops
**GOOD**: When one source fails, immediately try 3 more:
1. GitHub topics for curated lists
2. LLM proxy for discovery
3. Direct provider API endpoints
4. Known aggregator sites (awesome-lists, etc.)

The user explicitly called out: "no tengo que ser olgazán" (don't be lazy). When a search fails, don't report failure — report what you tried next.

## Key Lesson: Never Assume - Always Search

When the user mentions a system/widget/project:
1. **ALWAYS search for it first** — try GitHub, Google (via browser), and direct URLs
2. **NEVER assume it's private/just because you don't know about it**
3. If you can't find it, say "I couldn't find public info about X, can you share a link?"
4. Don't fabricate properties of systems you haven't verified

This applies to: provider names, model names, agent systems, any software the user mentions.

The user called out: "deja de inferir e inventar cosas" (stop inferring and making things up). When in doubt, search. When you can't search, ASK.

## Key Lesson: Ask Clarification About Research Output Format

Before conducting research:
1. **Ask what output format the user needs** — what columns, what sources, what scope
2. **Define the expected output before starting** — what constitutes a valid result vs noise
3. **Don't just dump raw data** — process and structure results before presenting

The user called out: "decime 3 cosas y dame las fuentes" — be specific about exactly what you're looking for and what format you need back.

## Key Lesson: Search Method — Simple First, Then Refine

**Correct approach:**
1. Start with a **generic search engine query** (Bing, DuckDuckGo HTML) — NOT GitHub, NOT specific sites
2. Based on initial results, **refine** — go to specific sites, GitHub repos, API docs
3. Cross-reference multiple sources

**Wrong approach (what I did):**
- Started with GitHub topics as first measure (too specific)
- Mixed curl scraping of SPAs (useless — JS-rendered)
- Didn't define output format before starting
- Dumped raw grep output without processing

**The user's method (Playwright/RL browser):**
- Record actions in real browser → replay as script
- Uses YOUR browser profile/session → no captchas
- CSS selectors (not shadow DOM refs)
- Much faster for batch scraping
- This is the SUPERIOR approach for web research when available

## Key Lesson: Don't Confuse User's Local Setup with Public Products

**Pitfall**: The user mentioned "Antigravity" and I assumed it was their private system. It was actually Google's Antigravity IDE — a public product launched in May 2026.

**Rule**: When the user mentions a product/system:
1. Search for it FIRST (Bing, official site, GitHub)
2. Check if it's a public product before assuming it's their private setup
3. The user configures/uses many public products (OpenCode, Hermes, Antigravity CLI, etc.) — don't assume they built it
4. **Use Bing as first search measure** — NOT GitHub, NOT specific sites. Bing is less aggressive with captchas than Google.
5. Define output format BEFORE searching — what data points, what columns, what scope

## Key Lesson: Memory Management is Proactive

**Pitfall**: Memory was full (2,195/2,200 chars) and I couldn't add new entries. The user had to tell me to clean up.

**Rule**: 
1. **Monitor memory usage** — if above 90%, proactively consolidate/remove old entries
2. **Before adding new entries**, check if there's space. If not, clean first.
3. **Consolidate related entries** — multiple small entries about the same topic should be merged
4. **Remove stale info** — if a project is complete or info is outdated, remove it
5. The `memory` tool's `replace` action requires EXACT `old_text` match — use `add` + `remove` pattern carefully

## Key Lesson: Research Output Must Be Structured

When the user asks "decime X cosas de Y software":
1. Define the exact data points needed BEFORE searching
2. Search with those specific data points in mind
3. Present results in a structured format (bullets, key:value)
4. Cite sources for each data point
5. Don't dump raw grep/curl output — process it first

**Example of GOOD output:**
```
**OpenCode** (fuente: https://opencode.ai)
- Agente de terminal open-source para coding
- 160K GitHub stars, 900+ contributors
- ACP: SÍ — tiene sección de ACP Support
- Creado por Anomaly
```

**Example of BAD output:**
```
OpenCode is an open source agent that helps you write code...
[50 lines of raw HTML grep output]
```

## Multi-Agent Architecture

For the specific architecture of Hermes + OpenCode + Antigravity CLI as multi-agent setup, see:
`references/multi-agent-architecture.md`

## Free LLM Providers Discovered (2025-2026)

See `references/free-llm-providers.md` for the full list discovered during research sessions.

Key providers NOT in the original DB:
- **Together AI** — free credits, Llama/Mistral models
- **Fireworks AI** — free credits, fast inference
- **Perplexity** — Sonar API, per-request pricing
- **Cerebras** — wafer-scale chip, competes with Groq on speed
- **Zhipu AI** — Chinese, GLM-4 Flash models, no published limits
- **GitHub Models** — GPT-4o free tier (10-15 RPM)
- **NVIDIA NIM** — credit-based, replenishes
- **Mistral** — 1 BILLION tokens/month free
- **freellmpool** — pools 18+ providers behind one OpenAI-compatible endpoint, NO API key needed for some (Pollinations, OVHcloud, Kilo Gateway)
- **OpenRouter AutoRouter** — auto-routes to free models as fallback
- **Pareto** — model selection/filtering layer

## Rate Limits Reference

See `references/ai-agent-comparison.md` for a detailed comparison of OpenCode, Antigravity, and Hermes-Nous agents (Jun 2026), including which can orchestrate which.

| Provider | Free Tier Limits | Notes |
|----------|-----------------|-------|
| Google Gemini | 15 RPM / 1,500 RPD (Flash) | No EU/UK |
| Mistral | 1 req/s / 1B tokens/month | Most generous |
| Groq | 30 RPM / 14,400 RPD / 6,000 TPM | 300-500 tok/s |
| Cerebras | 30 RPM / 60,000 TPM / 14,400 RPD | Wafer-scale |
| OpenRouter | 20 RPM / 200 RPD | Varies by backend |
| GitHub Models | 10-15 RPM / 50-150 RPD | Includes GPT-4o! |
| Cohere | 20 RPM / 1,000 req/month | Trial keys |


## Guardrails (Critical Rules)
- **NEVER** execute destructive operations without explicit user confirmation
- **ALWAYS** verify target exists before operating
- **ALWAYS** handle errors gracefully — skip with warning, don't crash

