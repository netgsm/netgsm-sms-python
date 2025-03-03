# Contributing to Netgsm Python SDK

Thank you for your interest in contributing to the Netgsm Python SDK! This document provides guidelines and steps for contributing.

## Development Environment Setup

1. Fork the repository and clone it to your local machine:
   ```
   git clone https://github.com/netgsm/netgsm-sms-python.git
   cd netgsm-python
   ```

2. Create a virtual environment and install development dependencies:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e ".[dev]"
   ```

3. Create a `.env` file by copying `.env.example` and update it with your credentials:
   ```
   cp .env.example .env
   ```

## Code Standards

We follow these standards for code quality:

- [PEP 8](https://www.python.org/dev/peps/pep-0008/) for code style
- [PEP 257](https://www.python.org/dev/peps/pep-0257/) for docstrings
- Comprehensive unit tests for all features

To check code quality:
```
flake8 netgsm
black --check netgsm
```

To auto-format your code:
```
black netgsm
```

## Testing

Run tests with pytest:
```
pytest
```

For code coverage:
```
pytest --cov=netgsm tests/
```

## Pull Request Process

1. Ensure your code follows our standards and passes all tests
2. Update documentation as needed
3. Add your changes to the CHANGES.md file
4. Create a pull request with a clear description of the changes and any relevant issue numbers

## Commit Messages

Please use clear and descriptive commit messages with the following format:
```
feat: add new feature X
fix: resolve issue with Y
docs: update documentation for Z
test: add tests for feature W
refactor: improve implementation of V
```

## Reporting Issues

When reporting issues, please include:

- A clear, descriptive title
- A detailed description of the issue
- Steps to reproduce the problem
- Expected behavior
- Actual behavior
- Your environment (Python version, OS, etc.)

## License

By contributing to this project, you agree that your contributions will be licensed under the project's [MIT License](LICENSE). 