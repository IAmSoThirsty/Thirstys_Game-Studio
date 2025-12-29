.PHONY: help install install-dev setup clean test lint format run docker-build docker-run docker-clean venv

# Default target
help:
	@echo "Thirsty's Game Studio - Available Commands"
	@echo "==========================================="
	@echo ""
	@echo "Setup:"
	@echo "  make setup         - Complete setup (venv + install)"
	@echo "  make venv          - Create virtual environment"
	@echo "  make install       - Install base dependencies"
	@echo "  make install-dev   - Install dev dependencies"
	@echo ""
	@echo "Development:"
	@echo "  make run           - Run the agent system"
	@echo "  make test          - Run tests"
	@echo "  make lint          - Run linters"
	@echo "  make format        - Format code with black"
	@echo "  make clean         - Clean build artifacts"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build  - Build Docker image"
	@echo "  make docker-run    - Run agent in Docker"
	@echo "  make docker-clean  - Remove Docker containers/images"
	@echo ""

# Setup everything
setup: venv install
	@echo "Setup complete! Activate with: source .venv/bin/activate"

# Create virtual environment
venv:
	@echo "Creating virtual environment..."
	@test -d .venv || python3 -m venv .venv
	@echo "Virtual environment created at .venv"
	@echo "Activate with: source .venv/bin/activate"

# Install base dependencies
install:
	@echo "Installing dependencies..."
	@. .venv/bin/activate && pip install --upgrade pip setuptools wheel
	@. .venv/bin/activate && pip install -r requirements.txt
	@. .venv/bin/activate && pip install -e .
	@echo "Base dependencies installed"

# Install development dependencies
install-dev: install
	@echo "Installing development dependencies..."
	@. .venv/bin/activate && pip install -r requirements-dev.txt
	@echo "Development dependencies installed"

# Run the agent
run:
	@echo "Running agent system..."
	@. .venv/bin/activate && python -m agent.runner --output-dir output

# Run tests
test:
	@echo "Running tests..."
	@. .venv/bin/activate && pytest tests/ -v --cov=agent --cov-report=term-missing

# Run linters
lint:
	@echo "Running linters..."
	@. .venv/bin/activate && flake8 agent/
	@. .venv/bin/activate && mypy agent/
	@. .venv/bin/activate && pylint agent/

# Format code
format:
	@echo "Formatting code..."
	@. .venv/bin/activate && black agent/
	@. .venv/bin/activate && isort agent/

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	@rm -rf build/ dist/ *.egg-info
	@rm -rf .pytest_cache .coverage htmlcov .mypy_cache .tox
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@find . -type f -name "*.pyo" -delete
	@echo "Clean complete"

# Docker build
docker-build:
	@echo "Building Docker image..."
	@docker build -t thirsty-game-studio-agent:latest .
	@echo "Docker image built"

# Docker run
docker-run:
	@echo "Running agent in Docker..."
	@docker-compose up agent

# Docker clean
docker-clean:
	@echo "Cleaning Docker resources..."
	@docker-compose down -v
	@docker rmi thirsty-game-studio-agent:latest 2>/dev/null || true
	@echo "Docker resources cleaned"

# Install system dependencies for Android build
android-deps:
	@echo "Note: Android requires Android Studio and JDK 17+"
	@echo "Please install manually from:"
	@echo "  - Android Studio: https://developer.android.com/studio"
	@echo "  - JDK 17: https://adoptium.net/"

# Build Android app
android-build:
	@echo "Building Android app..."
	@cd android/ThirstysGame && ./gradlew assembleDebug
	@echo "Android APK built at android/ThirstysGame/app/build/outputs/apk/debug/"
