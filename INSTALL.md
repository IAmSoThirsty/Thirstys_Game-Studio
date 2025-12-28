# Installation Guide

This guide will help you set up the Thirsty's Game Studio development environment.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Manual Setup](#manual-setup)
- [Docker Setup](#docker-setup)
- [Development Setup](#development-setup)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### Required

- **Python 3.8 or higher** (3.12 recommended)
- **pip** (Python package manager)
- **Git**

### Optional

- **Docker** and **Docker Compose** (for containerized deployment)
- **Android Studio** and **JDK 17+** (for Android app development)
- **Make** (for using Makefile commands)

### Installing Prerequisites

#### Ubuntu/Debian

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv git make
```

#### macOS

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install python git make
```

#### Windows

1. Install [Python](https://www.python.org/downloads/) (3.8+)
2. Install [Git](https://git-scm.com/download/win)
3. Install [Docker Desktop](https://www.docker.com/products/docker-desktop) (optional)

## Quick Start

### Using Setup Script (Recommended)

#### Unix/Linux/macOS

```bash
# Clone the repository
git clone https://github.com/IAmSoThirsty/Thirstys_Game-Studio.git
cd Thirstys_Game-Studio

# Run setup script
chmod +x setup.sh
./setup.sh

# Activate virtual environment
source .venv/bin/activate

# Configure API keys
nano .env  # or use your preferred editor
```

#### Windows (PowerShell)

```powershell
# Clone the repository
git clone https://github.com/IAmSoThirsty/Thirstys_Game-Studio.git
cd Thirstys_Game-Studio

# Run setup script
.\setup.ps1

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Configure API keys
notepad .env
```

### Using Makefile (Unix/Linux/macOS)

```bash
# Complete setup
make setup

# Activate virtual environment
source .venv/bin/activate

# Configure API keys
nano .env
```

## Manual Setup

If you prefer to set up everything manually:

### 1. Clone Repository

```bash
git clone https://github.com/IAmSoThirsty/Thirstys_Game-Studio.git
cd Thirstys_Game-Studio
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
# On Unix/Linux/macOS:
source .venv/bin/activate

# On Windows:
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip setuptools wheel

# Install base requirements
pip install -r requirements.txt

# Install the package in editable mode
pip install -e .

# Optional: Install development dependencies
pip install -r requirements-dev.txt
```

### 4. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit with your API keys
nano .env  # or your preferred editor
```

### 5. Create Output Directory

```bash
mkdir -p output
```

## Docker Setup

### Using Docker Compose (Recommended)

```bash
# Build and run
docker-compose up agent

# Run in background
docker-compose up -d agent

# View logs
docker-compose logs -f agent

# Stop containers
docker-compose down
```

### Using Docker Directly

```bash
# Build image
docker build -t thirsty-game-studio-agent:latest .

# Run container
docker run -v $(pwd)/output:/app/output \
  --env-file .env \
  thirsty-game-studio-agent:latest
```

### Development with Docker

```bash
# Start development container with shell access
docker-compose --profile dev run --rm agent-dev

# Inside container
python -m agent.runner --output-dir /app/output
```

## Development Setup

For active development, install additional tools:

```bash
# With setup script
./setup.sh  # Choose 'y' when asked about dev dependencies

# With Makefile
make install-dev

# Manually
pip install -r requirements-dev.txt
```

### Development Tools Included

- **pytest** - Testing framework
- **black** - Code formatter
- **flake8** - Linter
- **mypy** - Type checker
- **pylint** - Code analyzer
- **sphinx** - Documentation generator

### Using Development Tools

```bash
# Format code
make format
# or
black agent/

# Run linter
make lint
# or
flake8 agent/

# Run tests
make test
# or
pytest tests/
```

## Verification

### Test Python Environment

```bash
# Check Python version
python --version

# Test agent runner
python -m agent.runner --help

# Or use installed command
thirsty-agent --help
```

### Test Agent System

```bash
# Run agent with test output
python -m agent.runner --output-dir output

# Check output directory
ls -la output/
```

### Expected Output

```
output/
├── f2p_policy.md
├── pr_template.md
└── (other generated artifacts)
```

## Project Structure

```
.
├── .venv/                   # Virtual environment (created during setup)
├── agent/                   # Python agent system
├── android/                 # Android app
├── cpp/                     # C++ interfaces
├── dotnet/                  # .NET interfaces
├── web/                     # Web interfaces
├── output/                  # Generated artifacts
├── tests/                   # Test files
├── .env                     # Environment configuration (create from .env.example)
├── requirements.txt         # Base dependencies
├── requirements-dev.txt     # Development dependencies
├── setup.py                 # Package setup
├── pyproject.toml          # Modern Python packaging
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker orchestration
├── Makefile                # Common commands
├── setup.sh                # Unix setup script
└── setup.ps1               # Windows setup script
```

## Troubleshooting

### Python Version Issues

```bash
# Check Python version
python --version  # or python3 --version

# If version is too old, install newer Python:
# Ubuntu/Debian
sudo apt install python3.12

# macOS
brew install python@3.12
```

### Virtual Environment Issues

```bash
# Deactivate current environment
deactivate

# Remove old virtual environment
rm -rf .venv

# Create new virtual environment
python3 -m venv .venv

# Reactivate
source .venv/bin/activate
```

### Permission Issues (Unix/Linux/macOS)

```bash
# Make scripts executable
chmod +x setup.sh
chmod +x gradlew
```

### Docker Issues

```bash
# Check Docker is running
docker ps

# Clean up Docker resources
docker-compose down -v
docker system prune -a

# Rebuild from scratch
docker-compose build --no-cache
```

### Import Errors

```bash
# Ensure package is installed in editable mode
pip install -e .

# Verify installation
pip list | grep thirsty
```

### API Key Issues

Make sure your `.env` file contains valid API keys:

```bash
# Check .env file exists
ls -la .env

# Edit .env file with your keys
nano .env
```

Required keys:
- `REDDIT_CLIENT_ID` and `REDDIT_CLIENT_SECRET`
- `DISCORD_BOT_TOKEN` and `DISCORD_GUILD_ID`
- `STEAM_API_KEY` and `STEAM_APP_ID`

## Next Steps

After installation:

1. **Configure API Keys** - Edit `.env` with your credentials
2. **Run the Agent** - `python -m agent.runner --output-dir output`
3. **Check Output** - Review generated artifacts in `output/`
4. **Build Android App** - See [android/ThirstysGame/README.md](android/ThirstysGame/README.md)
5. **Read Documentation** - See [docs/TEAM_AGENT_DESIGN.md](docs/TEAM_AGENT_DESIGN.md)

## Getting Help

- **Issues**: [GitHub Issues](https://github.com/IAmSoThirsty/Thirstys_Game-Studio/issues)
- **Documentation**: [docs/](docs/)
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)

## Additional Resources

- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)
- [Docker Documentation](https://docs.docker.com/)
- [Android Development](https://developer.android.com/)
- [GitHub Actions](https://docs.github.com/en/actions)
