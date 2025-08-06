#!/bin/bash

# Python Package Build and Release 
# https://pypi.org/project/mdtocf/

set -e

if [ -z "$1" ]; then
	echo "Usage: $0 <live|test>"
	echo "  live: Publish to PyPI"
	echo "  test: Publish to Test PyPI"
	sleep 1
fi

echo "Checking virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing required packages..."
pip install -e .  # pyproject.toml => project.dependencies
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

echo "Checking if git tag matches pyproject.toml version..."
# Extract version from pyproject.toml using Python
PROJECT_VERSION=$(python -c "import tomllib; f=open('pyproject.toml','rb'); data=tomllib.load(f); f.close(); print(data['project']['version'])")
TAG_NAME="${PROJECT_VERSION}"

# Check if the tag exists
if ! git rev-parse "$TAG_NAME" >/dev/null 2>&1; then
    echo "Error: Git tag '$TAG_NAME' does not exist for version $PROJECT_VERSION"
    echo "Please create the tag first: git tag $TAG_NAME"
    exit 1
fi

echo "Git tag '$TAG_NAME' found for version $PROJECT_VERSION"

echo "Cleaning up previous builds..."
rm -rf ./dist ./build *.egg-info

echo "Building the package..."
python -m build

if [ "$1" == "live" ]; then
	echo "Publishing to PyPI..."
	python -m twine upload --username __token__ --password "${PYPI_LIVE_TOKEN}" dist/*
elif [ "$1" == "test" ]; then
	echo "Publishing to (Test) PyPI..."
	python -m twine upload --username __token__ --password "${PYPI_TEST_TOKEN}" --repository testpypi dist/*
fi