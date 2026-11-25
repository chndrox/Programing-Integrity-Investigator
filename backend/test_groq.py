#!/usr/bin/env python
"""Test Groq API integration."""

import asyncio
from app.database import settings
from app.services.groq_service import get_groq_service


async def test_groq_connection():
    """Test Groq API connection and response."""
    print("=" * 60)
    print("GROQ API INTEGRATION TEST")
    print("=" * 60)
    print()
    
    # Check configuration
    print("1. Configuration Check")
    print("-" * 60)
    api_key_preview = f"{settings.groq_api_key[:20]}...{settings.groq_api_key[-10:]}"
    print(f"   API Key: {api_key_preview}")
    print(f"   Model: {settings.groq_model}")
    print(f"   ✓ Configuration loaded")
    print()
    
    # Initialize service
    print("2. Service Initialization")
    print("-" * 60)
    try:
        groq_service = get_groq_service()
        print(f"   ✓ Groq service initialized")
        print(f"   Model: {groq_service.model}")
        print()
    except Exception as e:
        print(f"   ✗ Failed to initialize: {e}")
        return False
    
    # Test API call
    print("3. API Connection Test")
    print("-" * 60)
    try:
        print("   Sending test request to Groq...")
        response = await groq_service.analyze_text(
            prompt="Say 'Groq API is working!' if you can read this.",
            system_prompt="You are a helpful assistant. Respond concisely in one sentence.",
            temperature=0.1
        )
        
        print(f"   ✓ API call successful")
        response_text = response.get('text', response.get('raw', str(response)))
        print(f"   Response: {response_text}")
        print()
        
        return True
        
    except Exception as e:
        print(f"   ✗ API call failed: {e}")
        print()
        print("   Troubleshooting:")
        print("   - Verify API key is correct in .env file")
        print("   - Check internet connection")
        print("   - Verify Groq service status at https://status.groq.com")
        return False


async def test_code_analysis():
    """Test Groq with code analysis task."""
    print("4. Code Analysis Test")
    print("-" * 60)
    
    groq_service = get_groq_service()
    
    test_code1 = 'def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)'
    test_code2 = 'def fib(n):\n    if n <= 1:\n        return n\n    return fib(n-1) + fib(n-2)'
    
    try:
        print("   Analyzing code similarity...")
        response = await groq_service.analyze_code_similarity(test_code1, test_code2)
        
        print(f"   ✓ Code analysis successful")
        if isinstance(response, dict):
            similarity = response.get('similarity_percentage', 'N/A')
            print(f"   Similarity: {similarity}%")
            confidence = response.get('confidence_level', 'N/A')
            print(f"   Confidence: {confidence}")
        else:
            print(f"   Response: {str(response)[:100]}...")
        print()
        return True
        
    except Exception as e:
        print(f"   ✗ Code analysis failed: {e}")
        return False


async def main():
    """Run all tests."""
    
    # Test 1: Basic connection
    test1 = await test_groq_connection()
    
    if test1:
        # Test 2: Code analysis
        test2 = await test_code_analysis()
        
        print("=" * 60)
        if test1 and test2:
            print("✓ ALL TESTS PASSED")
            print()
            print("Groq integration is working correctly!")
            print("Your AI agents are ready to analyze code submissions.")
        else:
            print("✗ SOME TESTS FAILED")
            print()
            print("Please check the error messages above.")
        print("=" * 60)
        
        return test1 and test2
    else:
        print("=" * 60)
        print("✗ CONNECTION TEST FAILED")
        print()
        print("Please verify:")
        print("1. API key is correct in .env file")
        print("2. Internet connection is active")
        print("3. Groq service is operational")
        print("=" * 60)
        return False


if __name__ == "__main__":
    try:
        result = asyncio.run(main())
        exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n\n✗ Unexpected error: {e}")
        exit(1)
