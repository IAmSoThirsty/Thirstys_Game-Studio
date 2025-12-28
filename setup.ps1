# Setup script for Thirsty's Game Studio Agent System (Windows PowerShell)

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Thirsty's Game Studio Setup" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "Checking Python version..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Found: $pythonVersion" -ForegroundColor Green
    
    # Parse version number
    $version = $pythonVersion -replace "Python ", ""
    $versionParts = $version.Split(".")
    $majorVersion = [int]$versionParts[0]
    $minorVersion = [int]$versionParts[1]
    
    if ($majorVersion -lt 3 -or ($majorVersion -eq 3 -and $minorVersion -lt 8)) {
        Write-Host "ERROR: Python 3.8 or higher is required. Found: $version" -ForegroundColor Red
        exit 1
    }
}
catch {
    Write-Host "ERROR: Python is not installed or not in PATH." -ForegroundColor Red
    Write-Host "Please install Python 3.8 or higher from https://www.python.org/" -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host ""
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path ".venv") {
    Write-Host "Virtual environment already exists. Skipping creation." -ForegroundColor Green
}
else {
    python -m venv .venv
    Write-Host "Virtual environment created at .\.venv" -ForegroundColor Green
}

# Activate virtual environment
Write-Host ""
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host ""
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip setuptools wheel

# Install dependencies
Write-Host ""
Write-Host "Installing dependencies..." -ForegroundColor Yellow
if (Test-Path "requirements.txt") {
    pip install -r requirements.txt
    Write-Host "Base requirements installed." -ForegroundColor Green
}

# Install development dependencies (optional)
$devDeps = Read-Host "Install development dependencies? (y/n)"
if ($devDeps -eq "y" -or $devDeps -eq "Y") {
    if (Test-Path "requirements-dev.txt") {
        pip install -r requirements-dev.txt
        Write-Host "Development requirements installed." -ForegroundColor Green
    }
}

# Install package in editable mode
Write-Host ""
Write-Host "Installing package in editable mode..." -ForegroundColor Yellow
pip install -e .

# Create .env file if it doesn't exist
if (-not (Test-Path ".env")) {
    Write-Host ""
    Write-Host "Creating .env file from template..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host ".env file created. Please edit it with your API keys." -ForegroundColor Green
}

# Create output directory
if (-not (Test-Path "output")) {
    New-Item -ItemType Directory -Path "output" | Out-Null
}

Write-Host ""
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To activate the virtual environment, run:" -ForegroundColor Yellow
Write-Host "    .\.venv\Scripts\Activate.ps1"
Write-Host ""
Write-Host "To run the agent:" -ForegroundColor Yellow
Write-Host "    python -m agent.runner --output-dir output"
Write-Host ""
Write-Host "Or use the installed command:" -ForegroundColor Yellow
Write-Host "    thirsty-agent --output-dir output"
Write-Host ""
Write-Host "To deactivate the virtual environment:" -ForegroundColor Yellow
Write-Host "    deactivate"
Write-Host ""
Write-Host "Don't forget to configure your API keys in .env file!" -ForegroundColor Yellow
Write-Host "==================================" -ForegroundColor Cyan
