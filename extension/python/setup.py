#!/usr/bin/env python3
"""
Setup script for ABAP Code Assistant Python backend
"""
import subprocess
import sys
import os
import platform
from pathlib import Path

def get_pip_command():
    """Get the appropriate pip command for the platform"""
    pip_commands = [
        f"{sys.executable} -m pip",
        "pip3",
        "pip",
        f"{sys.executable} -m pip3"
    ]
    
    for cmd in pip_commands:
        try:
            result = subprocess.run(cmd.split() + ["--version"], 
                                 capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                return cmd.split()
        except:
            continue
    
    return [sys.executable, "-m", "pip"]

def install_requirements():
    """Install required Python packages"""
    print(f"Python version: {sys.version}")
    print(f"Platform: {platform.platform()}")
    print(f"Python executable: {sys.executable}")
    
    pip_cmd = get_pip_command()
    print(f"Using pip command: {' '.join(pip_cmd)}")
    
    # Try to upgrade pip first
    try:
        subprocess.run(pip_cmd + ["install", "--upgrade", "pip"], 
                     capture_output=True, text=True, timeout=30)
    except:
        pass  # Ignore pip upgrade errors
    
    # Install dependencies directly
    dependencies = [
        "groq==0.30.0",
        "python-dotenv==1.0.0", 
        "pydantic==2.5.0",
        "rich==13.7.0"
    ]
    
    try:
        print("Installing Python dependencies...")
        result = subprocess.run(
            pip_cmd + ["install"] + dependencies,
            capture_output=True, text=True, timeout=120
        )
        
        if result.returncode == 0:
            print("✅ Python dependencies installed successfully!")
            return True
        else:
            print(f"❌ Failed to install dependencies:")
            print(f"Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Installation timed out")
        return False
    except Exception as e:
        print(f"❌ Installation failed: {e}")
        return False

if __name__ == "__main__":
    success = install_requirements()
    sys.exit(0 if success else 1) 