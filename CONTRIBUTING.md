# Contributing to QuantumScope

Thank you for your interest in contributing to QuantumScope! We welcome contributions from the community to help improve this project.

## How to Contribute

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
   ```bash
   git clone https://github.com/your-username/QuantumScope.git
   cd QuantumScope
   ```
3. **Create a new branch** for your feature or bugfix
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make your changes** and commit them with a clear message
   ```bash
   git commit -m "Add your commit message here"
   ```
5. **Push your changes** to your fork
   ```bash
   git push origin feature/your-feature-name
   ```
6. **Create a Pull Request** from your fork to the main repository

## Development Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

3. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code
- Use type hints for all function signatures
- Keep lines under 88 characters (Black's default)
- Document all public functions and classes with docstrings
- Write unit tests for new features

## Running Tests

```bash
pytest
```

## Reporting Issues

When reporting issues, please include:
- A clear description of the issue
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Any error messages
- Your Python version and operating system

## Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.
