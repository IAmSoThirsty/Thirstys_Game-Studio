"""Test configuration for pytest."""

import sys
from pathlib import Path

# Add agent directory to path
agent_dir = Path(__file__).parent.parent / "agent"
sys.path.insert(0, str(agent_dir))
