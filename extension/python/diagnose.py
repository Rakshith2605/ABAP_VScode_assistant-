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
    
    dependencies = ['groq', 'dotenv', 'pydantic', 'rich']
    
    for dep in dependencies:
        try:
            __import__(dep)
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
    
    # Test config command
    try:
        result = subprocess.run([
            sys.executable, "main.py", "config"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print(f"  ✅ config command works")
        else:
            print(f"  ❌ config command failed: {result.stderr}")
    except Exception as e:
        print(f"  ❌ config command error: {e}")
    
    # Test setup command with dummy API key
    try:
        result = subprocess.run([
            sys.executable, "main.py", "setup"
        ], capture_output=True, text=True, timeout=30, env={
            **os.environ,
            "GROQ_API_KEY": "test_key_for_diagnostic"
        })
        
        if result.returncode == 0:
            print(f"  ✅ setup command works")
        else:
            # Check if it's just an API key validation error (expected)
            if "Invalid API Key" in result.stderr or "Setup failed" in result.stderr:
                print(f"  ✅ setup command works (API key validation as expected)")
            else:
                print(f"  ❌ setup command failed: {result.stderr}")
    except Exception as e:
        print(f"  ❌ setup command error: {e}")

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