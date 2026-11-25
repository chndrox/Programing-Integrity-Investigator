#!/usr/bin/env python
"""
Test script to verify complete login flow:
1. Health check
2. Login endpoint exists
3. Demo credentials work
4. JWT token is valid
5. Token can be used for protected endpoints
"""

import httpx
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

def test_health():
    """Test backend health."""
    print("\n1. Testing Backend Health")
    print("-" * 60)
    
    try:
        resp = httpx.get(f"{BASE_URL}/health", timeout=5)
        if resp.status_code == 200:
            print("✓ Health check: 200 OK")
            print(f"  Response: {resp.json()}")
            return True
        else:
            print(f"✗ Health check failed: {resp.status_code}")
            return False
    except Exception as e:
        print(f"✗ Health check error: {e}")
        return False


def test_endpoint_exists():
    """Check if login endpoint is registered."""
    print("\n2. Checking Login Endpoint Registration")
    print("-" * 60)
    
    try:
        resp = httpx.get(f"{BASE_URL}/openapi.json", timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            paths = data.get("paths", {})
            
            if "/api/auth/login" in paths:
                print("✓ Login endpoint registered: /api/auth/login")
                methods = list(paths["/api/auth/login"].keys())
                print(f"  Methods: {methods}")
                return True
            else:
                print("✗ Login endpoint not found")
                print(f"  Available auth endpoints: {[p for p in paths if 'auth' in p]}")
                return False
        else:
            print(f"✗ OpenAPI schema not found: {resp.status_code}")
            return False
    except Exception as e:
        print(f"✗ Endpoint check error: {e}")
        return False


def test_login_credentials():
    """Test login with demo credentials."""
    print("\n3. Testing Login with Demo Credentials")
    print("-" * 60)
    
    credentials = {
        "username": "instructor1",
        "password": "password123"
    }
    
    print(f"Username: {credentials['username']}")
    print(f"Password: {credentials['password']}")
    
    try:
        resp = httpx.post(
            f"{BASE_URL}/api/auth/login",
            json=credentials,
            timeout=5
        )
        
        print(f"\nStatus Code: {resp.status_code}")
        
        if resp.status_code == 200:
            data = resp.json()
            print("✓ Login successful: 200 OK")
            
            # Check response structure
            required_fields = ["access_token", "token_type", "user"]
            for field in required_fields:
                if field in data:
                    print(f"  ✓ {field}: present")
                else:
                    print(f"  ✗ {field}: missing")
                    return False
            
            print(f"\nToken Type: {data['token_type']}")
            print(f"Token (first 50 chars): {data['access_token'][:50]}...")
            print(f"\nUser Info:")
            print(f"  ID: {data['user']['id']}")
            print(f"  Username: {data['user']['username']}")
            print(f"  Email: {data['user']['email']}")
            print(f"  Full Name: {data['user']['full_name']}")
            print(f"  Role: {data['user']['role']}")
            
            return data["access_token"]
        
        elif resp.status_code == 401:
            print("✗ Login failed: 401 Unauthorized")
            print(f"  Error: {resp.json().get('detail', 'Unknown error')}")
            return False
        
        else:
            print(f"✗ Unexpected status code: {resp.status_code}")
            print(f"  Response: {resp.text}")
            return False
            
    except Exception as e:
        print(f"✗ Login error: {e}")
        return False


def test_protected_endpoint(token):
    """Test accessing protected endpoint with token."""
    print("\n4. Testing Protected Endpoint with Token")
    print("-" * 60)
    
    if not token:
        print("✗ No token provided")
        return False
    
    try:
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        resp = httpx.get(
            f"{BASE_URL}/api/dashboard/stats",
            headers=headers,
            timeout=5
        )
        
        print(f"Status Code: {resp.status_code}")
        
        if resp.status_code == 200:
            print("✓ Protected endpoint accessible with token: 200 OK")
            data = resp.json()
            print(f"\nDashboard Stats:")
            print(f"  Total Submissions: {data['total_submissions']}")
            print(f"  Active Investigations: {data['active_investigations']}")
            print(f"  Completed Investigations: {data['completed_investigations']}")
            print(f"  Cases Requiring Review: {data['cases_requiring_review']}")
            return True
        elif resp.status_code == 401:
            print("✗ Unauthorized (401) - Token may be invalid")
            return False
        else:
            print(f"✗ Unexpected status: {resp.status_code}")
            return False
            
    except Exception as e:
        print(f"✗ Protected endpoint error: {e}")
        return False


def main():
    print("=" * 60)
    print("PII LOGIN FLOW TEST")
    print("=" * 60)
    
    results = []
    
    # Test 1: Health
    results.append(("Health Check", test_health()))
    
    # Test 2: Endpoint exists
    results.append(("Endpoint Registration", test_endpoint_exists()))
    
    # Test 3: Login
    token = test_login_credentials()
    results.append(("Login Flow", token is not False))
    
    # Test 4: Protected endpoint
    if token:
        results.append(("Protected Endpoint", test_protected_endpoint(token)))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "PASS" if passed else "FAIL"
        symbol = "✓" if passed else "✗"
        print(f"{symbol} {test_name}: {status}")
    
    all_passed = all(result for _, result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ ALL TESTS PASSED - Login flow is working!")
    else:
        print("✗ SOME TESTS FAILED - Check output above")
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    exit(main())
