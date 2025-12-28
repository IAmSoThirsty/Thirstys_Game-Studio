#!/bin/bash
# Setup script for Thirsty's Game Studio Agent System (Unix/Linux/macOS)

set -e  # Exit on error

echo "=================================="
echo "Thirsty's Game Studio Setup"
echo "=================================="
echo ""

# Check Python version
echo "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "Found Python $PYTHON_VERSION"

# Check if version is 3.8 or higher
if ! python3 -c 'import sys; exit(0 if sys.version_info >= (3, 8) else 1)'; then
    echo "ERROR: Python 3.8 or higher is required. Found: $PYTHON_VERSION"
    exit 1
fi

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ -d ".venv" ]; then
    echo "Virtual environment already exists. Skipping creation."
else
    python3 -m venv .venv
    echo "Virtual environment created at ./.venv"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install dependencies
echo ""
echo "Installing dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "Base requirements installed."
fi

# Install development dependencies (optional)
read -p "Install development dependencies? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if [ -f "requirements-dev.txt" ]; then
        pip install -r requirements-dev.txt
        echo "Development requirements installed."
    fi
fi

# Install package in editable mode
echo ""
echo "Installing package in editable mode..."
pip install -e .

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo ""
    echo "Creating .env file from template..."
    cp .env.example .env
    echo ".env file created. Please edit it with your API keys."
fi

# Create output directory
mkdir -p output

echo ""
echo "=================================="
echo "Setup Complete!"
echo "=================================="
echo ""
echo "To activate the virtual environment, run:"
echo "    source .venv/bin/activate"
echo ""
echo "To run the agent:"
echo "    python -m agent.runner --output-dir output"
echo ""
echo "Or use the installed command:"
echo "    thirsty-agent --output-dir output"
echo ""
echo "To deactivate the virtual environment:"
echo "    deactivate"
echo ""
echo "Don't forget to configure your API keys in .env file!"
echo "=================================="
