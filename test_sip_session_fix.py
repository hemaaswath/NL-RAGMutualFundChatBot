#!/usr/bin/env python3
"""
Test SIP amount query and session state issues
"""

import os
import sys
from pathlib import Path

# Add Docs/src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "Docs" / "src"))

def test_sip_query():
    """Test SIP amount query specifically."""
    print("=" * 60)
    print("TESTING SIP AMOUNT QUERY")
    print("=" * 60)
    
    try:
        from phase2.pipeline import rag_pipeline
        
        # Clear cache first
        import shutil
        if os.path.exists("cache"):
            shutil.rmtree("cache", ignore_errors=True)
            print("Cache cleared")
        
        # Test 1: SIP amount query
        print("\n1. Testing: 'What is the minimum SIP amount?'")
        result1 = rag_pipeline("What is the minimum SIP amount?", use_cache=False)
        print(f"   Query Type: {result1.get('query_type', 'N/A')}")
        print(f"   Chunks Retrieved: {result1.get('chunks_retrieved', 'N/A')}")
        print(f"   Answer: {result1.get('answer', 'N/A')[:100]}...")
        
        # Test 2: Same query again (should use cache)
        print("\n2. Testing same query again (should use cache):")
        result2 = rag_pipeline("What is the minimum SIP amount?", use_cache=True)
        print(f"   Query Type: {result2.get('query_type', 'N/A')}")
        print(f"   Chunks Retrieved: {result2.get('chunks_retrieved', 'N/A')}")
        print(f"   Cached: {result2.get('cached', 'N/A')}")
        print(f"   Answer: {result2.get('answer', 'N/A')[:100]}...")
        
        # Test 3: Different query
        print("\n3. Testing different query: 'What is expense ratio?'")
        result3 = rag_pipeline("What is expense ratio?", use_cache=True)
        print(f"   Query Type: {result3.get('query_type', 'N/A')}")
        print(f"   Chunks Retrieved: {result3.get('chunks_retrieved', 'N/A')}")
        print(f"   Cached: {result3.get('cached', 'N/A')}")
        print(f"   Answer: {result3.get('answer', 'N/A')[:100]}...")
        
        # Check if results are different
        answers_different = result1.get('answer') != result3.get('answer')
        query_types_different = result1.get('query_type') != result3.get('query_type')
        
        print(f"\n" + "=" * 60)
        print("RESULTS ANALYSIS:")
        print(f"  Different answers between queries: {answers_different}")
        print(f"  Different query types: {query_types_different}")
        
        if answers_different:
            print("  ❌ ISSUE: Same answer returned for different queries!")
        else:
            print("  ✅ Different answers for different queries")
            
        if query_types_different:
            print("  ✅ Correct classification for different query types")
        else:
            print("  ❌ ISSUE: Same query type for different queries!")
        
        return not answers_different and not query_types_different
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return False

def test_direct_retrieval():
    """Test direct retrieval to see if SIP data exists."""
    print("\n" + "=" * 60)
    print("TESTING DIRECT RETRIEVAL")
    print("=" * 60)
    
    try:
        from phase2.simple_retriever import retrieve_simple
        
        # Test direct retrieval
        chunks = retrieve_simple("minimum SIP amount", top_k=5, similarity_threshold=0.3)
        print(f"Direct retrieval found {len(chunks)} chunks")
        
        for i, chunk in enumerate(chunks[:2]):
            print(f"  Chunk {i+1}: {chunk['text'][:100]}...")
            
        return len(chunks) > 0
        
    except Exception as e:
        print(f"✗ Direct retrieval failed: {e}")
        return False

def main():
    """Run all tests."""
    print("SIP AMOUNT AND SESSION STATE TESTS")
    
    # Test 1: SIP query through pipeline
    test1_passed = test_sip_query()
    
    # Test 2: Direct retrieval
    test2_passed = test_direct_retrieval()
    
    print("\n" + "=" * 60)
    print("OVERALL RESULTS:")
    print("=" * 60)
    print(f"SIP Query Test: {'PASS' if test1_passed else 'FAIL'}")
    print(f"Direct Retrieval Test: {'PASS' if test2_passed else 'FAIL'}")
    
    overall_passed = test1_passed and test2_passed
    print(f"Overall: {'PASS' if overall_passed else 'FAIL'}")
    
    if overall_passed:
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Some tests failed!")

if __name__ == "__main__":
    main()
