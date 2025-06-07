.PHONY: test lint format clean install dev docs

# Variables
PYTHON = python3
PIP = pip3

# Install package in development mode
install:
	$(PIP) install -e .

# Install development dependencies
dev:
	$(PIP) install -e ".[dev]"
	pre-commit install

# Run tests
test:
	pytest -v --cov=QuantumScope --cov-report=term-missing

# Run linters
lint:
	black --check .
	isort --check-only .
	flake8 QuantumScope tests
	mypy QuantumScope

# Format code
format:
	black .
	isort .

# Build documentation
docs:
	cd docs && make html

# Clean build artifacts
clean:
	rm -rf build/ dist/ *.egg-info/ .pytest_cache/ .coverage htmlcov/
	find . -type d -name '__pycache__' -exec rm -rf {} +
	find . -type f -name '*.py[co]' -delete

# Build package
build:
	$(PYTHON) -m build

# Upload to PyPI (requires twine and PyPI credentials)
publish: clean build
	twine upload dist/*

# Run all checks (test, lint, format)
check: lint test
