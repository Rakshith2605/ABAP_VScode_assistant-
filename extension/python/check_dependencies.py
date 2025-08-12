#!/usr/bin/env python3
"""
Dependency checker for ABAP Code Assistant
"""
import sys
import subprocess
import os
import platform
import shutil

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

def check_conda_environment():
    """Check if we're in a conda environment and if it has the right packages"""
    conda_env = os.environ.get('CONDA_DEFAULT_ENV')
    if conda_env:
        print(f"✅ Running in conda environment: {conda_env}")
        
        # Check if this is our abap-assistant environment
        if conda_env == 'abap-assistant':
            print("✅ Using dedicated abap-assistant conda environment")
            return True
        else:
            print(f"⚠️  Using conda environment '{conda_env}', but 'abap-assistant' is recommended")
            return False
    else:
        print("ℹ️  Not running in conda environment")
        return False

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
    
    # Check conda environment
    in_conda = check_conda_environment()
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} is installed")
        except ImportError:
            print(f"❌ {package} is missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        
        if in_conda:
            print("ℹ️  You're in a conda environment. Consider activating 'abap-assistant':")
            print("   conda activate abap-assistant")
            print("   pip install -r requirements.txt")
        
        print("Attempting to install missing packages...")
        if install_dependencies():
            print("✅ Dependencies installed successfully")
            return True
        else:
            print("❌ Failed to install dependencies")
            print("\n💡 Manual installation options:")
            print("1. Activate conda environment: conda activate abap-assistant")
            print("2. Install from requirements: pip install -r requirements.txt")
            print("3. Run setup script: python setup.py")
            return False
    else:
        print("✅ All dependencies are already installed!")
        return True

def main():
    """Main function with better error handling"""
    try:
        success = check_dependencies()
        if success:
            print("\n🎉 All dependencies are ready!")
            sys.exit(0)
        else:
            print("\n⚠️  Some dependencies are missing or failed to install")
            print("The extension will still work but with limited functionality")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error during dependency check: {e}")
        print("The extension will continue with limited functionality")
        sys.exit(1)

if __name__ == "__main__":
    main() 