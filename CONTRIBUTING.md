# Contributing to Instagram Account Scraper

First off, thank you for considering contributing! 🎉

## Getting Started

1. Fork the repository on GitHub.
2. Clone your fork locally:
   ```bash
   git clone https://github.com/xiaozhucchongya-byte/instagram-account-scraper.git
   cd instagram-account-scraper
   ```
3. Install in development mode:
   ```bash
   pip install -e ".[dev]"
   ```
4. Create a branch for your feature:
   ```bash
   git checkout -b feature/my-new-feature
   ```

## Development Workflow

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=ig_scraper

# Run a specific test file
pytest tests/test_scraper.py -v
```

### Code Style

- Follow PEP 8 (use `flake8` or your editor's linter).
- Use type hints for all function signatures.
- Keep functions focused and well-documented.
- Add docstrings for all public functions and classes.

### Adding a New Feature

1. Write the code in `src/ig_scraper/`.
2. Add tests in `tests/`.
3. Update the README if the feature is user-facing.
4. Update the CHANGELOG.
5. Run tests: `pytest`
6. Commit with a clear message: `feat: add hashtag story scraping`

### Commit Message Convention

We use [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation only
- `refactor:` Code refactoring
- `test:` Test additions or changes
- `chore:` Build/tooling changes

### Pull Request Process

1. Ensure all tests pass: `pytest`
2. Update documentation if needed.
3. Add a changelog entry under `[Unreleased]` in `CHANGELOG.md`.
4. Open a pull request with a clear description of the changes.

## Reporting Bugs

Please use the [GitHub issue tracker](https://github.com/xiaozhucchongya-byte/instagram-account-scraper/issues) to report bugs.

Include:
- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages / tracebacks

## Feature Requests

We welcome feature requests! Please open an issue with:
- A clear description of the feature
- The use case it addresses
- Any alternatives you've considered

## Code of Conduct

Be respectful and constructive. We're all here to build something useful together.
