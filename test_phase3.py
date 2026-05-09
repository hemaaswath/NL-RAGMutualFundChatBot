"""
Test Phase 3: API Backend
"""

import sys
from pathlib import Path

# Add Docs/src to Python path
sys.path.insert(0, str(Path(__file__).parent / "Docs" / "src"))

print("=" * 80)
print("Testing Phase 3: API Backend")
print("=" * 80)

# Test 1: Config
print("\n[1] Testing config...")
try:
    from phase3.config import API_HOST, API_PORT, CORS_ORIGINS
    print(f"✓ API_HOST: {API_HOST}")
    print(f"✓ API_PORT: {API_PORT}")
    print(f"✓ CORS_ORIGINS: {CORS_ORIGINS}")
except Exception as e:
    print(f"✗ Config error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 2: API Main
print("\n[2] Testing API main import...")
try:
    from phase3.api.main import app, lifespan
    print(f"✓ FastAPI app imported: {type(app)}")
    print(f"✓ Lifespan function imported: {type(lifespan)}")
except Exception as e:
    print(f"✗ API main error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: Service
print("\n[3] Testing RAG service...")
try:
    from phase3.api.services.rag_service import RAGService
    print(f"✓ RAGService class imported")
except Exception as e:
    print(f"✗ RAG service error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Router
print("\n[4] Testing router import...")
try:
    from phase3.api.routes.query import router as query_router
    from phase3.api.routes.health import router as health_router
    from phase3.api.routes.schemes import router as schemes_router
    from phase3.api.routes.feedback import router as feedback_router
    print(f"✓ Query router imported: {type(query_router)}")
    print(f"✓ Health router imported: {type(health_router)}")
    print(f"✓ Schemes router imported: {type(schemes_router)}")
    print(f"✓ Feedback router imported: {type(feedback_router)}")
except Exception as e:
    print(f"✗ Router error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 80)
print("Phase 3 tests completed successfully!")
print("=" * 80)
