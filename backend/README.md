# Game of Life Backend

This is the backend server for Conway's Game of Life, built with FastAPI and Python.

## Development Setup

1. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start the development server:

```bash
uvicorn src.main:app --reload
```

## Code Quality Tools

We use several tools to maintain code quality:

### Automatic Code Formatting and Linting

Python code is automatically formatted and linted on commit using husky and lint-staged. The following tools are run:

- **black**: Code formatting
- **flake8**: Style guide enforcement
  - flake8-docstrings: Docstring style checking
  - flake8-quotes: Quote style checking
  - flake8-bugbear: Bug finding
- **isort**: Import sorting

To manually run the formatters:

```bash
# Format with black
black .

# Sort imports
isort .

# Run flake8
flake8 .
```

### Configuration Files

- `setup.cfg`: Configuration for flake8 and isort

The linting script is located in `/scripts/lint-python.sh` and is automatically run by husky pre-commit hooks.

## Testing

Run tests with:
```bash
pytest
```

For coverage report:
```bash
pytest --cov=src
```

## Project Structure

```
backend/
├── src/           # Source code
├── tests/         # Test files
├── requirements.txt   # Project dependencies
└── setup.cfg      # Tool configurations
```

## Contributing

1. Ensure you have Python 3.8+ and pip installed
2. Create and activate a virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Make your changes
5. Run tests and ensure all checks pass
6. Commit your changes (this will trigger automatic formatting and linting)
7. Push to your fork and submit a pull request
