---
model_tier: inherited
name: cardputer-buddy
description: Iterate on the Cardputer-Adv MicroPython app bundle (Claude Buddy, Snake, Hello) after the device is already provisioned via m5-onboard. Use when the user wants to add a new app, push a single changed .py without re-flashing, watch device serial logs, or run a one-shot REPL command. Trigger on "add an app", "push to the cardputer", "tail the device", "run on the device", or follow-up work after /maker-setup.
---

## Execution Phases



**DRY-RUN RULE:** Before executing any destructive or external operation, first perform a dry-run to preview what will happen. Show the user what actions would be taken, then ask for confirmation before proceeding.
> **[UNIVERSAL DRY-RUN / SIMULATION RULE]**
> If the user requests execution in `--dry-run` mode or asks for a "simulation", the agent will **NOT** execute commands that alter system state or call destructive MCP tools in the Action Phase.
> Instead, the agent will print the exact payload (JSON, code block, or parameters) it planned to execute, and will wait for explicit human approval.
### 1. Preparation Phase
- Load references and verify prerequisites
- Resolve target scope

### 2. Action Phase
- Execute the main workflow (original content below preserves existing steps)

### 3. Verification Phase
- Verify output matches expected results

## Context & Triggers
**When to use this skill:**
- TODO: Add specific triggers for this skill
- Triggers: "cardputer-buddy", "use cardputer-buddy"



# Cardputer Buddy app bundle

The `buddy/` directory in the local `build-with-claude` clone is the MicroPython payload that `m5-onboard` installs onto `/flash/`. Work inside that clone.


## Prerequisites
- [ ] Read access to target files/directories
- [ ] Write access for auto-fix operations


## Device layout

```
/flash/
├── main.py              launcher menu (replaces UIFlow's boot flow)
├── buddy_*.py           shared libs (BLE, UI, state, protocol, chars)
├── burst_frames.py      sprite frames
└── apps/
    ├── claude_buddy.py  BLE client → Claude Desktop's Hardware Buddy
    ├── hello_cardputer.py
    └── snake.py
```

`main.py` scans `/flash/apps/` at boot and lists every `.py` as a menu entry. Drop a file into `buddy/device/apps/`, push it, and it appears on next boot.

## Adding an app

Crib from `buddy/device/apps/hello_cardputer.py` — smallest example of keyboard polling, font, and exit conventions. Then push without re-flashing:

```bash
python3 onboard/scripts/install_apps.py --port <PORT> --src buddy
```

`<PORT>` is whatever `detect.py` reported last run (e.g. `/dev/cu.usbmodem1101`, `/dev/ttyACM0`, `COM3`).

## Dev loop tooling (`buddy/scripts/`)

```bash
# Push a subset of files over USB-serial
python3 buddy/scripts/push.py --port <PORT> --files apps/snake.py

# Watch device logs
python3 buddy/scripts/tail_serial.py --port <PORT>

# One-shot REPL exec
python3 buddy/scripts/repl_run.py --port <PORT> --script "import os; print(os.listdir('/flash'))"
```


## Guardrails (Critical Rules)
- **NEVER** execute destructive operations without explicit user confirmation
- **ALWAYS** verify target exists before operating
- **ALWAYS** handle errors gracefully — skip with warning, don't crash

