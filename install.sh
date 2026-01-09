#!/bin/bash

# Fast PDF to Markdown Converter - Global Installer
# Author: pc-style

set -e

echo "Installing PDF2MD-CLI globally..."

# Check if bun is installed
if ! command -v bun &> /dev/null
then
    echo "Error: Bun is not installed. Please install it first from https://bun.sh"
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
bun install

# Build the binary
echo "Building the binary..."
bun run build

# Install globally
echo "Linking globally..."
bun install -g .

echo ""
echo "Success! You can now use 'pdf2md' command from anywhere."
echo "Run 'pdf2md --help' to get started."
