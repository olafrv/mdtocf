#!/bin/bash

# Python Package Build and Release
# https://pypi.org/project/mdtocf/

set -e

if [ -f .env ]; then
    set -a && source .env && set +a
fi

if [ -z "$1" ]; then
	echo "Usage: $0 <live|test>"
	echo "  live: Publish to PyPI"
	echo "  test: Publish to Test PyPI"
	exit 1
fi

if [ "$1" == "live" ] && [ -z "$PYPI_LIVE_TOKEN" ]; then
	echo "Error: PYPI_LIVE_TOKEN is not set."
	exit 1
elif [ "$1" == "test" ] && [ -z "$PYPI_TEST_TOKEN" ]; then
	echo "Error: PYPI_TEST_TOKEN is not set."
	exit 1
fi

echo "Setting up virtual environment..."
if [ ! -f .venv/bin/uv ]; then
    python3 -m venv .venv && .venv/bin/pip install uv --quiet
fi
.venv/bin/uv sync --group dev

echo "Running tests..."
.venv/bin/uv run pytest tests

echo "Running code formatting checks..."
.venv/bin/uv run ruff format --check . || {
	echo "Fix code formatting issues before releasing."
	exit 1
}

echo "Checking for uncommitted changes..."
git diff --exit-code
git diff --cached --exit-code

echo "Checking if git tag matches pyproject.toml version..."
PROJECT_VERSION=$(.venv/bin/uv run python -c "import tomllib; f=open('pyproject.toml','rb'); data=tomllib.load(f); f.close(); print(data['project']['version'])")
TAG_NAME="${PROJECT_VERSION}"

if git rev-parse "$TAG_NAME" >/dev/null 2>&1; then
    echo "Git tag '$TAG_NAME' already exists."
else
    echo "Creating git tag '$TAG_NAME'..."
    git tag "$TAG_NAME"
fi

echo "Cleaning up previous builds..."
rm -rf ./dist ./build *.egg-info

echo "Building the package..."
.venv/bin/uv build

echo "Pushing changes remote repository..."
git push
git push --tags

if [ "$1" == "live" ]; then
	echo "Publishing to PyPI..."
	.venv/bin/uvx twine upload --username __token__ --password "${PYPI_LIVE_TOKEN}" dist/*
elif [ "$1" == "test" ]; then
	echo "Publishing to (Test) PyPI..."
	.venv/bin/uvx twine upload --username __token__ --password "${PYPI_TEST_TOKEN}" --repository testpypi dist/*
fi
