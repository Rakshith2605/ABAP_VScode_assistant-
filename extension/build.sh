#!/bin/bash

# Build script for Local AI Code Completion VS Code Extension

echo "🚀 Building ABAP Code Assistant VS Code Extension..."

# Ensure script runs from its directory (extension/)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR" || exit 1

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

# Check if vsce is installed
if ! command -v vsce &> /dev/null; then
    echo "📦 Installing vsce globally..."
    npm install -g vsce
fi

# Install dependencies
echo "📦 Installing dependencies in $PWD..."
if [ -f package.json ]; then
    npm install
else
    echo "⚠️ package.json not found in $PWD. Skipping npm install."
fi

# Package the extension
echo "📦 Packaging extension..."
vsce package

echo "✅ Extension packaged successfully!"
echo "📁 Look for the .vsix file in the current directory"
echo "🔧 To install in VS Code:"
echo "   1. Open VS Code"
echo "   2. Go to Extensions (Ctrl+Shift+X)"
echo "   3. Click '...' and select 'Install from VSIX...'"
echo "   4. Select the generated .vsix file" 