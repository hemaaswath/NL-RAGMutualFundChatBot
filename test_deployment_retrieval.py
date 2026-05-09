#!/usr/bin/env python3
"""
Unit test for debugging data retrieval on Streamlit deployment.
Tests each component of the retrieval pipeline step by step.
"""

import os
import sys
import json
from pathlib import Path

# Add Docs/src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "Docs" / "src"))

def test_environment():
    """Test the deployment environment."""
    print("=" * 60)
    print("1. ENVIRONMENT TEST")
    print("=" * 60)
    
    print(f"Working directory: {os.getcwd()}")
    print(f"Python path: {sys.path[:3]}")
    print(f"Environment variables:")
    for key in ["STREAMLIT_SERVER_PORT", "STREAMLIT_SHARING", "ANONYMIZED_TELEMETRY"]:
        print(f"  {key}: {os.getenv(key, 'NOT SET')}")
    
    # Check if we're on Streamlit Cloud
    is_streamlit_cloud = (
        os.getenv("STREAMLIT_SERVER_PORT") or 
        os.getenv("STREAMLIT_SHARING") or
        "/app" in os.getcwd()
    )
    print(f"Detected Streamlit Cloud: {is_streamlit_cloud}")
    print()

def test_data_files():
    """Test if data files are accessible."""
    print("=" * 60)
    print("2. DATA FILES TEST")
    print("=" * 60)
    
    # Test chunk files
    chunk_paths = [
        "data/chunks",
        "./data/chunks",
        "Docs/src/data/chunks",
        "./Docs/src/data/chunks",
        "/app/data/chunks",
        str(Path.cwd() / "data" / "chunks"),
    ]
    
    chunks_found = False
    for path in chunk_paths:
        chunks_dir = Path(path)
        if chunks_dir.exists() and any(chunks_dir.iterdir()):
            print(f"✓ Found chunks at: {path}")
            chunk_files = list(chunks_dir.glob("*_chunks.json"))
            print(f"  Files: {[f.name for f in chunk_files]}")
            chunks_found = True
            
            # Test loading one chunk file
            if chunk_files:
                try:
                    with open(chunk_files[0], 'r', encoding='utf-8') as f:
                        chunks = json.load(f)
                    print(f"  ✓ Successfully loaded {len(chunks)} chunks from {chunk_files[0].name}")
                    print(f"  Sample chunk keys: {list(chunks[0].keys()) if chunks else 'None'}")
                except Exception as e:
                    print(f"  ✗ Error loading {chunk_files[0].name}: {e}")
            break
        else:
            print(f"✗ No chunks at: {path}")
    
    if not chunks_found:
        print("ERROR: No chunk files found in any location!")
    
    print()

def test_chromadb():
    """Test ChromaDB connection and schema."""
    print("=" * 60)
    print("3. CHROMADB TEST")
    print("=" * 60)
    
    try:
        # Disable telemetry
        os.environ["ANONYMIZED_TELEMETRY"] = "False"
        os.environ["CHROMA_TELEMETRY"] = "False"
        
        import chromadb
        print(f"✓ ChromaDB imported successfully: {chromadb.__version__}")
        
        # Test client creation
        from phase1.config import CHROMA_PERSIST_DIR
        print(f"ChromaDB path: {CHROMA_PERSIST_DIR}")
        
        client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
        print("✓ ChromaDB client created")
        
        # Test collection
        from phase1.config import CHROMA_COLLECTION_NAME
        print(f"Collection name: {CHROMA_COLLECTION_NAME}")
        
        try:
            collection = client.get_or_create_collection(
                name=CHROMA_COLLECTION_NAME,
                metadata={"hnsw:space": "cosine"}
            )
            print("✓ Collection created/retrieved")
            
            # Test collection count
            count = collection.count()
            print(f"✓ Collection count: {count}")
            
            # Test if we can query (even if empty)
            try:
                results = collection.query(
                    query_embeddings=[[0.1] * 384],  # Dummy embedding
                    n_results=1,
                    include=["documents", "metadatas", "distances"]
                )
                print("✓ Query test successful")
                print(f"  Query results: {len(results['documents'][0]) if results['documents'] else 0} documents")
            except Exception as e:
                print(f"✗ Query test failed: {e}")
                
        except Exception as e:
            print(f"✗ Collection creation failed: {e}")
            print(f"  This is likely the schema incompatibility issue!")
            
    except Exception as e:
        print(f"✗ ChromaDB import/setup failed: {e}")
        print(f"  Error type: {type(e).__name__}")
    
    print()

