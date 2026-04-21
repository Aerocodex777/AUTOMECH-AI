#!/usr/bin/env python3
"""
Test script to verify AutoMech deployment configuration
Run this before deploying to production
"""
import os
import sys
from dotenv import load_dotenv

def test_environment():
    """Test environment variables"""
    print("🔍 Testing Environment Configuration...\n")
    
    load_dotenv("backend/.env")
    
    tests_passed = 0
    tests_failed = 0
    
    # Test 1: Groq API Key
    print("1. Testing GROQ_API_KEY...")
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key and groq_key != "your_groq_api_key_here" and groq_key.startswith("gsk_"):
        print("   ✅ GROQ_API_KEY is configured")
        tests_passed += 1
    else:
        print("   ❌ GROQ_API_KEY is missing or invalid")
        print("      Get your key from: https://console.groq.com/keys")
        tests_failed += 1
    
    # Test 2: Cloud LLM preference
    print("\n2. Testing PREFER_CLOUD_LLM...")
    prefer_cloud = os.getenv("PREFER_CLOUD_LLM", "false")
    print(f"   ℹ️  PREFER_CLOUD_LLM = {prefer_cloud}")
    if prefer_cloud.lower() == "true":
        print("   ✅ Configured for cloud deployment (recommended for hosting)")
    else:
        print("   ⚠️  Will try local Ollama first (good for development)")
    tests_passed += 1
    
    # Test 3: JWT Secret
    print("\n3. Testing JWT_SECRET_KEY...")
    jwt_secret = os.getenv("JWT_SECRET_KEY")
    if jwt_secret and len(jwt_secret) >= 32:
        if jwt_secret == "automech-super-secret-key-change-this-in-production-min-32-characters-long":
            print("   ⚠️  Using default JWT secret (CHANGE THIS IN PRODUCTION!)")
            tests_passed += 1
        else:
            print("   ✅ JWT_SECRET_KEY is configured with custom value")
            tests_passed += 1
    else:
        print("   ❌ JWT_SECRET_KEY is missing or too short (need 32+ characters)")
        tests_failed += 1
    
    # Test 4: Database URL
    print("\n4. Testing DATABASE_URL...")
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        if "postgresql" in db_url:
            print("   ✅ Using PostgreSQL (recommended for production)")
        elif "sqlite" in db_url:
            print("   ⚠️  Using SQLite (OK for development, use PostgreSQL for production)")
        else:
            print(f"   ℹ️  Database: {db_url.split(':')[0]}")
        tests_passed += 1
    else:
        print("   ℹ️  No DATABASE_URL set (will use SQLite by default)")
        tests_passed += 1
    
    # Summary
    print("\n" + "="*60)
    print(f"📊 Test Results: {tests_passed} passed, {tests_failed} failed")
    print("="*60)
    
    if tests_failed > 0:
        print("\n❌ Configuration issues found. Please fix before deploying.")
        return False
    else:
        print("\n✅ Configuration looks good!")
        return True


def test_groq_connection():
    """Test actual connection to Groq API"""
    print("\n🌐 Testing Groq API Connection...\n")
    
    try:
        from groq import Groq
        load_dotenv("backend/.env")
        
        groq_key = os.getenv("GROQ_API_KEY")
        if not groq_key or groq_key == "your_groq_api_key_here":
            print("❌ Cannot test connection: GROQ_API_KEY not configured")
            return False
        
        client = Groq(api_key=groq_key)
        
        print("Sending test request to Groq API...")
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": "Say 'test successful' if you can read this"}],
            max_tokens=50
        )
        
        result = response.choices[0].message.content
        print(f"Response: {result}")
        print("\n✅ Groq API connection successful!")
        return True
        
    except ImportError:
        print("⚠️  Groq package not installed. Run: pip install groq")
        return False
    except Exception as e:
        print(f"❌ Groq API connection failed: {e}")
        print("\nPossible issues:")
        print("  - Invalid API key")
        print("  - No internet connection")
        print("  - Groq API is down")
        print("  - Rate limit exceeded")
        return False


def test_dependencies():
    """Test if all required packages are installed"""
    print("\n📦 Testing Dependencies...\n")
    
    required_packages = [
        "fastapi",
        "uvicorn",
        "langchain",
        "langchain_groq",
        "chromadb",
        "sentence_transformers",
        "groq",
        "python-dotenv",
        "sqlalchemy",
    ]
    
    missing = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} (missing)")
            missing.append(package)
    
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print("Run: pip install -r backend/requirements.txt")
        return False
    else:
        print("\n✅ All dependencies installed")
        return True


def main():
    """Run all tests"""
    print("="*60)
    print("🚀 AutoMech Deployment Test")
    print("="*60)
    
    # Test 1: Dependencies
    deps_ok = test_dependencies()
    
    # Test 2: Environment
    env_ok = test_environment()
    
    # Test 3: Groq connection (only if env is OK)
    groq_ok = False
    if env_ok:
        groq_ok = test_groq_connection()
    
    # Final summary
    print("\n" + "="*60)
    print("📋 FINAL SUMMARY")
    print("="*60)
    print(f"Dependencies: {'✅ PASS' if deps_ok else '❌ FAIL'}")
    print(f"Environment:  {'✅ PASS' if env_ok else '❌ FAIL'}")
    print(f"Groq API:     {'✅ PASS' if groq_ok else '❌ FAIL'}")
    print("="*60)
    
    if deps_ok and env_ok and groq_ok:
        print("\n🎉 All tests passed! Ready to deploy!")
        print("\nNext steps:")
        print("  1. Review HOSTING_GUIDE.md for deployment instructions")
        print("  2. Set PREFER_CLOUD_LLM=true for production")
        print("  3. Use PostgreSQL for production database")
        print("  4. Generate a secure JWT_SECRET_KEY")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please fix issues before deploying.")
        print("\nSee HOSTING_GUIDE.md for help.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
