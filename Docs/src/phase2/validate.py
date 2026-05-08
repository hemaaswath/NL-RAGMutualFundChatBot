"""
Validation script for Phase 2 RAG Pipeline
Tests the pipeline with various query types
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from phase2.pipeline import rag_pipeline, get_available_schemes, get_cache_stats


def test_factual_queries():
    """Test factual queries."""
    print("=" * 80)
    print("Testing Factual Queries")
    print("=" * 80)
    
    factual_queries = [
        "What is the expense ratio of HDFC Mid Cap Fund?",
        "What is the minimum SIP amount?",
        "What is the NAV of HDFC Equity Fund?",
        "What is the exit load for HDFC Focused Fund?"
    ]
    
    for query in factual_queries:
        print(f"\nQuery: {query}")
        result = rag_pipeline(query, use_cache=False)
        
        print(f"Query Type: {result.get('query_type', 'unknown')}")
        print(f"Chunks Retrieved: {result.get('chunks_retrieved', 0)}")
        print(f"Has Context: {result.get('has_context', False)}")
        print(f"Success: {result.get('success', False)}")
        print(f"\nAnswer: {result.get('answer', 'No answer generated')}")
        print("-" * 80)


def test_advisory_queries():
    """Test advisory queries (should be refused)."""
    print("\n" + "=" * 80)
    print("Testing Advisory Queries (Should Be Refused)")
    print("=" * 80)
    
    advisory_queries = [
        "Should I invest in HDFC Mid Cap Fund?",
        "Which fund is better - HDFC Mid Cap or HDFC Large Cap?",
        "Can you recommend a good mutual fund?",
        "Is this a good investment?"
    ]
    
    for query in advisory_queries:
        print(f"\nQuery: {query}")
        result = rag_pipeline(query, use_cache=False)
        
        print(f"Query Type: {result.get('query_type', 'unknown')}")
        print(f"Refusal Type: {result.get('refusal_type', 'N/A')}")
        print(f"Success: {result.get('success', False)}")
        print(f"\nAnswer: {result.get('answer', 'No answer generated')}")
        print("-" * 80)


def test_scheme_filter():
    """Test scheme-specific filtering."""
    print("\n" + "=" * 80)
    print("Testing Scheme Filter")
    print("=" * 80)
    
    query = "What is the expense ratio?"
    scheme = "HDFC Mid-Cap Fund (Direct Growth)"
    
    print(f"\nQuery: {query}")
    print(f"Scheme Filter: {scheme}")
    result = rag_pipeline(query, scheme=scheme, use_cache=False)
    
    print(f"Chunks Retrieved: {result.get('chunks_retrieved', 0)}")
    print(f"Success: {result.get('success', False)}")
    print(f"\nAnswer: {result.get('answer', 'No answer generated')}")
    print("-" * 80)


def test_cache():
    """Test caching functionality."""
    print("\n" + "=" * 80)
    print("Testing Cache Functionality")
    print("=" * 80)
    
    query = "What is the expense ratio?"
    
    print(f"\nQuery: {query}")
    
    # First call - not cached
    result1 = rag_pipeline(query, use_cache=True)
    print(f"First call - Cached: {result1.get('cached', False)}")
    
    # Second call - should be cached
    result2 = rag_pipeline(query, use_cache=True)
    print(f"Second call - Cached: {result2.get('cached', False)}")
    
    # Cache stats
    stats = get_cache_stats()
    print(f"\nCache Stats: {stats}")
    print("-" * 80)


def main():
    """Run all validation tests."""
    print("\n")
    print("*" * 80)
    print("Phase 2 RAG Pipeline Validation")
    print("*" * 80)
    
    try:
        # Test factual queries
        test_factual_queries()
        
        # Test advisory queries
        test_advisory_queries()
        
        # Test scheme filter
        test_scheme_filter()
        
        # Test cache
        test_cache()
        
        # Get available schemes
        print("\n" + "=" * 80)
        print("Available Schemes")
        print("=" * 80)
        schemes = get_available_schemes()
        for scheme in schemes:
            print(f"  - {scheme}")
        
        print("\n" + "*" * 80)
        print("✅ Phase 2 Validation Complete")
        print("*" * 80 + "\n")
        
    except Exception as e:
        print(f"\n❌ Validation Error: {e}")
        import traceback
        print(traceback.format_exc())


if __name__ == "__main__":
    main()
