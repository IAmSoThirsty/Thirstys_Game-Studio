# Quick Start Guide

Get up and running with Thirsty's Game Studio in 5 minutes!

## Prerequisites

- Python 3.8+ (3.12 recommended)
- Git

## Installation

### Option 1: Automated Setup (Recommended)

#### Unix/Linux/macOS

```bash
git clone https://github.com/IAmSoThirsty/Thirstys_Game-Studio.git
cd Thirstys_Game-Studio
chmod +x setup.sh
./setup.sh
source .venv/bin/activate
```

#### Windows PowerShell

```powershell
git clone https://github.com/IAmSoThirsty/Thirstys_Game-Studio.git
cd Thirstys_Game-Studio
.\setup.ps1
.\.venv\Scripts\Activate.ps1
```

### Option 2: Using Makefile (Unix/Linux/macOS only)

```bash
git clone https://github.com/IAmSoThirsty/Thirstys_Game-Studio.git
cd Thirstys_Game-Studio
make setup
source .venv/bin/activate
```

### Option 3: Docker

```bash
git clone https://github.com/IAmSoThirsty/Thirstys_Game-Studio.git
cd Thirstys_Game-Studio
cp .env.example .env
docker-compose up agent
```

## First Run

### Run the Agent System

```bash
# Make sure virtual environment is activated
python -m agent.runner --output-dir output

# Or use the installed command
thirsty-agent --output-dir output
```

Expected output:
```
============================================================
Agent Team Run Complete!
============================================================
Successful tasks: 5
Failed tasks: 0
Total execution time: 0.00s

Generated artifacts:
  - run_summary: output/run_summary_*.json
  - proposals: output/proposals.json
  - insights: output/community_insights.json
  - issues: output/drafted_issues.json
  - f2p_policy: output/f2p_policy.md
  - app_data: output/app_data.json
  - pr_template: output/pr_template.md
============================================================
```

### Check the Output

```bash
ls -la output/
```

You should see generated JSON files and markdown documents containing:
- Community insights analysis
- Feature proposals
- F2P policy documents
- Draft GitHub issues
- PR templates

## Configuration (Optional)

To enable real API integrations, edit `.env`:

```bash
cp .env.example .env
nano .env  # or your preferred editor
```

Add your API keys:
- Reddit API: Get from https://www.reddit.com/prefs/apps
- Discord Bot: Get from https://discord.com/developers/applications
- Steam API: Get from https://steamcommunity.com/dev/apikey

## Common Commands

### Python Agent

```bash
# Run with different log level
thirsty-agent --log-level DEBUG

# Output as JSON
thirsty-agent --json-output

# Custom output directory
thirsty-agent --output-dir /path/to/output
```

### Using Makefile

```bash
make help          # Show all available commands
make run           # Run the agent
make test          # Run tests
make lint          # Run linters
make format        # Format code
make clean         # Clean build artifacts
```

### Docker

```bash
# Run agent
docker-compose up agent

# Run in background
docker-compose up -d agent

# View logs
docker-compose logs -f agent

# Stop
docker-compose down
```

## Build Android App

```bash
cd android/ThirstysGame
./gradlew assembleDebug
```

APK will be at: `android/ThirstysGame/app/build/outputs/apk/debug/`

## Next Steps

1. **Explore the Output** - Check the `output/` directory for generated artifacts
2. **Configure APIs** - Add your API keys to `.env` for real data
3. **Run Tests** - `make test` or `pytest`
4. **Build Android** - See `android/ThirstysGame/README.md`
5. **Read Documentation** - Check `docs/TEAM_AGENT_DESIGN.md`

## Troubleshooting

### "Python not found"
Install Python 3.8+ from https://www.python.org/

### "Virtual environment activation failed"
```bash
# Recreate virtual environment
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
```

### "Import errors"
```bash
# Reinstall package
pip install -e .
```

### "Docker build fails"
```bash
# Clean and rebuild
docker-compose down -v
docker system prune -a
docker-compose build --no-cache
```

## Getting Help

- 📖 Full installation guide: [INSTALL.md](INSTALL.md)
- 🛠️ Development setup: [docs/DEVELOPMENT_SETUP.md](docs/DEVELOPMENT_SETUP.md)
- 🤝 Contributing: [CONTRIBUTING.md](CONTRIBUTING.md)
- 🐛 Issues: [GitHub Issues](https://github.com/IAmSoThirsty/Thirstys_Game-Studio/issues)

## System Requirements

- **OS**: Linux, macOS, Windows 10/11
- **RAM**: 4GB minimum, 8GB recommended
- **Disk**: 2GB free space
- **Python**: 3.8+ (3.12 recommended)
- **Docker**: Optional, for containerized deployment
- **Android Studio**: Optional, for Android app development

---

**Ready to contribute?** Check out [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines!
