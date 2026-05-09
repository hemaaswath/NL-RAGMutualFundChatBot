#!/usr/bin/env python3
"""
Comprehensive test and fix for SIP amount and session state issues
"""

import os
import sys
import json
from pathlib import Path

# Add Docs/src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "Docs" / "src"))

def test_comprehensive():
    """Test all issues comprehensively."""
    print("=" * 80)
    print("COMPREHENSIVE FIX TEST")
    print("=" * 80)
    
    issues_found = []
    
    # Test 1: Clear cache completely
    print("\n1. Clearing cache completely...")
    try:
        import shutil
        if os.path.exists("cache"):
            shutil.rmtree("cache", ignore_errors=True)
            print("   ✅ Cache cleared")
        else:
            print("   ℹ️  No cache to clear")
    except Exception as e:
        print(f"   ❌ Cache clear failed: {e}")
        issues_found.append(f"Cache clear: {e}")
    
    # Test 2: SIP amount query with fresh pipeline
    print("\n2. Testing SIP amount query with fresh pipeline...")
    try:
        from phase2.pipeline import rag_pipeline
        
        result1 = rag_pipeline("What is the minimum SIP amount?", use_cache=False)
        print(f"   Query Type: {result1.get('query_type', 'N/A')}")
        print(f"   Chunks Retrieved: {result1.get('chunks_retrieved', 'N/A')}")
        print(f"   Answer: {result1.get('answer', 'N/A')[:150]}...")
        
        # Check if answer contains SIP information
        answer1 = result1.get('answer', '').lower()
        sip_keywords = ['sip', 'minimum', 'amount', '₹', 'rs.']
        has_sip_info = any(keyword in answer1 for keyword in sip_keywords)
        
        if has_sip_info:
            print("   ✅ Answer contains SIP information")
        else:
            print("   ❌ Answer missing SIP information")
            issues_found.append("SIP information not found in answer")
        
    except Exception as e:
        print(f"   ❌ SIP query failed: {e}")
        issues_found.append(f"SIP query: {e}")
    
    # Test 3: Different query to check session state
    print("\n3. Testing different query to check session state...")
    try:
        result2 = rag_pipeline("What is expense ratio?", use_cache=True)
        print(f"   Query Type: {result2.get('query_type', 'N/A')}")
        print(f"   Chunks Retrieved: {result2.get('chunks_retrieved', 'N/A')}")
        print(f"   Cached: {result2.get('cached', 'N/A')}")
        print(f"   Answer: {result2.get('answer', 'N/A')[:100]}...")
        
        # Check if answers are different
        answers_different = result1.get('answer', '') != result2.get('answer', '')
        
        if answers_different:
            print("   ✅ Different answers for different queries")
        else:
            print("   ❌ Same answer for different queries")
            issues_found.append("Session state issue - same answers")
        
    except Exception as e:
        print(f"   ❌ Different query failed: {e}")
        issues_found.append(f"Different query: {e}")
    
    # Test 4: Direct SIP retrieval check
    print("\n4. Testing direct SIP retrieval...")
    try:
        from phase2.simple_retriever import retrieve_simple
        
        chunks = retrieve_simple("minimum SIP amount", top_k=5, similarity_threshold=0.3)
        print(f"   Direct retrieval found {len(chunks)} chunks")
        
        if len(chunks) > 0:
            print("   ✅ SIP data found in chunks")
        else:
            print("   ❌ SIP data not found in chunks")
            issues_found.append("Direct SIP retrieval failed")
            
    except Exception as e:
        print(f"   ❌ Direct retrieval failed: {e}")
        issues_found.append(f"Direct retrieval: {e}")
    
    # Test 5: Check chunk data quality
    print("\n5. Checking SIP data quality in chunks...")
    try:
        chunk_files = [
            "data/chunks/hdfc-mid-cap-fund-direct-growth_chunks.json",
            "data/chunks/hdfc-large-cap-fund-direct-growth_chunks.json"
        ]
        
        sip_found_in_chunks = False
        for chunk_file in chunk_files:
            if os.path.exists(chunk_file):
                with open(chunk_file, 'r', encoding='utf-8') as f:
                    chunks = json.load(f)
                    for chunk in chunks:
                        text = chunk.get('text', '').lower()
                        if 'sip' in text and ('minimum' in text or 'amount' in text):
                            print(f"   ✅ Found SIP data in {chunk_file}")
                            sip_found_in_chunks = True
                            break
        
        if not sip_found_in_chunks:
            print("   ❌ No SIP data found in any chunk files")
            issues_found.append("SIP data missing from chunks")
            
    except Exception as e:
        print(f"   ❌ Chunk quality check failed: {e}")
        issues_found.append(f"Chunk quality: {e}")
    
    # Summary
    print("\n" + "=" * 80)
    print("ISSUE SUMMARY")
    print("=" * 80)
    
    if issues_found:
        print(f"❌ Found {len(issues_found)} issues:")
        for i, issue in enumerate(issues_found, 1):
            print(f"   {i}. {issue}")
    else:
        print("✅ No issues found!")
    
    print("\n" + "=" * 80)
    print("RECOMMENDATIONS:")
    print("=" * 80)
    
    if issues_found:
        print("1. Check if SIP data exists in chunk files")
        print("2. Verify similarity threshold is low enough (0.3)")
        print("3. Check cache implementation for session state")
        print("4. Verify response generation handles different contexts")
    else:
        print("✅ All systems working correctly!")
    
    return len(issues_found) == 0

if __name__ == "__main__":
    test_comprehensive()
