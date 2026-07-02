# Handling Tool Failures on Windows
When encountering tool failures due to environment state (e.g., PATH issues, missing binaries) on Windows:
1. **Check if the tool is installed** — use `which` or equivalent.
2. **Verify PATH includes the tool's directory** — ensure it's in `%PATH%` or `PATH` env var.
3. **Install the tool manually** — download and place executable in a known location (e.g., `C:\Users\user\bin`).
4. **Add to PATH** — update system PATH or user environment variables to include the tool's directory.
5. **Test with absolute path** — if installation succeeds, test using full path before relying on `which`/PATH.

This approach ensures durability: failures are not hard-coded as 'this tool does not work' but resolved via setup steps that can be repeated or adapted for future sessions.
