.PHONY: clean install test lint lint-netgsm lint-tests lint-examples format format-netgsm format-tests format-examples build publish help

# Detect OS and set Python command
ifeq ($(OS),Windows_NT)
	PYTHON = py
else
	PYTHON = python3
endif

help:
	@echo "clean      - remove all build, test, coverage and Python artifacts"
	@echo "install    - install the package to the active Python's site-packages"
	@echo "test       - run tests with pytest"
	@echo "lint       - check style with flake8 and black (all)"
	@echo "format     - format code with black (all)"
	@echo "build      - package"
	@echo "publish    - package and upload a release"

clean:
	$(PYTHON) -c "import shutil; import glob; import os; [shutil.rmtree(p, ignore_errors=True) for p in ['build', 'dist', '*.egg-info', '.coverage', 'htmlcov', '.pytest_cache', '.tox'] + glob.glob('**/__pycache__', recursive=True)]"
	$(PYTHON) -c "import glob; import os; [os.remove(f) for f in glob.glob('**/*.py[cod]', recursive=True)]"

install:
	$(PYTHON) -m pip install -e ".[dev]"

test:
	$(PYTHON) -m pytest --verbose --color=yes

lint: lint-netgsm lint-tests lint-examples

lint-netgsm:
	$(PYTHON) scripts/lint.py netgsm

lint-tests:
	$(PYTHON) scripts/lint.py tests

lint-examples:
	$(PYTHON) scripts/lint.py examples

format: format-netgsm format-tests format-examples

format-netgsm:
	$(PYTHON) scripts/format.py netgsm

format-tests:
	$(PYTHON) scripts/format.py tests

format-examples:
	$(PYTHON) scripts/format.py examples

build: clean
	$(PYTHON) setup.py sdist bdist_wheel

publish: build
	$(PYTHON) -m twine check dist/*
	$(PYTHON) -m twine upload dist/* 