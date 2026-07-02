# User Preference: Everything over os.walk (2026-06)

## Signal
User said: "te dije que solo busques con everything, deja de ja de gastar recursos en tus pendenjadas, si te digo que lo hagas asi lo haces asi y punto"

## Rule
When the user asks to search for files or find things on the filesystem:
1. **FIRST**: Use Everything HTTP API (`http://127.0.0.1:80/?search=...`)
2. **NEVER**: Use `os.walk`, `terminal("cmd.exe /c ...")`, or MSYS `find` unless explicitly told to
3. **NEVER**: Waste time checking if the service is running, starting it, or verifying binaries

The HTTP API works as long as Everything GUI is running. That's the only check needed.

## Why
- `os.walk` is slow on large drives and wastes tokens/time
- The CLI `es.exe` may be a fake (cmd.exe renamed) — produces no output
- The HTTP API is instant and reliable
- User has been explicit and frustrated about this preference
