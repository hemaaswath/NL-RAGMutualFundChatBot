"""
Test Phase 2: RAG Pipeline
"""

import sys
from pathlib import Path

# Add Docs/src to Python path
sys.path.insert(0, str(Path(__file__).parent / "Docs" / "src"))

print("=" * 80)
print("Testing Phase 2: RAG Pipeline")
print("=" * 80)

# Test 1: Config
print("\n[1] Testing config...")
try:
    from phase2.config import TOP_K, SIMILARITY_THRESHOLD, GROQ_API_KEY
    print(f"✓ TOP_K: {TOP_K}")
    print(f"✓ SIMILARITY_THRESHOLD: {SIMILARITY_THRESHOLD}")
    print(f"✓ GROQ_API_KEY: {'SET' if GROQ_API_KEY else 'NOT SET'}")
except Exception as e:
    print(f"✗ Config error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 2: Classifier
print("\n[2] Testing classifier...")
try:
    from phase2.classifier import classify_query, should_refuse
    query_type = classify_query("What is the expense ratio?")
    print(f"✓ Query classification: {query_type}")
    refusal = should_refuse("What is the stock price of HDFC?")
    print(f"✓ Refusal check: {refusal}")
except Exception as e:
    print(f"✗ Classifier error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: Retriever
print("\n[3] Testing retriever...")
try:
    from phase2.retriever import retrieve
    results = retrieve("What is the expense ratio of HDFC Mid Cap Fund?")
    print(f"✓ Retrieved {len(results)} chunks")
    if results:
        print(f"✓ Sample result keys: {list(results[0].keys())}")
except Exception as e:
    print(f"✗ Retriever error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Generator
print("\n[4] Testing generator...")
try:
    from phase2.generator import generate_response
    if GROQ_API_KEY:
        response = generate_response("What is the expense ratio?", results[:2])
        print(f"✓ Response generated: {str(response)[:100]}...")
    else:
        print("⚠ Skipping generator test (GROQ_API_KEY not set)")
except Exception as e:
    print(f"✗ Generator error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 5: RAG Pipeline
print("\n[5] Testing RAG pipeline...")
try:
    from phase2.pipeline import rag_pipeline
    if GROQ_API_KEY:
        result = rag_pipeline("What is the expense ratio of HDFC Mid Cap Fund?")
        print(f"✓ Pipeline result type: {result.get('query_type')}")
        print(f"✓ Pipeline answer: {result.get('answer', '')[:100]}...")
    else:
        print("⚠ Skipping pipeline test (GROQ_API_KEY not set)")
except Exception as e:
    print(f"✗ Pipeline error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 80)
print("Phase 2 tests completed successfully!")
print("=" * 80)
