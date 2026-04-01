#!/usr/bin/env bash

set -e

echo "Building da-ui..."

if [[ -n $(git status --porcelain) ]]; then
    echo "❌ Working directory is not clean. Commit or stash changes first."
    git status --porcelain
    exit 1
fi

rm -rf dist *.egg-info

uv build

echo "Success..."