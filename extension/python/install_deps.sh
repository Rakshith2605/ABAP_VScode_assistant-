#!/bin/bash
# ABAP Code Assistant - Dependency Installer
# Run this script to install dependencies

echo "Installing ABAP Code Assistant dependencies..."

# Check Python
python3 --version || python --version || echo "Python not found"

# Install dependencies
echo "Installing dependencies..."
python3 -m pip install --user groq python-dotenv pydantic requests || \
python -m pip install --user groq python-dotenv pydantic requests || \
echo "Installation failed"

echo "Done!"
