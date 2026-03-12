#!/usr/bin/env bash

set -e

echo "Starting release process for Developer Assistant..."

echo "Cleaning old build files..."
rm -rf dist/ *.egg-info

echo "Running tests..."
# uv run pytest

echo "Building package..."
uv build

echo "Checking PyPI metadata rendering..."
uv run twine check dist/*

VERSION=$(grep -m 1 'version =' pyproject.toml | tr -d 'version =" ')
read -p "Publish version $VERSION to PyPI? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Release aborted."
    exit 1
fi

echo "Uploading to PyPI..."
uv publish

echo "Tagging version v$VERSION in Git..."
git tag -a "v$VERSION" -m "Release version $VERSION"
git push origin "v$VERSION"

echo "✅ Successfully released $VERSION!"