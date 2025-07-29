#!/usr/bin/env python3
"""
Diagnostic script for ABAP Code Assistant
"""
import sys
import os
import subprocess
import platform

def check_python():
    """Check Python environment"""
    print("🐍 Python Environment:")
    print(f"  Python version: {sys.version}")
    print(f"  Python executable: {sys.executable}")
    print(f"  Platform: {platform.platform()}")
    print(f"  Current directory: {os.getcwd()}")

def check_dependencies():
    """Check if dependencies are installed"""
    print("\n📦 Dependencies:")
    
    dependencies = ['groq', 'python-dotenv', 'pydantic', 'rich']
    
    for dep in dependencies:
        try:
            __import__(dep.replace('-', '_'))
            print(f"  ✅ {dep}")
        except ImportError:
            print(f"  ❌ {dep}")

def check_pip():
    """Check pip availability"""
    print("\n📥 Pip:")
    
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
                print(f"  ✅ {cmd}")
                return cmd.split()
        except:
            print(f"  ❌ {cmd}")
    
    return None

def test_imports():
    """Test importing the main modules"""
    print("\n🔧 Module Imports:")
    
    # Add current directory to path
    sys.path.insert(0, os.path.dirname(__file__))
    
    try:
        import groq
        print("  ✅ groq imported successfully")
    except ImportError as e:
        print(f"  ❌ groq import failed: {e}")
    
    try:
        from local_ai_code_completion import config
        print("  ✅ config imported successfully")
    except ImportError as e:
        print(f"  ❌ config import failed: {e}")
    
    try:
        from local_ai_code_completion import setup
        print("  ✅ setup imported successfully")
    except ImportError as e:
        print(f"  ❌ setup import failed: {e}")
    
    try:
        from local_ai_code_completion import ai_completion
        print("  ✅ ai_completion imported successfully")
    except ImportError as e:
        print(f"  ❌ ai_completion import failed: {e}")

def test_commands():
    """Test main commands"""
    print("\n⚡ Command Tests:")
    
    commands = ['config', 'setup']
    
    for cmd in commands:
        try:
            result = subprocess.run([
                sys.executable, "main.py", cmd
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print(f"  ✅ {cmd} command works")
            else:
                print(f"  ❌ {cmd} command failed: {result.stderr}")
        except Exception as e:
            print(f"  ❌ {cmd} command error: {e}")

def main():
    """Run all diagnostics"""
    print("🔍 ABAP Code Assistant Diagnostics")
    print("=" * 50)
    
    check_python()
    check_dependencies()
    check_pip()
    test_imports()
    test_commands()
    
    print("\n" + "=" * 50)
    print("Diagnostics complete!")

if __name__ == "__main__":
    main() 