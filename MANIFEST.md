# Project Manifest

This document lists all fundamental project files and their purposes.

## Python Package Files

### Core Setup Files
- **`setup.py`** - Python package setup script (setuptools-based)
- **`pyproject.toml`** - Modern Python package configuration (PEP 518)
- **`requirements.txt`** - Base runtime dependencies
- **`requirements-dev.txt`** - Development dependencies (testing, linting, etc.)

### Package Structure
- **`agent/`** - Main Python package directory
  - **`agent/__init__.py`** - Package initialization
  - **`agent/runner.py`** - Main entry point for agent system
  - **`agent/core/`** - Core interfaces and abstractions
  - **`agent/community/`** - Community data sources and analyzers
  - **`agent/monetization/`** - F2P guardrail enforcement
  - **`agent/comparative/`** - Competitive analysis utilities
  - **`agent/orchestration/`** - Task and worker management
  - **`agent/issues/`** - GitHub issue drafting
  - **`agent/prs/`** - PR template generation
  - **`agent/integration/`** - Integration utilities

## Virtual Environment

- **`.venv/`** - Python virtual environment (created during setup)
  - Contains isolated Python interpreter and packages
  - Excluded from git via `.gitignore`
  - Created with: `python3 -m venv .venv`
  - Activated with:
    - Unix/Linux/macOS: `source .venv/bin/activate`
    - Windows: `.venv\Scripts\Activate.ps1`

## Docker Files

- **`Dockerfile`** - Multi-stage Docker image definition
  - Builder stage: Compiles dependencies
  - Production stage: Minimal runtime image
  - Includes health check and proper labels

- **`docker-compose.yml`** - Docker orchestration configuration
  - `agent` service: Production agent runner
  - `agent-dev` service: Development container with shell access
  - Networks and volumes configured

- **`.dockerignore`** - Files to exclude from Docker build context
  - Optimizes build performance and image size

## Environment Configuration

- **`.env.example`** - Template for environment variables
  - Contains placeholders for API keys
  - Copy to `.env` and fill in real values
  - `.env` is excluded from git (in `.gitignore`)

## Setup Scripts

### Unix/Linux/macOS
- **`setup.sh`** - Automated setup script for Unix-like systems
  - Creates virtual environment
  - Installs dependencies
  - Sets up configuration
  - Executable: `chmod +x setup.sh`

### Windows
- **`setup.ps1`** - PowerShell setup script for Windows
  - Same functionality as `setup.sh`
  - PowerShell-compatible syntax
  - Run with: `.\setup.ps1`

## Build Automation

- **`Makefile`** - Build automation and common tasks
  - `make setup` - Complete setup
  - `make install` - Install dependencies
  - `make run` - Run agent system
  - `make test` - Run tests
  - `make lint` - Run linters
  - `make format` - Format code
  - `make docker-build` - Build Docker image
  - `make clean` - Clean artifacts
  - `make help` - Show all commands

## Testing

- **`tests/`** - Test directory
  - **`tests/__init__.py`** - Test package initialization
  - **`tests/conftest.py`** - Pytest configuration and fixtures
  - **`tests/test_runner.py`** - Basic runner tests
  - **`tests/README.md`** - Testing documentation
  - Tests run with: `pytest` or `make test`

## Documentation

- **`README.md`** - Main project documentation
- **`QUICKSTART.md`** - Quick start guide (5-minute setup)
- **`INSTALL.md`** - Comprehensive installation guide
- **`CONTRIBUTING.md`** - Contribution guidelines
- **`CHANGELOG.md`** - Version history and changes
- **`LICENSE`** - MIT License

### docs/ Directory
- **`docs/TEAM_AGENT_DESIGN.md`** - Agent system architecture
- **`docs/DEVELOPMENT_SETUP.md`** - Development setup guide

## Output Directory

- **`output/`** - Generated artifacts directory
  - **`output/.gitkeep`** - Preserves empty directory in git
  - Contains generated files:
    - `run_summary_*.json` - Agent run summaries
    - `proposals.json` - Feature proposals
    - `community_insights.json` - Community analysis
    - `drafted_issues.json` - Draft GitHub issues
    - `f2p_policy.md` - F2P policy document
    - `app_data.json` - App data for Android
    - `pr_template.md` - PR template

## Git Configuration

- **`.gitignore`** - Git ignore patterns
  - Virtual environments (`.venv/`, `venv/`, etc.)
  - Python artifacts (`__pycache__/`, `*.pyc`)
  - Build directories (`build/`, `dist/`)
  - IDE files (`.vscode/`, `.idea/`)
  - Environment files (`.env`)
  - Test artifacts (`.pytest_cache/`, `.coverage`)
  - Docker artifacts

## Android Project

- **`android/ThirstysGame/`** - Android application
  - Kotlin/Jetpack Compose app
  - See `android/ThirstysGame/README.md` for details
  - Build with: `./gradlew assembleDebug`

