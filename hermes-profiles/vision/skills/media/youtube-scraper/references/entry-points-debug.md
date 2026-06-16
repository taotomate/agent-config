# Debugging: entry_points.txt Corruption by In-File Markers

## Symptom

`hermes doctor` crashes with:
```
TypeError: Pair.__new__() missing 1 required positional argument: 'value'
```
originating from `importlib.metadata` → `pydantic` → `openai` import chain.

## Root Cause

The Youtube Scraper v1 appended `<!-- youtube-scraper: processed -->` as a marker to every file it scanned, including `hermes_agent.egg-info/entry_points.txt`. 

`entry_points.txt` is a strict-format setuptools metadata file. Every non-blank line must be either:
- A section header: `[console_scripts]`
- An entry point: `name = module:path`

There is **no comment syntax**. Not `#`, not `<!-- -->`, nothing. Any line without `=` is parsed as an entry point and crashes `Pair.__new__()`.

## Fix

1. Remove the junk line from `entry_points.txt`
2. Upgrade scraper to v2 (DB-based tracking, no in-file markers)
3. Add `*.egg-info/` and `*.dist-info/` exclusion to directory scanner

## Detection Script

To find which package has a broken entry_points.txt:
```python
import importlib.metadata
for dist in importlib.metadata.distributions():
    try:
        _ = dist.entry_points
    except Exception as e:
        print(f'BROKEN: {dist.name} {dist.version} -> {e}')
```

## Lesson

**Never write markers/annotations into files you don't own — especially Python package metadata.** Use a separate tracking mechanism (SQLite, sidecar file, xattrs) instead.
