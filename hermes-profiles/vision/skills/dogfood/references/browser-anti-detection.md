# Browser Anti-Detection Strategies

## Problem
Automated browsers (Playwright/Puppeteer) are detected by bot protection (Cloudflare, Google, etc.). Symptoms:
- Cookie consent dialogs that won't dismiss
- "Before you continue to Google" blocking content
- 403/429 responses

## Strategy 1: Chrome Remote Debugging (Best)

Use the user's real Chrome with their real cookies/session.

**Setup:**
1. Close Chrome completely
2. Reopen with:
```
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\Users\user\ChromeDebugProfile"
```
3. The `--user-data-dir` creates a separate debug profile
4. Connect via CDP on `localhost:9222`

**Pros:** Real session, real fingerprint, undetectable
**Cons:** Requires Chrome restart, separate profile

## Strategy 2: Playwright Stealth

- `playwright-stealth` plugin
- Rotate User-Agents
- Human-like behavior (scrolls, pauses, mouse movements)
- Disable `navigator.webdriver`

**Limitations:** Still detectable by Google and advanced protection

## Strategy 3: Firefox + Anti-Fingerprint

- Canvas Blocker, Chameleon, Trace, JShelter
- LibreWolf (hardened Firefox fork)

## Strategy 4: Hybrid (Recommended)

- Chrome Remote Debugging for Google/social media
- Hardened Firefox for general browsing
- Playwright only for sites without bot protection

## Hermes-Specific Notes

- Built-in `browser` tool uses Playwright — detected by Google
- For `gemini.google.com/share/...` links: ask user to paste content
- `curl` with cookies also detected by Google
- Chrome Remote Debugging is the only reliable way to access Google services