- **`app/`** - Android app module (Gradle project)
  - Contains source code and resources
  - `app/build.gradle` - App-level Gradle config

- **`build.gradle`** - Root Gradle build script
- **`settings.gradle`** - Gradle settings
- **`gradlew`** - Gradle wrapper (Unix/Linux/macOS)
- **`gradlew.bat`** - Gradle wrapper (Windows)
- **`gradle/`** - Gradle wrapper files

## Other Language Interfaces

- **`cpp/include/`** - C++ interface headers
  - For Unreal Engine or custom C++ game engines
  - `IGamingAgentPlugin.h`

- **`dotnet/AgentPlugin/`** - C# interface
  - For Unity integration
  - `IGamingAgentPlugin.cs`

- **`web/plugin/`** - TypeScript interface
  - For web-based games
  - `IGamingAgentPlugin.ts`

## CI/CD

- **`.github/workflows/`** - GitHub Actions workflows
  - `agent_team.yml` - Daily agent pipeline runs
  - `android_build.yml` - Android APK/AAB builds
  - `android-ci.yml` - Android CI checks

## Entry Points

### Command Line
After installation, these commands are available:

1. **`thirsty-agent`** - Installed CLI command
   ```bash
   thirsty-agent --output-dir output
   ```

2. **`python -m agent.runner`** - Module execution
   ```bash
   python -m agent.runner --output-dir output
   ```

3. **`make run`** - Makefile target
   ```bash
   make run
   ```

4. **Docker**
   ```bash
   docker-compose up agent
   ```

## Dependencies

### Runtime (requirements.txt)
- Currently: None (uses Python standard library only)
- Optional: praw, discord.py, requests, textblob, spacy

### Development (requirements-dev.txt)
- pytest - Testing framework
- pytest-cov - Coverage plugin
- pytest-asyncio - Async test support
- pytest-mock - Mocking utilities
- black - Code formatter
- flake8 - Linter
- mypy - Type checker
- pylint - Code analyzer
- isort - Import sorter
- sphinx - Documentation generator
- build - Package build tool
- twine - Package upload tool

## Configuration Files

### Python Tool Configuration (in pyproject.toml)
- **[tool.black]** - Black formatter settings
- **[tool.pytest.ini_options]** - Pytest configuration
- **[tool.mypy]** - MyPy type checker settings

## Directory Structure Summary

```
Thirstys_Game-Studio/
├── .venv/                      # Virtual environment (created)
├── agent/                      # Python package
├── android/                    # Android app
├── app/                        # Android app module
├── cpp/                        # C++ interfaces
├── docs/                       # Documentation
├── dotnet/                     # .NET interfaces
├── gradle/                     # Gradle wrapper
├── output/                     # Generated artifacts
├── tests/                      # Test files
├── web/                        # Web interfaces
├── .dockerignore              # Docker ignore file
├── .env.example               # Environment template
├── .gitignore                 # Git ignore file
├── CHANGELOG.md               # Version history
├── CONTRIBUTING.md            # Contribution guide
├── Dockerfile                 # Docker image definition
├── INSTALL.md                 # Installation guide
├── LICENSE                    # MIT License
├── Makefile                   # Build automation
├── QUICKSTART.md              # Quick start guide
├── README.md                  # Main documentation
├── build.gradle               # Root Gradle config
├── docker-compose.yml         # Docker orchestration
├── gradlew                    # Gradle wrapper (Unix)
├── gradlew.bat                # Gradle wrapper (Windows)
├── pyproject.toml             # Python project config
├── requirements-dev.txt       # Dev dependencies
├── requirements.txt           # Runtime dependencies
├── settings.gradle            # Gradle settings
├── setup.ps1                  # Windows setup script
└── setup.py                   # Python package setup
```

## Installation Verification Checklist

After setup, verify these exist:

- [ ] `.venv/` directory created
- [ ] `.venv/bin/python` (or `.venv\Scripts\python.exe` on Windows)
- [ ] Package installed: `pip list | grep thirsty`
- [ ] Command works: `thirsty-agent --help`
- [ ] Tests pass: `pytest tests/`
- [ ] Output directory: `output/` with `.gitkeep`
- [ ] Environment file: `.env` (copied from `.env.example`)

## Complete Setup Commands Reference

### Quick Setup (Automated)
```bash
./setup.sh                      # Unix/Linux/macOS
.\setup.ps1                     # Windows
```

### Manual Setup
```bash
python3 -m venv .venv
source .venv/bin/activate       # Unix/Linux/macOS
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
cp .env.example .env
```

### Verify Installation
```bash
thirsty-agent --help
pytest tests/
python -m agent.runner --output-dir output
```

### Docker Setup
```bash
docker-compose build
docker-compose up agent
```

---

**All files listed above are fundamental to the project and have been properly implemented and tested.**
