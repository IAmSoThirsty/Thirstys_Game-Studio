# Development Setup Guide

This guide covers the complete setup process for developing Thirsty's Game Studio.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Python Agent Setup](#python-agent-setup)
3. [Android App Setup](#android-app-setup)
4. [Docker Setup](#docker-setup)
5. [IDE Configuration](#ide-configuration)
6. [Common Tasks](#common-tasks)

## Prerequisites

### System Requirements

- **Operating System**: Linux, macOS, or Windows 10/11
- **RAM**: 8GB minimum, 16GB recommended
- **Disk Space**: 10GB free space

### Required Software

#### All Platforms

- **Python 3.8+** (3.12 recommended)
  - Linux/Mac: Usually pre-installed, or install via package manager
  - Windows: Download from [python.org](https://www.python.org/downloads/)
  
- **Git**
  - Linux: `sudo apt install git` or `sudo yum install git`
  - Mac: `brew install git`
  - Windows: Download from [git-scm.com](https://git-scm.com/)

#### For Android Development

- **Android Studio Arctic Fox or later**
  - Download from [developer.android.com](https://developer.android.com/studio)
  
- **JDK 17 or higher**
  - Included with Android Studio, or download from [adoptium.net](https://adoptium.net/)

#### For Docker (Optional)

- **Docker Desktop**
  - Linux: Install Docker Engine from [docs.docker.com](https://docs.docker.com/engine/install/)
  - Mac/Windows: Download Docker Desktop from [docker.com](https://www.docker.com/products/docker-desktop)

## Python Agent Setup

### Quick Setup with Scripts

#### Unix/Linux/macOS

```bash
# Navigate to project root
cd Thirstys_Game-Studio

# Run setup script
chmod +x setup.sh
./setup.sh

# Activate virtual environment
source .venv/bin/activate
```

#### Windows PowerShell

```powershell
# Navigate to project root
cd Thirstys_Game-Studio

# Run setup script
.\setup.ps1

# Activate virtual environment
.\.venv\Scripts\Activate.ps1
```

### Manual Setup

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # Unix/Mac
# OR
.\.venv\Scripts\Activate.ps1  # Windows

# Upgrade pip
pip install --upgrade pip setuptools wheel

# Install dependencies
pip install -r requirements.txt

# Install in editable mode
pip install -e .
```

### Install Development Dependencies

```bash
# Activate virtual environment first
source .venv/bin/activate

# Install dev dependencies
pip install -r requirements-dev.txt
```

### Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit with your API keys
nano .env  # or use your preferred editor
```

Required environment variables:
- `REDDIT_CLIENT_ID` - From https://www.reddit.com/prefs/apps
- `REDDIT_CLIENT_SECRET`
- `DISCORD_BOT_TOKEN` - From https://discord.com/developers/applications
- `DISCORD_GUILD_ID`
- `STEAM_API_KEY` - From https://steamcommunity.com/dev/apikey
- `STEAM_APP_ID`

## Android App Setup

### Open in Android Studio

1. Launch Android Studio
2. Select "Open an existing project"
3. Navigate to `android/ThirstysGame`
4. Wait for Gradle sync to complete

### Command Line Build

```bash
# Navigate to Android project
cd android/ThirstysGame

# Build debug APK
./gradlew assembleDebug

# Build release APK (requires signing configuration)
./gradlew assembleRelease

# Install to connected device
./gradlew installDebug

# Run tests
./gradlew test
```

### Troubleshooting Android Build

If Gradle sync fails:

```bash
# Clean build
./gradlew clean

# Refresh dependencies
./gradlew --refresh-dependencies
```

## Docker Setup

### Build Docker Image

```bash
# Build image
docker build -t thirsty-game-studio-agent:latest .

# Or using docker-compose
docker-compose build
```

### Run with Docker Compose

```bash
# Run agent (one-time)
docker-compose up agent

# Run in background
docker-compose up -d agent

# View logs
docker-compose logs -f agent

# Stop containers
docker-compose down
```

### Development with Docker

```bash
# Start development container with shell
docker-compose --profile dev run --rm agent-dev

# Inside container, you have full access to the code
python -m agent.runner --output-dir /app/output
```

## IDE Configuration

### Visual Studio Code

Install recommended extensions:
- Python (Microsoft)
- Pylance
- Python Test Explorer
- Docker
- Kotlin (for Android development)

Add to `.vscode/settings.json`:

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": ["tests"],
  "[python]": {
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": true
    }
  }
}
```

### PyCharm

1. Open project in PyCharm
2. Configure Python interpreter:
   - File → Settings → Project → Python Interpreter
   - Add Interpreter → Existing environment
   - Select `.venv/bin/python`
3. Enable pytest:
   - Settings → Tools → Python Integrated Tools
   - Default test runner: pytest

## Common Tasks

### Running the Agent

```bash
# Activate virtual environment
source .venv/bin/activate

# Run agent
python -m agent.runner --output-dir output

# Or use installed command
thirsty-agent --output-dir output

# With different log level
thirsty-agent --log-level DEBUG

# JSON output
thirsty-agent --json-output
```

### Code Quality

```bash
# Format code
make format
# or
black agent/

# Run linter
make lint
# or
flake8 agent/

# Type checking
mypy agent/

# Run all checks
make lint && make test
```

### Testing

```bash
# Run all tests
make test
# or
pytest

# Run with coverage
pytest --cov=agent --cov-report=html

# Run specific test file
pytest tests/test_runner.py

# Run specific test
pytest tests/test_runner.py::test_runner_imports
```

### Building Documentation

```bash
# Install sphinx (included in requirements-dev.txt)
pip install -r requirements-dev.txt

# Build documentation (if configured)
cd docs
make html
```

### Clean Build Artifacts

```bash
# Using Makefile
make clean

# Manual cleanup
rm -rf build/ dist/ *.egg-info
rm -rf .pytest_cache .coverage htmlcov
find . -type d -name __pycache__ -exec rm -rf {} +
```

### Using Make Commands

```bash
# View all available commands
make help

# Complete setup
make setup

# Install dependencies
make install
make install-dev

# Run agent
make run

# Run tests
make test

# Lint code
make lint

# Format code
make format

# Docker operations
make docker-build
make docker-run
make docker-clean
```

## Virtual Environment Management

### Activating the Environment

Always activate the virtual environment before working:

```bash
# Unix/Linux/macOS
source .venv/bin/activate

# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# Windows CMD
.venv\Scripts\activate.bat
```

### Deactivating

```bash
deactivate
```

### Recreating Virtual Environment

If you encounter issues:

```bash
# Deactivate first
deactivate

# Remove old environment
rm -rf .venv

# Create new environment
python3 -m venv .venv

# Activate and reinstall
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

## Troubleshooting

### Python Import Errors

```bash
# Ensure package is installed
pip install -e .

# Check PYTHONPATH
echo $PYTHONPATH

# Verify installation
pip list | grep thirsty
```

### Permission Errors (Unix/Linux)

```bash
# Make scripts executable
chmod +x setup.sh
chmod +x android/ThirstysGame/gradlew
```

### Android Gradle Issues

```bash
# Clean project
cd android/ThirstysGame
./gradlew clean

# Clear Gradle cache
rm -rf ~/.gradle/caches/
```

### Docker Build Issues

```bash
# Clean Docker cache
docker system prune -a

# Rebuild without cache
docker-compose build --no-cache
```

## Next Steps

After setup is complete:

1. **Configure API Keys** - Edit `.env` with your credentials
2. **Run Tests** - Ensure everything is working: `make test`
3. **Run Agent** - Test the agent system: `make run`
4. **Explore Code** - Review the [TEAM_AGENT_DESIGN.md](TEAM_AGENT_DESIGN.md)
5. **Read Contribution Guidelines** - See [CONTRIBUTING.md](../CONTRIBUTING.md)

## Additional Resources

- [INSTALL.md](../INSTALL.md) - Installation guide
- [README.md](../README.md) - Project overview
- [CONTRIBUTING.md](../CONTRIBUTING.md) - How to contribute
- [Android README](../android/ThirstysGame/README.md) - Android app details

## Getting Help

If you encounter issues:

1. Check this guide and [INSTALL.md](../INSTALL.md)
2. Search existing [GitHub Issues](https://github.com/IAmSoThirsty/Thirstys_Game-Studio/issues)
3. Create a new issue with:
   - Your OS and versions (Python, Java, etc.)
   - Error messages
   - Steps to reproduce
