@echo off
REM sync-agent-config.bat — Synchronize project with agent-config

set AGENT_CONFIG=%~dp0
REM Update this path if agent-config is not in the same directory as this script

echo === agent-config sync ===

REM Check agent-config exists
if not exist "%AGENT_CONFIG%" (
    echo ERROR: agent-config not found at %AGENT_CONFIG%
    exit /b 1
)

REM Sync skill registry
echo Syncing skill registry...
if not exist ".config" mkdir .config
copy "%AGENT_CONFIG%\.config\skill-registry.md" .config\skill-registry.md /Y

REM Verify critical files
echo Verifying critical paths...
if exist "%AGENT_CONFIG%\agents\base.md" (
    echo   OK: %AGENT_CONFIG%\agents\base.md
) else (
    echo   MISSING: %AGENT_CONFIG%\agents\base.md
)

if exist "%AGENT_CONFIG%\.config\GOVERNANCE_PROTOCOL.md" (
    echo   OK: %AGENT_CONFIG%\.config\GOVERNANCE_PROTOCOL.md
) else (
    echo   MISSING: %AGENT_CONFIG%\.config\GOVERNANCE_PROTOCOL.md
)

if exist "%AGENT_CONFIG%\shared\audit-framework.md" (
    echo   OK: %AGENT_CONFIG%\shared\audit-framework.md
) else (
    echo   MISSING: %AGENT_CONFIG%\shared\audit-framework.md
)

REM Verify AGENTS.md inheritance
echo Checking AGENTS.md inheritance...
findstr /C:"inherited_from: %AGENT_CONFIG%\agents\base.md" AGENTS.md >nul 2>&1
if %errorlevel% equ 0 (
    echo   OK: AGENTS.md inherits from base.md
) else (
    echo   WARNING: AGENTS.md may not inherit from base.md
)

echo === Sync complete ===
