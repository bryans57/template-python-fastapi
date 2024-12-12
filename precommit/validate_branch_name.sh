#!/bin/bash

BRANCH_NAME=$(git rev-parse --abbrev-ref HEAD)

# Regex for allowed branch names (e.g., "feature/*")
if ! [[ $BRANCH_NAME =~ ^(feature|bugfix|release|hotfix)/.*$ ]]; then
    echo "Branch name '$BRANCH_NAME' is invalid. It must follow the pattern 'feature/*'."
    exit 1
fi
