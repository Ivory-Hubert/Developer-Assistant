#!/usr/bin/env bash

set -e

echo "Starting release process for Developer Assistant..."

if [[ -n $(git status --porcelain) ]]; then
    echo "❌ Working directory is not clean. Commit or stash changes first."
    git status --porcelain
    exit 1
fi

echo "Cleaning old build files..."
rm -rf dist/ *.egg-info

VERSION=$(grep -m 1 'version =' pyproject.toml | tr -d 'version =" ')
read -p "Publish version $VERSION to PyPI? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Release aborted."
    exit 1
fi

# echo "Running tests..."
# uv run pytest

echo "Building package..."
uv build

echo "Checking PyPI metadata rendering..."
uv run twine check dist/*

echo "Uploading to PyPI..."
uv publish

echo "Uploading to GitHub..."
git push

echo "Tagging version v$VERSION in Git..."
git tag -a "v$VERSION" -m "Release version $VERSION"
git push origin "v$VERSION"

echo "✅ Successfully released v$VERSION!"