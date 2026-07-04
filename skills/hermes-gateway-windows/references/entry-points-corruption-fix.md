# Fix: hermes doctor crashes — corrupt entry_points.txt

**Date:** 2026-06-07
**Symptom:** `hermes doctor` crashes immediately with:
```
TypeError: Pair.__new__() missing 1 required positional argument: 'value'
```
Traceback goes through `importlib.metadata` → pydantic plugin loader → openai import chain.

## Root Cause

The file `hermes_agent.egg-info/entry_points.txt` in the source tree contained a non-standard line injected by a youtube-scraper tool:

```html
<!-- youtube-scraper: processed -->
```

Python 3.11's `importlib.metadata` parser expects every non-blank, non-section-header line in `entry_points.txt` to follow the format `name = value`. An HTML comment line has no `=`, causing `Pair.parse()` to fail.

## Diagnosis Script

```python
python -c "
import importlib.metadata
for dist in importlib.metadata.distributions():
    try:
        eps = dist.entry_points
    except Exception as e:
        print(f'BROKEN: {dist.name} {dist.version} -> {e}')
"
```

This identified `hermes-agent 0.15.1` as the broken package.

## Fix

1. Locate the corrupt file:
   - Check `<package>.egg-info/entry_points.txt` (editable install)
   - Check `<package>-<version>.dist-info/entry_points.txt` (venv site-packages)

2. Read the file. In this case the egg-info version had:
   ```
   [console_scripts]
   hermes = hermes_cli.main:main
   hermes-acp = acp_adapter.entry:main
   hermes-agent = run_agent:main


   <!-- youtube-scraper: processed -->
   ```

3. Rewrite with only valid entries:
   ```
   [console_scripts]
   hermes = hermes_cli.main:main
   hermes-acp = acp_adapter.entry:main
   hermes-agent = run_agent:main
   ```

4. Verify: re-run the diagnosis script or `hermes doctor` directly.

## Key Files in This Setup

- Corrupt: `D:\Engram_SDD\Hermes-Nous\hermes-agent\hermes_agent.egg-info\entry_points.txt`
- Clean: `D:\Engram_SDD\Hermes-Nous\hermes-agent\venv\Lib\site-packages\hermes_agent-0.15.1.dist-info\entry_points.txt`

The `.dist-info/` copy in the venv was already clean — only the `.egg-info/` in the source tree was corrupted.

## General Lesson

Any tool that injects text into Python package metadata files (`.egg-info/`, `.dist-info/`) can break `importlib.metadata` parsing. The error is always the same cryptic `Pair.__new__()` TypeError regardless of what the corrupt line contains. When you see this error, scan all distributions for broken entry points rather than assuming it's a pydantic or openai bug.
