#!/usr/bin/env python3
"""
Dependency checker for ABAP Code Assistant
"""
import sys
import subprocess

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = ['groq', 'python-dotenv', 'pydantic', 'rich']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} is installed")
        except ImportError:
            print(f"❌ {package} is missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Installing missing packages...")
        
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", 
                "groq==0.30.0", "python-dotenv==1.0.0", 
                "pydantic==2.5.0", "rich==13.7.0"
            ])
            print("✅ All dependencies installed successfully!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            return False
    else:
        print("✅ All dependencies are already installed!")
        return True

if __name__ == "__main__":
    success = check_dependencies()
    sys.exit(0 if success else 1) 