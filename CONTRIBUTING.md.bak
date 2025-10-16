# Contributing to Kai

Thank you for your interest in contributing to Kai! This document provides guidelines and instructions for contributing.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/kai.git`
3. Create a virtual environment: `python -m venv .venv`
4. Activate it: `source .venv/bin/activate` (Linux/Mac) or `.venv\Scripts\activate` (Windows)
5. Install dependencies: `pip install -r requirements.txt`
6. Install development dependencies: `pip install pytest black flake8 mypy`

## Development Workflow

1. Create a new branch: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Run tests: `python -m pytest tests/`
4. Format code: `black .`
5. Check linting: `flake8 .`
6. Commit your changes: `git commit -m "Description of changes"`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Create a Pull Request

## Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Write docstrings for all functions and classes
- Keep functions small and focused
- Use meaningful variable names

## Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Aim for high test coverage
- Test edge cases and error conditions

## Project Structure

```
kai/
├── ai/              # AI model and context management
├── core/            # Core functionality (executor, config, history)
├── utils/           # Utility modules (safety, UI)
├── tests/           # Test suite
└── main.py          # Entry point
```

## Adding New Features

When adding a new feature:

1. Discuss it in an issue first
2. Update documentation
3. Add tests
4. Update README if needed
5. Follow existing code patterns

## Safety Considerations

Kai executes shell commands, so safety is paramount:

- Always validate user input
- Check commands for dangerous patterns
- Require confirmation for risky operations
- Never auto-execute destructive commands
- Add new dangerous patterns to `utils/safety.py`

## Reporting Bugs

When reporting bugs, include:

- Operating system and version
- Python version
- Kai version
- Steps to reproduce
- Expected vs actual behavior
- Error messages and logs

## Feature Requests

For feature requests:

- Check if it already exists in issues
- Describe the use case
- Explain why it would be useful
- Suggest implementation if possible

## Questions?

Feel free to open an issue for questions or join our discussions.

Thank you for contributing to Kai! 🤖
