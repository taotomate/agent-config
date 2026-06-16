# Chrome Remote Debugging via Node.js on Windows

## Problem

The Hermes automated browser (Playwright) gets detected by Google and others. The solution: control the **user's real Chrome** (with their cookies/sessions) via Chrome DevTools Protocol (CDP).

However, launching Chrome with `--remote-debugging-port` from MSYS bash is broken:
- `cmd /c start` doesn't forward arguments properly to Chrome
- `&` backgrounding doesn't work for GUI processes
- `nohup`/`disown` don't work like on Linux
- `execute_code` can't access the D: drive

## Solution: launch via Node.js

Write a Node.js script that spawns Chrome with correct flags:

```javascript
const { exec } = require('child_process');
const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const args = [
  '--remote-debugging-port=9222',
  '--user-data-dir=C:\\Users\\user\\ChromeDebugProfile',
  '--no-first-run',
  '--no-default-browser-check'
];
const cmd = `"${chromePath}" ${args.join(' ')}`;
const child = exec(cmd, { windowsHide: true });
console.log('PID:', child.pid);

setTimeout(() => {
  const http = require('http');
  const req = http.get('http://localhost:9222/json/version', (res) => {
    let data = '';
    res.on('data', c => data += c);
    res.on('end', () => {
      console.log('STATUS:', res.statusCode);
      console.log(data);
    });
  });
  req.on('error', (e) => console.log('Not connected yet:', e.message));
  req.setTimeout(3000, () => req.destroy());
}, 7000);
```

## Critical pre-step

**Close ALL Chrome processes first.** If any `chrome.exe` is running, the new process just passes args to the existing instance and the debug flag is ignored.

```bash
cmd /c "taskkill /F /IM chrome.exe /T"
```

## Successful connection output

```json
{
  "Browser": "Chrome/143.0.7499.109",
  "Protocol-Version": "1.3",
  "webSocketDebuggerUrl": "ws://localhost:9222/devtools/browser/<uuid>"
}
```

## Notes

- `--user-data-dir` separates debug profile from normal profile
- The debug port (9222) allows direct CDP access for bot-like browsing with real user sessions
- File saved at `C:\\Users\\user\\launch_chrome_debug.js` for reuse
- **Node `ws` module required:** Not bundled with Node.js. Install first: `cd C:\Users\user && npm install ws`
- **CDP navigate is async:** `Page.navigate` returns immediately with `frameId`/`loaderId` but page loads asynchronously. Wait 8-12s before calling `Runtime.evaluate` for content.
- **No REST navigate endpoint:** There is no `/json/navigate` HTTP endpoint in Chrome DevTools. Navigation MUST go through WebSocket CDP commands.
- **Gemini shared links:** `gemini.google.com/share/...` links may return "Link doesn't exist" even with real session — they expire or are deleted by creator. Ask user to regenerate or paste content directly.
- **Reconnection:** If Chrome is restarted, the `webSocketDebuggerUrl` changes. Always re-fetch from `http://localhost:9222/json/list` before connecting.
