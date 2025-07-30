#!/usr/bin/env python3
"""
Test script to verify AI Town setup
"""

import os
import sys
import importlib.util

def check_python_version():
    """Check if Python 3.7+ is installed"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7+ required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'flask',
        'flask_socketio',
        'python-dotenv',
        'requests',
        'eventlet'
    ]
    
    missing = []
    for package in required_packages:
        spec = importlib.util.find_spec(package)
        if spec is None:
            missing.append(package)
    
    if missing:
        print(f"❌ Missing packages: {', '.join(missing)}")
        return False
    
    print("✅ All dependencies installed")
    return True

def check_env_file():
    """Check if .env file exists and has required variables"""
    if not os.path.exists('.env'):
        print("❌ .env file not found")
        return False
    
    with open('.env', 'r') as f:
        content = f.read()
    
    if 'OPENROUTER_API_KEY=your_api_key_here' in content:
        print("❌ Please update your .env file with a real OpenRouter API key")
        return False
    
    if 'OPENROUTER_API_KEY=' not in content:
        print("❌ OPENROUTER_API_KEY not found in .env")
        return False
    
    print("✅ .env file configured")
    return True

def check_files():
    """Check if all required files exist"""
    required_files = [
        'ai_town.py',
        'town_server.py',
        'templates/town.html',
        'requirements.txt',
        'README.md',
        'start_town.sh'
    ]
    
    missing = []
    for file in required_files:
        if not os.path.exists(file):
            missing.append(file)
    
    if missing:
        print(f"❌ Missing files: {', '.join(missing)}")
        return False
    
    print("✅ All required files present")
    return True

def main():
    """Run all checks"""
    print("🔍 Testing AI Town Setup...")
    print("=" * 40)
    
    checks = [
        check_python_version,
        check_dependencies,
        check_env_file,
        check_files
    ]
    
    passed = 0
    for check in checks:
        if check():
            passed += 1
        print()
    
    print("=" * 40)
    if passed == len(checks):
        print("🎉 All checks passed! AI Town is ready to run.")
        print("Run: ./start_town.sh")
    else:
        print(f"⚠️  {len(checks) - passed} issues found. Please fix them before running.")
        sys.exit(1)

if __name__ == "__main__":
    main()