def test_memory_store():
    """Test the memory store fallback."""
    print("=" * 60)
    print("4. MEMORY STORE TEST")
    print("=" * 60)
    
    try:
        from phase1.memory_vector_store import MemoryVectorStore, get_memory_store
        
        print("✓ Memory store imported")
        
        store = get_memory_store()
        print("✓ Memory store instance created")
        
        # Test loading chunks
        chunk_paths = [
            "data/chunks",
            "./data/chunks",
            "Docs/src/data/chunks",
            "./Docs/src/data/chunks",
            "/app/data/chunks",
        ]
        
        success = store.load_from_chunks(chunk_paths)
        if success:
            print(f"✓ Memory store loaded {store.count()} chunks")
            
            # Test query
            test_query = "What is the expense ratio?"
            results = store.query(test_query, top_k=3)
            print(f"✓ Query test: {len(results)} results retrieved")
            
            if results:
                print(f"  Sample result similarity: {results[0].get('similarity', 'N/A')}")
                print(f"  Sample result text length: {len(results[0].get('text', ''))}")
        else:
            print("✗ Memory store failed to load chunks")
            
    except Exception as e:
        print(f"✗ Memory store test failed: {e}")
        print(f"  Error type: {type(e).__name__}")
        import traceback
        print(f"  Traceback: {traceback.format_exc()}")
    
    print()

def test_retriever():
    """Test the retriever with fallback."""
    print("=" * 60)
    print("5. RETRIEVER TEST")
    print("=" * 60)
    
    try:
        from phase2.retriever import retrieve
        
        print("✓ Retriever imported")
        
        test_query = "What is the expense ratio of HDFC Mid Cap Fund?"
        results = retrieve(test_query, top_k=3)
        
        print(f"✓ Retrieval test: {len(results)} results")
        
        for i, result in enumerate(results):
            print(f"  Result {i+1}:")
            print(f"    Similarity: {result.get('similarity', 'N/A')}")
            print(f"    Text length: {len(result.get('text', ''))}")
            print(f"    Has metadata: {'metadata' in result}")
            
    except Exception as e:
        print(f"✗ Retriever test failed: {e}")
        print(f"  Error type: {type(e).__name__}")
        import traceback
        print(f"  Traceback: {traceback.format_exc()}")
    
    print()

def test_full_pipeline():
    """Test the full RAG pipeline."""
    print("=" * 60)
    print("6. FULL PIPELINE TEST")
    print("=" * 60)
    
    try:
        from phase2.pipeline import rag_pipeline
        
        print("✓ RAG pipeline imported")
        
        test_query = "What is the expense ratio of HDFC Mid Cap Fund?"
        result = rag_pipeline(test_query, use_cache=False)
        
        print(f"✓ Pipeline test completed")
        print(f"  Query type: {result.get('query_type', 'N/A')}")
        print(f"  Chunks retrieved: {result.get('chunks_retrieved', 'N/A')}")
        print(f"  Cached: {result.get('cached', 'N/A')}")
        print(f"  Answer length: {len(result.get('answer', ''))}")
        print(f"  Has sources: {'sources' in result}")
        
        if result.get('answer'):
            print(f"  Answer preview: {result['answer'][:200]}...")
        
    except Exception as e:
        print(f"✗ Full pipeline test failed: {e}")
        print(f"  Error type: {type(e).__name__}")
        import traceback
        print(f"  Traceback: {traceback.format_exc()}")
    
    print()

def main():
    """Run all tests."""
    print("STREAMLIT DEPLOYMENT RETRIEVAL DEBUG TEST")
    print("=" * 60)
    print()
    
    test_environment()
    test_data_files()
    test_chromadb()
    test_memory_store()
    test_retriever()
    test_full_pipeline()
    
    print("=" * 60)
    print("TEST COMPLETED")
    print("=" * 60)

if __name__ == "__main__":
    main()
