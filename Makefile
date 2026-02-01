.PHONY: help install install-dev setup clean test lint format run docker-build docker-run docker-clean venv game-build game-run game-docker deploy-all

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
	@echo "  make game-run      - Run the game"
	@echo "  make test          - Run all tests"
	@echo "  make test-game     - Run game tests only"
	@echo "  make lint          - Run linters"
	@echo "  make format        - Format code with black"
	@echo "  make clean         - Clean build artifacts"
	@echo ""
	@echo "Docker - Agent:"
	@echo "  make docker-build  - Build Docker image (agent)"
	@echo "  make docker-run    - Run agent in Docker"
	@echo "  make docker-clean  - Remove Docker containers/images"
	@echo ""
	@echo "Docker - Game:"
	@echo "  make game-build    - Build game Docker image"
	@echo "  make game-docker   - Run game in Docker (headless)"
	@echo ""
	@echo "Production Deployment:"
	@echo "  make deploy-all    - Deploy complete stack (agent + game)"
	@echo "  make deploy-game   - Deploy game only"
	@echo "  make deploy-stop   - Stop all services"
	@echo "  make deploy-status - Check deployment status"
	@echo ""
	@echo "Android:"
	@echo "  make android-build - Build Android APK"
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

# Run the game
game-run:
	@echo "Running Thirsty's Game..."
	@. .venv/bin/activate && python main.py

# Run tests
test:
	@echo "Running all tests..."
	@. .venv/bin/activate && pytest tests/ -v

# Run game tests only
test-game:
	@echo "Running game tests..."
	@. .venv/bin/activate && pytest tests/test_engine.py tests/test_components.py tests/test_systems.py tests/test_save_system.py -v

# Run linters
lint:
	@echo "Running linters..."
	@. .venv/bin/activate && flake8 agent/ app/ || true
	@. .venv/bin/activate && mypy agent/ app/ || true

# Format code
format:
	@echo "Formatting code..."
	@. .venv/bin/activate && black agent/ app/ tests/
	@. .venv/bin/activate && isort agent/ app/ tests/

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	@rm -rf build/ dist/ *.egg-info
	@rm -rf .pytest_cache .coverage htmlcov .mypy_cache .tox
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@find . -type f -name "*.pyo" -delete
	@rm -rf saves/ output/
	@echo "Clean complete"

# Docker build - Agent
docker-build:
	@echo "Building Docker image (agent)..."
	@docker build -t thirsty-game-studio-agent:latest -f Dockerfile .
	@echo "Docker image built"

# Docker run - Agent
docker-run:
	@echo "Running agent in Docker..."
	@docker-compose up agent

# Docker clean
docker-clean:
	@echo "Cleaning Docker resources..."
	@docker-compose down -v
	@docker rmi thirsty-game-studio-agent:latest 2>/dev/null || true
	@docker rmi thirsty-game:latest 2>/dev/null || true
	@echo "Docker resources cleaned"

# Build game Docker image
game-build:
	@echo "Building game Docker image..."
	@docker build -t thirsty-game:latest -f Dockerfile.game .
	@echo "Game Docker image built"

# Run game in Docker (headless)
game-docker: game-build
	@echo "Running game in Docker (headless mode)..."
	@docker-compose --profile game up game-server

# Deploy complete stack (God-Tier Monolithic Deployment)
deploy-all:
	@echo "=========================================="
	@echo "  God-Tier Monolithic Deployment"
	@echo "  Thirsty's Game Studio Complete Stack"
	@echo "=========================================="
	@echo ""
	@echo "Building all images..."
	@docker build -t thirsty-game-studio-agent:latest -f Dockerfile .
	@docker build -t thirsty-game:latest -f Dockerfile.game .
	@echo ""
	@echo "Starting complete stack..."
	@docker-compose --profile game up -d agent game-server
	@echo ""
	@echo "=========================================="
	@echo "  Deployment Complete!"
	@echo "=========================================="
	@echo ""
	@echo "Services running:"
	@docker-compose ps
	@echo ""
	@echo "Logs: docker-compose logs -f"
	@echo "Stop: make deploy-stop"

# Deploy game only
deploy-game: game-build
	@echo "Deploying game service..."
	@docker-compose --profile game up -d game-server
	@echo "Game deployed! Check status with: make deploy-status"

# Stop all services
deploy-stop:
	@echo "Stopping all services..."
	@docker-compose --profile game down
	@echo "All services stopped"

# Check deployment status
deploy-status:
	@echo "Deployment Status:"
	@echo "=================="
	@docker-compose ps
	@echo ""
	@echo "Resource Usage:"
	@docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}" 2>/dev/null || echo "No containers running"

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
