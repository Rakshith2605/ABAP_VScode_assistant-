#!/usr/bin/env python3
"""
Test script for ABAP Code Assistant Python backend
"""
import sys
import os
import subprocess
from pathlib import Path

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import groq
        print("✅ groq imported successfully")
    except ImportError as e:
        print(f"❌ groq import failed: {e}")
        return False
    
    try:
        import dotenv
        print("✅ python-dotenv imported successfully")
    except ImportError as e:
        print(f"❌ python-dotenv import failed: {e}")
        return False
    
    try:
        import pydantic
        print("✅ pydantic imported successfully")
    except ImportError as e:
        print(f"❌ pydantic import failed: {e}")
        return False
    
    try:
        import rich
        print("✅ rich imported successfully")
    except ImportError as e:
        print(f"❌ rich import failed: {e}")
        return False
    
    return True

def test_main_module():
    """Test if the main module can be imported"""
    print("\nTesting main module...")
    
    try:
        # Add the current directory to Python path
        sys.path.insert(0, os.path.dirname(__file__))
        
        from main import main
        print("✅ main module imported successfully")
        return True
    except ImportError as e:
        print(f"❌ main module import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ main module error: {e}")
        return False

def test_config_command():
    """Test the config command"""
    print("\nTesting config command...")
    
    try:
        result = subprocess.run([
            sys.executable, "main.py", "config"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ config command works")
            print(f"Output: {result.stdout}")
            return True
        else:
            print(f"❌ config command failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ config command error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing ABAP Code Assistant Python Backend")
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print(f"Current directory: {os.getcwd()}")
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed")
        return False
    
    # Test main module
    if not test_main_module():
        print("\n❌ Main module test failed")
        return False
    
    # Test config command
    if not test_config_command():
        print("\n❌ Config command test failed")
        return False
    
    print("\n✅ All tests passed!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 