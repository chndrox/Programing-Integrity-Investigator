#!/usr/bin/env python
"""Comprehensive backend verification script."""

import sys
import httpx

def test_imports():
    """Test all module imports."""
    print("\n=== Testing Module Imports ===")
    try:
        import pydantic
        print(f"✓ Pydantic {pydantic.__version__}")
        
        from pydantic_core import core_schema
        print("✓ Pydantic-core")
        
        from app.database import engine, Base, get_db, settings
        print("✓ app.database")
        
        from app.models import (
            User, Student, Assignment, Submission, Investigation,
            CommitHistory, AuditLog, InstructorDecision, CaseReport
        )
        print("✓ app.models")
        
        from app.schemas import UserResponse, StudentResponse
        print("✓ app.schemas")
        
        from app.api.auth import get_current_user, create_access_token
        print("✓ app.api.auth")
        
        from app.orchestrator.agent_orchestrator import AgentOrchestrator
        print("✓ app.orchestrator.agent_orchestrator")
        
        from app.mcp.submissions_mcp import SubmissionsMCP
        print("✓ app.mcp.submissions_mcp")
        
        from app.main import app
        print(f"✓ app.main (FastAPI title: {app.title})")
        
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False


def test_endpoints():
    """Test API endpoints."""
    print("\n=== Testing API Endpoints ===")
    
    base_url = "http://127.0.0.1:8000"
    
    try:
        # Test health endpoint
        resp = httpx.get(f"{base_url}/health", timeout=5)
        if resp.status_code == 200 and resp.json().get("status") == "healthy":
            print("✓ GET /health - Status 200, Response: {'status': 'healthy'}")
        else:
            print(f"✗ GET /health - Status {resp.status_code}")
            return False
        
        # Test OpenAPI schema
        resp = httpx.get(f"{base_url}/openapi.json", timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            print(f"✓ GET /openapi.json - Status 200, {len(data.get('paths', {}))} endpoints")
        else:
            print(f"✗ GET /openapi.json - Status {resp.status_code}")
            return False
        
        # Test Swagger UI
        resp = httpx.get(f"{base_url}/docs", timeout=5)
        if resp.status_code == 200 and ("swagger" in resp.text.lower() or "openapi" in resp.text.lower()):
            print("✓ GET /docs - Swagger UI accessible")
        else:
            print(f"✗ GET /docs - Status {resp.status_code}")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ Endpoint test failed: {e}")
        return False


def main():
    """Run all verification tests."""
    print("=" * 60)
    print("BACKEND VERIFICATION TEST")
    print("=" * 60)
    
    imports_ok = test_imports()
    endpoints_ok = test_endpoints()
    
    print("\n" + "=" * 60)
    if imports_ok and endpoints_ok:
        print("✓ ALL TESTS PASSED - Backend is ready")
        print("=" * 60)
        return 0
    else:
        print("✗ SOME TESTS FAILED")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
