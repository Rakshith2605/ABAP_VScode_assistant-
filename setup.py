#!/usr/bin/env python3
"""
Setup script for ABAP VSCode Assistant
Installs dependencies and sets up the environment
"""
import subprocess
import sys
import os
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
    print("🔧 Setting up ABAP VSCode Assistant...")
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    
    pip_cmd = get_pip_command()
    print(f"Using pip command: {' '.join(pip_cmd)}")
    
    # Try to upgrade pip first
    try:
        print("📦 Upgrading pip...")
        subprocess.run(pip_cmd + ["install", "--upgrade", "pip"], 
                     capture_output=True, text=True, timeout=30)
    except:
        pass  # Ignore pip upgrade errors
    
    # Install dependencies from requirements.txt
    requirements_file = Path(__file__).parent / "requirements.txt"
    
    if requirements_file.exists():
        print("📋 Installing dependencies from requirements.txt...")
        try:
            result = subprocess.run(
                pip_cmd + ["install", "-r", str(requirements_file)],
                capture_output=True, text=True, timeout=300
            )
            
            if result.returncode == 0:
                print("✅ Dependencies installed successfully!")
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
    else:
        print("❌ requirements.txt not found")
        return False

def create_env_example():
    """Create a .env.example file"""
    env_example = Path(__file__).parent / ".env.example"
    
    if not env_example.exists():
        print("📝 Creating .env.example file...")
        env_content = """# ABAP VSCode Assistant Environment Variables
# Copy this file to .env and fill in your values

# Groq API Configuration
GROQ_API_KEY=your_groq_api_key_here
GROQ_BASE_URL=https://api.groq.com

# Model Configuration
LACC_MODEL_NAME=llama-3.3-70b-versatile
LACC_TEMPERATURE=0.3
LACC_TOP_P=0.3
LACC_TIMEOUT=15000

# VS Code Extension Context
LACC_PREFIX=
LACC_SUFFIX=
LACC_COMMENT=
LACC_FILE=
LACC_LANGUAGE=abap
LACC_MODE=code
"""
        
        try:
            with open(env_example, 'w') as f:
                f.write(env_content)
            print("✅ .env.example created successfully!")
        except Exception as e:
            print(f"❌ Failed to create .env.example: {e}")
    else:
        print("ℹ️  .env.example already exists")

def main():
    """Main setup function"""
    print("🚀 ABAP VSCode Assistant Setup")
    print("=" * 40)
    
    # Install dependencies
    if not install_requirements():
        print("\n❌ Setup failed. Please check the errors above.")
        sys.exit(1)
    
    # Create environment example file
    create_env_example()
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Copy .env.example to .env and add your Groq API key")
    print("2. Test the installation: python extension/python/test_backend.py")
    print("3. Run the main application: python extension/python/main.py config")
    print("\n🔗 For more information, see the README.md file")

if __name__ == "__main__":
    main()
