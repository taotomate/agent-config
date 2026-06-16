# Auto-Commit via File Watcher — Pattern Reference

## Problem
AI coding agents (OpenCode, Aider, etc.) suffer from context drift and forget to run `git commit` after making changes. This leads to lost work, inconsistent repo state, and reliance on the model's memory for mechanical tasks.

## Solution: Infrastructure-Level Auto-Commit
Decouple the commit action from the agent's memory by using a file watcher that automatically commits changes. The agent edits files freely; the infrastructure handles version control.

## Implementation: inotifywait Watcher (Linux/WSL)

```bash
#!/bin/bash
# auto-commit.sh — watches a repo and commits on any file change
REPO_DIR="${1:-.}"
cd "$REPO_DIR" || exit 1

echo "Watching $REPO_DIR for changes..."

while inotifywait -r -e modify,create,delete,move --exclude '\.git/' "$REPO_DIR" 2>/dev/null; do
    sleep 5
    if git diff --quiet && git diff --cached --quiet; then
        continue
    fi
    git add -A
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    CHANGED=$(git diff --cached --stat | tail -1)
    git commit -m "auto: $TIMESTAMP — $CHANGED" --no-verify
    echo "Auto-committed: $CHANGED"
done
```

## Implementation: Windows Alternative (PowerShell)

```powershell
$repoDir = $args[0] || "."
$lastCommit = [datetime]::MinValue
$debounceSeconds = 5

$watcher = New-Object System.IO.FileSystemWatcher
$watcher.Path = (Resolve-Path $repoDir).Path
$watcher.IncludeSubdirectories = $true
$watcher.EnableRaisingEvents = $true

$action = {
    $now = [datetime]::Now
    if (($now - $lastCommit).TotalSeconds -lt $debounceSeconds) { return }
    Push-Location $repoDir
    $status = git status --porcelain
    if ($status) {
        git add -A
        $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        git commit -m "auto: $ts" --no-verify
        $script:lastCommit = $now
    }
    Pop-Location
}

Register-ObjectEvent $watcher "Changed" -Action $action
Register-ObjectEvent $watcher "Created" -Action $action
while ($true) { Start-Sleep -Seconds 1 }
```

## Design Principles
- Agent autonomy preserved: agent doesn't need to know about the watcher
- Git as source of truth: every change committed with timestamp and diff stat
- Debounce prevents spam: 5-second quiet period before committing
- No-verify flag: skips pre-commit hooks to avoid infinite loops

## Alternative Approaches
- Aider's built-in auto-commit: Aider does this natively — every edit committed
- OpenCode + custom tool: Can be wired via MCP but still model-dependent
- Git hook post-checkout + alias wrapper: Less reliable, depends on git commands
