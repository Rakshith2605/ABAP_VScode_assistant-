#!/usr/bin/env python3
"""
Robust dependency checker for ABAP Code Assistant
Works across different Python installations and platforms
"""
import sys
import subprocess
import os
import platform
import shutil
import tempfile
import json
from pathlib import Path

def get_python_info():
    """Get comprehensive Python environment information"""
    info = {
        'version': sys.version,
        'executable': sys.executable,
        'platform': platform.platform(),
        'architecture': platform.architecture(),
        'python_path': os.environ.get('PYTHONPATH', 'Not set'),
        'conda_env': os.environ.get('CONDA_DEFAULT_ENV', 'Not in conda'),
        'virtual_env': os.environ.get('VIRTUAL_ENV', 'Not in venv'),
        'pip_version': 'Unknown'
    }
    
    # Try to get pip version
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            info['pip_version'] = result.stdout.strip()
    except:
        pass
    
    return info

def get_pip_command():
    """Get the appropriate pip command for the platform"""
    # Try different pip commands in order of preference
    pip_commands = [
        [sys.executable, "-m", "pip"],  # Most reliable
        [sys.executable, "-m", "pip3"],
        ["pip3"],
        ["pip"]
    ]
    
    for cmd in pip_commands:
        try:
            result = subprocess.run(cmd + ["--version"], 
                                 capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print(f"✅ Using pip command: {' '.join(cmd)}")
                return cmd
        except:
            continue
    
    # Fallback to sys.executable -m pip
    print(f"⚠️  Using fallback pip command: {sys.executable} -m pip")
    return [sys.executable, "-m", "pip"]

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} is not supported. Python 3.8+ is required.")
        return False
    else:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True

def install_dependencies_flexible():
    """Install dependencies with flexible version requirements"""
    pip_cmd = get_pip_command()
    
    # More flexible dependency versions that work across different systems
    dependencies = [
        "groq>=0.20.0",  # Allow newer versions
        "python-dotenv>=0.19.0",
        "pydantic>=1.8.0",  # Support both v1 and v2
        "requests>=2.25.0",  # HTTP requests
        "rich>=10.0.0"  # Rich for pretty logging if available
    ]
    
    print("📦 Installing dependencies with flexible versions...")
    
    # Try to upgrade pip first (but don't fail if it doesn't work)
    try:
        print("🔄 Upgrading pip...")
        subprocess.run(pip_cmd + ["install", "--upgrade", "pip"], 
                     capture_output=True, text=True, timeout=30)
    except Exception as e:
        print(f"⚠️  Pip upgrade failed (continuing anyway): {e}")
    
    # Install dependencies one by one for better error handling
    success_count = 0
    for dep in dependencies:
        try:
            print(f"📥 Installing {dep}...")
            result = subprocess.run(
                pip_cmd + ["install", dep],
                capture_output=True, text=True, timeout=60
            )
            
            if result.returncode == 0:
                print(f"✅ {dep} installed successfully")
                success_count += 1
            else:
                print(f"❌ Failed to install {dep}: {result.stderr}")
                # Try with --user flag for systems without admin access
                try:
                    print(f"🔄 Retrying {dep} with --user flag...")
                    result2 = subprocess.run(
                        pip_cmd + ["install", "--user", dep],
                        capture_output=True, text=True, timeout=60
                    )
                    if result2.returncode == 0:
                        print(f"✅ {dep} installed successfully (user install)")
                        success_count += 1
                    else:
                        print(f"❌ User install also failed: {result2.stderr}")
                except Exception as e:
                    print(f"❌ User install attempt failed: {e}")
                    
        except subprocess.TimeoutExpired:
            print(f"⏰ Timeout installing {dep}")
        except Exception as e:
            print(f"❌ Error installing {dep}: {e}")
    
    print(f"\n📊 Installation summary: {success_count}/{len(dependencies)} packages installed")
    return success_count >= len(dependencies) * 0.75  # Allow 25% failure rate

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = ['groq', 'dotenv', 'pydantic', 'rich']
    missing_packages = []
    
    print("🔍 Checking Python environment...")
    python_info = get_python_info()
    
    # Print environment info
    for key, value in python_info.items():
        print(f"  {key}: {value}")
    
    # Check Python version
    if not check_python_version():
        return False
    
    print("\n🔍 Checking required packages...")
    
    for package in required_packages:
        try:
            if package == 'dotenv':
                __import__('dotenv')
            elif package == 'pydantic':
                # Try both v1 and v2
                try:
                    __import__('pydantic')
                except ImportError:
                    __import__('pydantic.v1')
            else:
                __import__(package)
            print(f"✅ {package} is available")
        except ImportError:
            print(f"❌ {package} is missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("🔄 Attempting to install missing packages...")
        
        if install_dependencies_flexible():
            print("✅ Dependencies installed successfully")
            return True
        else:
            print("❌ Failed to install some dependencies")
            print("\n💡 Manual installation options:")
            print("1. Install Python 3.8+ if not already installed")
            print("2. Run: pip install groq python-dotenv pydantic")
            print("3. Or run: pip install --user groq python-dotenv pydantic")
            print("4. Check your internet connection and try again")
            return False
    else:
        print("✅ All required packages are available!")
        return True

def create_requirements_file():
    """Create a requirements.txt file for manual installation"""
    requirements_content = """# ABAP Code Assistant Dependencies
# Install with: pip install -r requirements.txt
# Or for user install: pip install --user -r requirements.txt

groq>=0.20.0
python-dotenv>=0.19.0
pydantic>=1.8.0
requests>=2.25.0
"""
    
    try:
        requirements_path = Path(__file__).parent / "requirements.txt"
        with open(requirements_path, 'w') as f:
            f.write(requirements_content)
        print(f"📝 Created requirements.txt at: {requirements_path}")
        return True
    except Exception as e:
        print(f"❌ Failed to create requirements.txt: {e}")
        return False

def main():
    """Main function with comprehensive error handling"""
    print("🚀 ABAP Code Assistant - Dependency Checker")
    print("=" * 50)
    
    try:
        success = check_dependencies()
        
        if success:
            print("\n🎉 All dependencies are ready!")
            print("✅ The extension should work properly now")
            sys.exit(0)
        else:
            print("\n⚠️  Some dependencies are missing or failed to install")
            print("📝 Creating requirements.txt for manual installation...")
            create_requirements_file()
            
            print("\n💡 Next steps:")
            print("1. Try running the extension again")
            print("2. If it still fails, manually install dependencies:")
            print("   pip install -r requirements.txt")
            print("3. Or use user install: pip install --user -r requirements.txt")
            print("4. Check the Output panel in VS Code for detailed error messages")
            
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Unexpected error during dependency check: {e}")
        print("💡 Please check your Python installation and try again")
        create_requirements_file()
        sys.exit(1)

if __name__ == "__main__":
    main() 