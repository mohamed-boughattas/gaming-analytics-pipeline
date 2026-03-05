# Contributing to Gaming Analytics Pipeline

Thank you for your interest in contributing to the Gaming Analytics Pipeline! This document provides guidelines and instructions for contributing.

## Code of Conduct

Be respectful, inclusive, and collaborative. Treat others as you would like to be treated.

## Getting Started

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager
- Git
- Docker (optional)

### Development Setup

1. **Fork and clone the repository**:

   ```bash
   git clone https://github.com/your-username/gaming-analytics-pipeline.git
   cd gaming-analytics-pipeline
   ```

2. **Create a virtual environment and install dependencies**:

   ```bash
   uv sync
   ```

3. **Set up pre-commit hooks**:

   ```bash
   make pre-commit-install
   ```

4. **Configure environment variables**:

   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

5. **Run tests to verify setup**:

   ```bash
   make test
   ```

## Development Workflow

### 1. Create a Branch

Create a descriptive branch for your work:

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Make Changes

- Write code following project conventions
- Add or update tests
- Update documentation as needed

### 3. Run Checks

Before committing, run the following:

```bash
# Format code
make format

# Run linters
make lint

# Run type checking
make typecheck

# Run security checks
make security

# Run tests
make test
```

### 4. Commit Changes

Write clear, descriptive commit messages:

```bash
git add .
git commit -m "feat: add support for new API endpoint"
# or
git commit -m "fix: resolve data type mismatch in games table"
```

Follow [Conventional Commits](https://www.conventionalcommits.org/) format:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code refactoring
- `test:` Test additions or changes
- `chore:` Maintenance tasks

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub with:

- Clear title and description
- Reference any related issues
- Screenshots for UI changes
- Testing instructions if applicable

## Coding Standards

### Code Style

We use [Ruff](https://github.com/astral-sh/ruff) for linting and formatting:

```bash
# Check code
ruff check src/ tests/

# Format code
ruff format src/ tests/
```

### Type Hints

All code should include type hints. We use [ty](https://github.com/astral-sh/ty) for type checking:

```python
from typing import Any

def process_games(games: list[dict[str, Any]]) -> dict[str, int]:
    """Process game data and return summary."""
    return {"count": len(games)}
```

### Documentation

- All functions and classes should have docstrings
- Use Google-style docstrings
- Include parameter and return type descriptions

```python
def extract_games(page_size: int = 20, max_pages: int | None = None) -> list[Game]:
    """Extract games from RAWG API.
    
    Args:
        page_size: Number of games per page
        max_pages: Maximum number of pages to fetch
    
    Returns:
        List of Game objects
    """
    # Implementation
```

### Testing

- Write tests for all new functionality
- Aim for high test coverage (>80%)
- Use pytest and pytest-asyncio
- Mock external dependencies (API calls, database)

```python
import pytest
from gaming_pipeline.extract import extract_games

@pytest.mark.asyncio
async def test_extract_games_with_defaults():
    """Test extracting games with default parameters."""
    games = await extract_games()
    assert len(games) > 0
    assert all(isinstance(game, Game) for game in games)
```

## Project Structure

```text
gaming-analytics-pipeline/
├── src/gaming_pipeline/
│   ├── config/           # Configuration management
│   ├── extract/          # Data extraction
│   ├── load/            # Data loading
│   ├── orchestrate/      # Prefect workflows
│   ├── quality/          # Data quality checks
│   └── transform/       # SQLMesh transformations
├── tests/               # Test files
├── docs/                # Documentation
├── dashboard/           # Marimo dashboard
└── plans/               # Architecture and implementation plans
```

## Types of Contributions

### Bug Fixes

- Describe the bug clearly
- Include steps to reproduce
- Provide test case that fails before fix
- Ensure all tests pass after fix

### New Features

- Discuss in an issue first
- Consider impact on existing functionality
- Include tests for new feature
- Update documentation

### Documentation

- Fix typos or unclear wording
- Add examples
- Improve existing documentation
- Keep it concise and clear

### Performance Improvements

- Benchmark before and after
- Ensure readability isn't compromised
- Document trade-offs

## Pull Request Review Process

1. **Automated Checks**
   - All tests must pass
   - Code must be formatted
   - Linting must pass
   - Type checking must pass
   - Security checks must pass

2. **Manual Review**
   - At least one maintainer approval
   - Address all review comments
   - Update PR description if needed

3. **Merge**
   - Squash and merge to main branch
   - Delete feature branch after merge
   - Update CHANGELOG if needed

## Questions?

- Open an issue for bugs or feature requests
- Start a discussion for questions
- Check existing issues first

## Resources

- [Documentation](README.md)
- [Architecture Decisions](docs/adr/)
- [Data Lineage](docs/data-lineage.md)
- [Prefect Documentation](https://docs.prefect.io/)
- [dlt Documentation](https://docs.dlthub.com/)

Thank you for contributing! 🎮
