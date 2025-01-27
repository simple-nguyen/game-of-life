#!/bin/bash

# Exit on error
set -e

# Check if we have any Python files staged
python_files=$(git diff --cached --name-only --diff-filter=ACM | grep '\.py$' || true)

if [ -n "$python_files" ]; then
    echo "Running Python linters..."
    cd backend
    
    # Activate virtual environment if it exists
    if [ -d "venv" ]; then
        source venv/bin/activate
    elif [ -d ".venv" ]; then
        source .venv/bin/activate
    fi

    # Run formatters and linters
    black $python_files
    isort $python_files
    flake8 $python_files

    # Add back the formatted files
    git add $python_files
fi
