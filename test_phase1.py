"""
Test Phase 1: Vector store and embeddings
"""

import sys
from pathlib import Path

# Add Docs/src to Python path
sys.path.insert(0, str(Path(__file__).parent / "Docs" / "src"))

print("=" * 80)
print("Testing Phase 1: Vector Store and Embeddings")
print("=" * 80)

# Test 1: Config
print("\n[1] Testing config...")
try:
    from phase1.config import PROJECT_ROOT, CHROMA_PERSIST_DIR, CHROMA_COLLECTION_NAME
    print(f"[OK] PROJECT_ROOT: {PROJECT_ROOT}")
    print(f"[OK] CHROMA_PERSIST_DIR: {CHROMA_PERSIST_DIR}")
    print(f"[OK] CHROMA_COLLECTION_NAME: {CHROMA_COLLECTION_NAME}")
except Exception as e:
    print(f"[FAIL] Config error: {e}")
    sys.exit(1)

# Test 2: Embeddings
print("\n[2] Testing embeddings...")
try:
    from phase1.embeddings import generate_single_embedding
    test_embedding = generate_single_embedding("test query")
    print(f"[OK] Embedding generated: shape {len(test_embedding)}")
    assert len(test_embedding) == 384, "Embedding dimension should be 384"
    print("[OK] Embedding dimension correct (384)")
except Exception as e:
    print(f"[FAIL] Embeddings error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: Vector Store Client
print("\n[3] Testing ChromaDB client...")
try:
    from phase1.vector_store import get_client
    client = get_client()
    print(f"[OK] ChromaDB client created: {type(client)}")
except Exception as e:
    print(f"[FAIL] ChromaDB client error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Collection
print("\n[4] Testing collection...")
try:
    from phase1.vector_store import get_or_create_collection
    collection = get_or_create_collection()
    print(f"[OK] Collection created/retrieved: {collection.name}")
    print(f"[OK] Collection count: {collection.count()}")
except Exception as e:
    print(f"[FAIL] Collection error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 5: Chunker
print("\n[5] Testing chunker...")
try:
    from phase1.chunker import chunk_all_schemes
    chunks = chunk_all_schemes()
    print(f"[OK] Chunks generated: {len(chunks)} chunks")
    if chunks:
        print(f"[OK] Sample chunk keys: {list(chunks[0].keys())}")
except Exception as e:
    print(f"[FAIL] Chunker error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 80)
print("Phase 1 tests completed successfully!")
print("=" * 80)
