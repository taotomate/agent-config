# scan-nightly.ps1
# Nightly graphify scan - small files first
# Runs via Windows Task Scheduler at 2:00 AM daily

$logDir = "D:\Engram_SDD\skills\graphify-proxy\logs"
$logFile = "$logDir\scan-$(Get-Date -Format 'yyyy-MM-dd').log"
$targetDir = "D:\Engram_SDD"
$tokenBudget = 30000

# Create log directory
New-Item -ItemType Directory -Path $logDir -Force | Out-Null

function Log($msg) {
    $ts = Get-Date -Format "HH:mm:ss"
    "$ts $msg" | Tee-Object -FilePath $logFile -Append
}

Log "=== Nightly Graphify Scan Started ==="

# Check if llama-server is already running
$llamaProc = Get-Process -Name "llama-server" -ErrorAction SilentlyContinue
if (-not $llamaProc) {
    Log "Starting llama-server..."
    $env:PATH = "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.8\bin;" + $env:PATH
    Start-Process "D:\llama-cuda\llama-server.exe" -ArgumentList `
        "--model", "D:\LLM-Llama.cpp\qwen2.5-coder-7b-instruct-q4_k_m.gguf", `
        "--port", "8081", `
        "--ctx-size", "65536", `
        "--n-gpu-layers", "99", `
        "--parallel", "4" `
        -WindowStyle Minimized
    Start-Sleep 8
    Log "llama-server started"
} else {
    Log "llama-server already running (PID: $($llamaProc.Id))"
}

# Start proxy if not running
$proxyProc = Get-Process -Name "python" -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*proxy.py*" }
if (-not $proxyProc) {
    Log "Starting proxy..."
    Start-Process python -ArgumentList "D:\Engram_SDD\skills\graphify-proxy\proxy.py" -WindowStyle Minimized
    Start-Sleep 3
    Log "Proxy started"
} else {
    Log "Proxy already running"
}

# Configure graphify to use proxy
$env:OPENAI_API_KEY = "dummy"
$env:OPENAI_BASE_URL = "http://localhost:8080/v1"

# Scan small files first (markdown, txt under 10KB)
Log "Scanning small files in $targetDir..."
graphify $targetDir --no-viz --backend openai --token-budget $tokenBudget 2>&1 | ForEach-Object { Log $_ }

Log "=== Nightly Scan Completed ==="
