# Tests

This directory contains tests for the Thirsty's Game Studio Agent System.

## Running Tests

### Using Make

```bash
make test
```

### Using pytest directly

```bash
# Activate virtual environment first
source .venv/bin/activate

# Run all tests
pytest

# Run with coverage
pytest --cov=agent --cov-report=html

# Run specific test file
pytest tests/test_runner.py

# Run with verbose output
pytest -v
```

## Test Structure

- `conftest.py` - Pytest configuration and fixtures
- `test_runner.py` - Tests for the main agent runner
- (More test files to be added as features are developed)

## Writing Tests

Follow these guidelines when writing tests:

1. Use descriptive test names that explain what is being tested
2. Keep tests focused and test one thing at a time
3. Use pytest fixtures for common setup
4. Add docstrings to explain complex test scenarios
5. Mock external dependencies (API calls, file I/O, etc.)

## Dependencies

Test dependencies are listed in `requirements-dev.txt` and include:

- pytest - Testing framework
- pytest-cov - Coverage plugin
- pytest-asyncio - Async test support
- pytest-mock - Mocking utilities
