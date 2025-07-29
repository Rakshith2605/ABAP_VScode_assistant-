#!/usr/bin/env python3
"""
Dependency checker for ABAP Code Assistant
"""
import sys
import subprocess
import os
import platform

def get_pip_command():
    """Get the appropriate pip command for the platform"""
    # Try different pip commands
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
    
    # Fallback to sys.executable -m pip
    return [sys.executable, "-m", "pip"]

def install_dependencies():
    """Install required dependencies"""
    pip_cmd = get_pip_command()
    print(f"Using pip command: {' '.join(pip_cmd)}")
    
    # Try to upgrade pip first
    try:
        subprocess.run(pip_cmd + ["install", "--upgrade", "pip"], 
                     capture_output=True, text=True, timeout=30)
    except:
        pass  # Ignore pip upgrade errors
    
    # Install dependencies
    dependencies = [
        "groq==0.30.0",
        "python-dotenv==1.0.0", 
        "pydantic==2.5.0",
        "rich==13.7.0"
    ]
    
    try:
        print("Installing dependencies...")
        result = subprocess.run(
            pip_cmd + ["install"] + dependencies,
            capture_output=True, text=True, timeout=120
        )
        
        if result.returncode == 0:
            print("✅ All dependencies installed successfully!")
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

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = ['groq', 'python-dotenv', 'pydantic', 'rich']
    missing_packages = []
    
    print(f"Python version: {sys.version}")
    print(f"Platform: {platform.platform()}")
    print(f"Python executable: {sys.executable}")
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} is installed")
        except ImportError:
            print(f"❌ {package} is missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        return install_dependencies()
    else:
        print("✅ All dependencies are already installed!")
        return True

if __name__ == "__main__":
    success = check_dependencies()
    sys.exit(0 if success else 1) 