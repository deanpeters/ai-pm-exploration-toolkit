# AI PM Toolkit Installer for Windows
# Cross-platform entry point for the production installer

param(
    [string]$Tier = "essentials"
)

# Map tier names to numbers
$TierArg = switch ($Tier) {
    "essentials" { "1" }
    "advanced"   { "2" }
    "full"       { "3" }
    default      { 
        Write-Error "Invalid tier '$Tier'. Use 'essentials', 'advanced', or 'full'."
        exit 1 
    }
}

Write-Host "🚀 Launching AI PM Toolkit Installer for Tier ${TierArg}..." -ForegroundColor Cyan

# Check for Python
$pythonCmd = $null
foreach ($cmd in @("python", "python3", "py")) {
    try {
        $version = & $cmd --version 2>$null
        if ($version -match "Python 3\.\d+") {
            $pythonCmd = $cmd
            break
        }
    }
    catch {
        continue
    }
}

if (-not $pythonCmd) {
    Write-Error "❌ Python 3 is required but not found."
    Write-Host "Please install Python 3 from: https://www.python.org/downloads/windows/" -ForegroundColor Yellow
    exit 1
}

# Check for PyYAML
try {
    & $pythonCmd -c "import yaml" 2>$null
}
catch {
    Write-Host "📦 Installing required Python dependencies..." -ForegroundColor Yellow
    & $pythonCmd -m pip install --user PyYAML
}

# Get the directory where this script is located
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Run the installer
$installerPath = Join-Path $ScriptDir "installer.py"
& $pythonCmd $installerPath --tier $TierArg $args