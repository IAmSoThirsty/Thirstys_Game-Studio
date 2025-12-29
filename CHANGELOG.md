# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Complete Python packaging setup with `setup.py` and `pyproject.toml`
- Virtual environment support with `.venv`
- Development dependencies in `requirements-dev.txt`
- Docker support with `Dockerfile` and `docker-compose.yml`
- `.dockerignore` for optimized Docker builds
- `.env.example` template for environment configuration
- Automated setup scripts:
  - `setup.sh` for Unix/Linux/macOS
  - `setup.ps1` for Windows PowerShell
- `Makefile` with common development tasks
- Comprehensive documentation:
  - `INSTALL.md` - Installation guide
  - `docs/DEVELOPMENT_SETUP.md` - Development setup guide
  - `tests/README.md` - Testing documentation
- Test infrastructure:
  - `tests/` directory with pytest configuration
  - `tests/conftest.py` - pytest configuration
  - `tests/test_runner.py` - basic runner tests
- Entry point `thirsty-agent` command for easy CLI access
- `.gitkeep` in output directory to preserve structure
- Enhanced `.gitignore` with Python virtual environment exclusions

### Changed
- Updated `.gitignore` to exclude virtual environments and Python artifacts

## [0.1.0] - 2024-12-28

### Initial Release
- Multi-agent orchestration system for game development
- Community insights aggregation from Reddit, Discord, and Steam
- Feature proposal generation based on community sentiment
- F2P guardrails enforcement
- Android app with Jetpack Compose
- CI/CD workflows for GitHub Actions
