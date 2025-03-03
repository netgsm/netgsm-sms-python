# Netgsm Python SDK Developer Guide

This guide explains the necessary steps for developing and testing the Netgsm Python SDK.

## Requirements

- Python 3.6 or higher
- pip (Python package manager)
- virtualenv or pipenv (optional, but recommended)

## Development Environment Setup

1. Clone the repository:

```bash
git clone https://github.com/netgsm/netgsm-sms-python.git
cd netgsm-sms-python
```

2. Create and activate a virtual environment:

```bash
# Using virtualenv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Or using pipenv
pipenv shell
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file:

```bash
cp .env.example .env
```

5. Edit the `.env` file to add your Netgsm credentials:

```
NETGSM_USERNAME=YOUR_USERNAME
NETGSM_PASSWORD=YOUR_PASSWORD
NETGSM_MSGHEADER=YOUR_SMS_HEADER
```

## Running Tests

To run tests for the SDK:

```bash
python -m unittest discover
```

To run a specific test file:

```bash
python -m unittest tests/test_sms_service.py
```

## Coding Standards

We follow Python's [PEP 8](https://www.python.org/dev/peps/pep-0008/) coding standards in this project.

To check your code:

```bash
flake8 netgsm
```

## Packaging and Distribution

To package the SDK:

```bash
python setup.py sdist bdist_wheel
```

To upload to PyPI (project managers only):

```bash
twine upload dist/*
```

## Version Management

Version numbers are determined according to [Semantic Versioning](https://semver.org/) standards:

- MAJOR version: Changes that break API compatibility
- MINOR version: Backward compatible feature additions
- PATCH version: Backward compatible bug fixes

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Help and Support

If you have questions or need help:

- Open a [GitHub Issue](https://github.com/netgsm/netgsm-sms-python/issues)
- Contact the Netgsm support team: teknikdestek@netgsm.com.tr 