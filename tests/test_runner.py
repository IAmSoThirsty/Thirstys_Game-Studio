"""Basic tests for the agent runner."""

import pytest
from agent.runner import main


def test_runner_imports():
    """Test that the runner module can be imported."""
    assert main is not None


def test_runner_help(capsys):
    """Test that the runner shows help message."""
    import sys
    from agent.runner import main
    
    # Mock sys.argv to test help
    original_argv = sys.argv
    try:
        sys.argv = ["runner.py", "--help"]
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0
    finally:
        sys.argv = original_argv
