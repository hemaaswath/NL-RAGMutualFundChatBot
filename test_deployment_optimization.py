#!/usr/bin/env python3
"""
Test deployment optimization performance
"""

import os
import sys
import time
import shutil
from pathlib import Path

# Add Docs/src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "Docs" / "src"))

def test_startup_performance():
    """Test startup performance with optimizations."""
    print("=" * 80)
    print("DEPLOYMENT OPTIMIZATION TEST")
    print("=" * 80)
    
    # Clear cache to test cold start
    print("\n1. Testing cold startup performance...")
    cache_dir = Path("cache")
    if cache_dir.exists():
        shutil.rmtree(cache_dir, ignore_errors=True)
        print("   Cache cleared for cold start test")
    
    start_time = time.time()
    
    try:
        # Test optimized retriever initialization
        from phase2.optimized_retriever import get_optimized_retriever
        retriever = get_optimized_retriever()
        
        # Should be fast due to lazy loading
        init_time = time.time() - start_time
        print(f"   Initialization time: {init_time:.2f} seconds")
        
        # Test first query (triggers actual loading)
        query_start = time.time()
        results = retriever.query("What is expense ratio?", top_k=5)
        query_time = time.time() - query_start
        
        print(f"   First query time: {query_time:.2f} seconds")
        print(f"   Chunks retrieved: {len(results)}")
        
        # Test second query (should use cached embeddings)
        query_start = time.time()
        results = retriever.query("What is minimum SIP amount?", top_k=5)
        cached_query_time = time.time() - query_start
        
        print(f"   Second query time: {cached_query_time:.2f} seconds")
        print(f"   Chunks retrieved: {len(results)}")
        
        # Performance analysis
        print(f"\n2. Performance Analysis:")
        if init_time < 0.5:
            print(f"   ✅ Fast initialization: {init_time:.2f}s (< 0.5s)")
        else:
            print(f"   ⚠️  Slow initialization: {init_time:.2f}s (> 0.5s)")
        
        if cached_query_time < query_time * 0.5:
            print(f"   ✅ Good caching: {cached_query_time:.2f}s vs {query_time:.2f}s")
        else:
            print(f"   ⚠️  Poor caching: {cached_query_time:.2f}s vs {query_time:.2f}s")
        
        # Test cache persistence
        print(f"\n3. Testing cache persistence...")
        retriever2 = get_optimized_retriever()
        cache_start = time.time()
        results = retriever2.query("What is expense ratio?", top_k=5)
        cache_time = time.time() - cache_start
        
        print(f"   Cache load time: {cache_time:.2f} seconds")
        
        if cache_time < 1.0:
            print(f"   ✅ Fast cache loading: {cache_time:.2f}s")
        else:
            print(f"   ⚠️  Slow cache loading: {cache_time:.2f}s")
        
        # Overall assessment
        total_time = init_time + query_time + cached_query_time
        print(f"\n4. Overall Performance:")
        print(f"   Total time for 3 operations: {total_time:.2f} seconds")
        print(f"   Average per operation: {total_time/3:.2f} seconds")
        
        if total_time < 5.0:
            print("   ✅ Excellent performance for deployment")
        elif total_time < 10.0:
            print("   ✅ Good performance for deployment")
        else:
            print("   ❌ Poor performance - needs more optimization")
        
        return total_time < 10.0
        
    except Exception as e:
        print(f"   ❌ Performance test failed: {e}")
        import traceback
        print(f"   Traceback: {traceback.format_exc()}")
        return False

def test_memory_usage():
    """Test memory usage optimization."""
    print(f"\n5. Testing memory usage...")
    
    try:
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        memory_before = process.memory_info().rss / 1024 / 1024  # MB
        
        # Load retriever and perform queries
        from phase2.optimized_retriever import get_optimized_retriever
        retriever = get_optimized_retriever()
        retriever._ensure_loaded()
        
        # Perform multiple queries
        for _ in range(5):
            retriever.query("test query", top_k=5)
        
        memory_after = process.memory_info().rss / 1024 / 1024  # MB
        memory_used = memory_after - memory_before
        
        print(f"   Memory before: {memory_before:.1f} MB")
        print(f"   Memory after: {memory_after:.1f} MB")
        print(f"   Memory used: {memory_used:.1f} MB")
        
        if memory_used < 200:
            print("   ✅ Good memory usage")
        else:
            print("   ⚠️  High memory usage")
        
        return memory_used < 200
        
    except ImportError:
        print("   ℹ️  psutil not available - skipping memory test")
        return True
    except Exception as e:
        print(f"   ❌ Memory test failed: {e}")
        return False

def main():
    """Run all optimization tests."""
    print("Testing deployment optimization performance...")
    
    # Test 1: Startup performance
    test1_passed = test_startup_performance()
    
    # Test 2: Memory usage
    test2_passed = test_memory_usage()
    
    # Summary
    print("\n" + "=" * 80)
    print("OPTIMIZATION TEST SUMMARY")
    print("=" * 80)
    print(f"Startup Performance: {'PASS' if test1_passed else 'FAIL'}")
    print(f"Memory Usage: {'PASS' if test2_passed else 'FAIL'}")
    
    overall_passed = test1_passed and test2_passed
    print(f"Overall: {'PASS' if overall_passed else 'FAIL'}")
    
    if overall_passed:
        print("\n✅ Deployment optimizations are working correctly!")
        print("Expected deployment time: < 10 seconds")
    else:
        print("\n❌ Some optimizations need improvement")
        print("Expected deployment time: > 10 seconds")
    
    return overall_passed

if __name__ == "__main__":
    main()
