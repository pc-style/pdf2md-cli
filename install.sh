#!/bin/bash

# Fast PDF to Markdown Converter - Global Installer
# Author: pc-style

set -e

APP_NAME="pdf2md"
INSTALL_DIR="/usr/local/bin"
REPO_URL="https://github.com/pc-style/pdf2md-cli.git"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we are in the project directory
if [ ! -f "package.json" ]; then
    echo -e "${YELLOW}Project not found in current directory. Downloading source...${NC}"
    
    # Check for git
    if ! command -v git &> /dev/null; then
        echo -e "${RED}Error: Git is required for remote installation.${NC}"
        exit 1
    fi

    # Create temp directory
    TEMP_DIR=$(mktemp -d)
    
    # Setup cleanup trap
    cleanup() {
        echo -e "${YELLOW}Cleaning up temporary files...${NC}"
        rm -rf "$TEMP_DIR"
    }
    trap cleanup EXIT

    # Clone into temp
    git clone --depth 1 "$REPO_URL" "$TEMP_DIR"
    cd "$TEMP_DIR"
fi

echo -e "${GREEN}Installing ${APP_NAME} globally...${NC}"

# 1. Check if Bun is installed
if ! command -v bun &> /dev/null; then
    echo -e "${RED}Error: Bun is not installed.${NC}"
    echo -e "Please install Bun first: ${YELLOW}curl -fsSL https://bun.sh/install | bash${NC}"
    exit 1
fi

# 2. Install dependencies (needed for build)
echo -e "Installing dependencies..."
bun install

# 3. Build the binary
echo -e "Building binary..."
bun run build

# 4. Check if build was successful
if [ ! -f "bin/$APP_NAME" ]; then
    echo -e "${RED}Error: Build failed. Binary not found at bin/$APP_NAME${NC}"
    exit 1
fi

# 5. Install to /usr/local/bin
echo -e "Installing to $INSTALL_DIR..."

# Check if we have write permissions to the install directory
if [ -w "$INSTALL_DIR" ]; then
    cp "bin/$APP_NAME" "$INSTALL_DIR/"
else
    echo -e "${YELLOW}Administrator permissions required to write to $INSTALL_DIR${NC}"
    sudo cp "bin/$APP_NAME" "$INSTALL_DIR/"
fi

# 6. Verify installation
if command -v $APP_NAME &> /dev/null; then
    echo -e "${GREEN}Success! ${APP_NAME} is now installed.${NC}"
    echo -e "Run ${YELLOW}$APP_NAME --help${NC} to get started."
else
    echo -e "${RED}Warning: Installation completed, but '$APP_NAME' is not in your PATH.${NC}"
    echo "Please ensure $INSTALL_DIR is in your PATH."
fi