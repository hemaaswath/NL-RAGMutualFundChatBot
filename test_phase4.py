"""
Test Phase 4: Streamlit UI
"""

import sys
from pathlib import Path

# Add Docs/src to Python path
sys.path.insert(0, str(Path(__file__).parent / "Docs" / "src"))

print("=" * 80)
print("Testing Phase 4: Streamlit UI")
print("=" * 80)

# Test 1: App imports
print("\n[1] Testing app imports...")
try:
    import streamlit as st
    from phase2.pipeline import rag_pipeline, get_available_schemes, initialize_vector_store
    print(f"✓ Streamlit imported: {st.__version__}")
    print(f"✓ Phase 2 imports successful")
except Exception as e:
    print(f"✗ Import error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 2: Pipeline functions
print("\n[2] Testing pipeline functions...")
try:
    schemes = get_available_schemes()
    print(f"✓ Available schemes: {len(schemes)}")
    if schemes:
        print(f"✓ Sample scheme: {schemes[0]}")
except Exception as e:
    print(f"✗ Pipeline functions error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: Initialize vector store
print("\n[3] Testing initialize_vector_store...")
try:
    initialize_vector_store()
    print(f"✓ Vector store initialization completed")
except Exception as e:
    print(f"✗ Vector store initialization error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 80)
print("Phase 4 tests completed successfully!")
print("=" * 80)
print("\nTo run the Streamlit UI: python run_ui.py")
