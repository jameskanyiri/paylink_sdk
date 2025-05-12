#!/bin/bash

set -e

VERSION_TYPE=$1  # patch, minor, or major

if [ -z "$VERSION_TYPE" ]; then
  echo "Usage: ./build.sh [patch|minor|major]"
  exit 1
fi

# Step 1: Update server_url in PayLinkClient
CLIENT_FILE="src/paylink_sdk/client.py"
NEW_URL="http://paylink-app.eastus.azurecontainer.io:8050/sse"
sed -i '' "s|http://0.0.0.0:8050/sse|$NEW_URL|g" "$CLIENT_FILE"

# Step 2: Bump version using Hatch
hatch version "$VERSION_TYPE"

# Step 3: Clean old dist
rm -rf dist/

# Step 4: Build
hatch build

# Step 5: Upload to PyPI
twine upload dist/*
