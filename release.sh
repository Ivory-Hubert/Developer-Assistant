#!/usr/bin/env bash
set -e

echo "Starting release process..."

if [[ -n $(git status --porcelain) ]]; then
    echo "❌ Working directory is not clean. Commit or stash changes first."
    git status --porcelain
    exit 1
fi

VERSION=$(grep -m 1 'version =' pyproject.toml | tr -d 'version =" ')
echo "Preparing release v$VERSION"

read -p "Publish version $VERSION? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Release aborted."
    exit 1
fi

echo "Pushing commits..."
git push

echo "Tagging version v$VERSION..."
git tag -a "v$VERSION" -m "Release version $VERSION"

git push origin "v$VERSION"

echo "✅ Tag pushed. Publishing initiated..."
