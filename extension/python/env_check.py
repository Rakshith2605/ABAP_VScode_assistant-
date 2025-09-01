#!/usr/bin/env python3
"""
Simple environment checker for ABAP Code Assistant
Runs without external dependencies to diagnose basic issues
"""
import sys
import os
import platform
import subprocess
from pathlib import Path

def check_basic_python():
    """Check basic Python installation"""
    print("🐍 Python Environment Check")
    print("=" * 40)
    
    # Python version
    version = sys.version_info
    print(f"Python Version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required")
        return False
    else:
        print("✅ Python version is compatible")
    
    # Python executable
    print(f"Python Executable: {sys.executable}")
    
    # Platform info
    print(f"Platform: {platform.platform()}")
    print(f"Architecture: {platform.architecture()}")
    
    return True

def check_pip():
    """Check pip availability"""
    print("\n📦 Pip Check")
    print("-" * 20)
    
    pip_commands = [
        [sys.executable, "-m", "pip"],
        [sys.executable, "-m", "pip3"],
        ["pip3"],
        ["pip"]
    ]
    
    pip_found = False
    for cmd in pip_commands:
        try:
            result = subprocess.run(cmd + ["--version"], 
                                 capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print(f"✅ Pip found: {' '.join(cmd)}")
                print(f"  Version: {result.stdout.strip()}")
                pip_found = True
                break
        except:
            continue
    
    if not pip_found:
        print("❌ Pip not found")
        print("💡 Install pip: python -m ensurepip --upgrade")
        return False
    
    return True

def check_environment_vars():
    """Check relevant environment variables"""
    print("\n🔧 Environment Variables")
    print("-" * 30)
    
    env_vars = {
        'PYTHONPATH': 'Python module search path',
        'CONDA_DEFAULT_ENV': 'Conda environment',
        'VIRTUAL_ENV': 'Virtual environment',
        'PATH': 'System PATH'
    }
    
    for var, desc in env_vars.items():
        value = os.environ.get(var, 'Not set')
        if value != 'Not set':
            print(f"✅ {var}: {value}")
        else:
            print(f"ℹ️  {var}: {value}")
    
    return True

def check_write_permissions():
    """Check if we can write to the current directory"""
    print("\n📝 Write Permissions")
    print("-" * 25)
    
    try:
        test_file = Path(__file__).parent / "test_write.tmp"
        with open(test_file, 'w') as f:
            f.write("test")
        test_file.unlink()  # Clean up
        print("✅ Can write to extension directory")
        return True
    except Exception as e:
        print(f"❌ Cannot write to extension directory: {e}")
        print("💡 Try running VS Code as administrator or check permissions")
        return False

def check_network():
    """Check basic network connectivity"""
    print("\n🌐 Network Connectivity")
    print("-" * 25)
    
    try:
        import urllib.request
        urllib.request.urlopen('https://api.groq.com', timeout=5)
        print("✅ Can reach Groq API")
        return True
    except Exception as e:
        print(f"❌ Cannot reach Groq API: {e}")
        print("💡 Check your internet connection and firewall settings")
        return False

def create_install_script():
    """Create a simple installation script"""
    print("\n📝 Creating Installation Script")
    print("-" * 35)
    
    script_content = f"""#!/bin/bash
# ABAP Code Assistant - Dependency Installer
# Run this script to install dependencies

echo "Installing ABAP Code Assistant dependencies..."

# Check Python
python3 --version || python --version || echo "Python not found"

# Install dependencies
echo "Installing dependencies..."
python3 -m pip install --user groq python-dotenv pydantic requests || \\
python -m pip install --user groq python-dotenv pydantic requests || \\
echo "Installation failed"

echo "Done!"
"""
    
    try:
        script_path = Path(__file__).parent / "install_deps.sh"
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        # Make executable on Unix systems
        if platform.system() != "Windows":
            os.chmod(script_path, 0o755)
        
        print(f"✅ Created install script: {script_path}")
        return True
    except Exception as e:
        print(f"❌ Failed to create install script: {e}")
        return False

def main():
    """Main function"""
    checks = [
        check_basic_python,
        check_pip,
        check_environment_vars,
        check_write_permissions,
        check_network
    ]
    
    results = []
    for check in checks:
        try:
            result = check()
            results.append(result)
        except Exception as e:
            print(f"❌ Check failed with error: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 CHECK SUMMARY")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All checks passed! Your environment looks good.")
        print("💡 Try running the extension now.")
    else:
        print("⚠️  Some checks failed. Here are the next steps:")
        print("\n1. Fix the issues above")
        print("2. Run: python env_check.py")
        print("3. If Python/pip issues: Install Python 3.8+ and pip")
        print("4. If permission issues: Run VS Code as administrator")
        print("5. If network issues: Check firewall and internet connection")
        
        # Create helpful files
        create_install_script()
    
    print("\n💡 For more help, run: python check_dependencies.py")

if __name__ == "__main__":
    main()
