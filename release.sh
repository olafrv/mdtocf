#!/bin/bash

# Python Package Build and Release 
# https://pypi.org/project/mdtocf/

set -e

echo "Activating virtual environment..."
source venv/bin/activate 2>/dev/null || { 
	./install.sh && source venv/bin/activate; 
}

echo "Installing required dev packages..."
pip install -e .[dev]  # pyproject.toml => project.optional-dependencies

echo "Running tests..."
pytest tests

echo "Running code formatting checks..."
black --check . || {
	echo "Fix code formatting issues before releasing."
	exit 1
}

echo "Checking for uncommitted changes..."
git diff --exit-code
git diff --cached --exit-code

echo "Cleaning up previous builds..."
rm -rf ./dist ./build *.egg-info

echo "Building the package..."
python -m build

if [ "$1" == "live" ]; then
	echo "Publishing to PyPI..."
	python -m twine upload --skip-existing --username __token__ --password "${PYPI_LIVE_TOKEN}" dist/*
elif [ "$1" == "test" ]; then
	echo "Publishing to (Test) PyPI..."
	python -m twine upload --skip-existing --username __token__ --password "${PYPI_TEST_TOKEN}" --repository testpypi dist/*
fi