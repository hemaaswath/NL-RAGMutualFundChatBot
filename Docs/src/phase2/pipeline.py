"""
Main RAG Pipeline for Phase 2
Orchestrates retrieval, classification, and generation
"""

from typing import Optional
from .config import TOP_K, SIMILARITY_THRESHOLD
from .retriever import retrieve, retrieve_by_scheme
from .classifier import classify_query, should_refuse, get_refusal_type
from .context import handle_edge_case
from .generator import generate_response
from .refusal import handle_advisory_query
from .cache import get_cache
from .utils import setup_logging

logger = setup_logging("pipeline")


def rag_pipeline(
    query: str,
    scheme: Optional[str] = None,
    top_k: int = TOP_K,
    similarity_threshold: float = SIMILARITY_THRESHOLD,
    use_cache: bool = True
) -> dict:
    """
    Main RAG pipeline: retrieve, classify, and generate response.
    
    Args:
        query: User query
        scheme: Optional scheme filter
        top_k: Number of chunks to retrieve
        similarity_threshold: Minimum similarity threshold
        use_cache: Whether to use cache
    
    Returns:
        Dictionary with response and metadata
    """
    logger.info(f"Processing query: {query[:50]}...")
    
    # Check cache first
    cache = get_cache()
    if use_cache:
        cached_result = cache.get(query, scheme)
        if cached_result:
            logger.info("Returning cached result")
            cached_result["cached"] = True
            return cached_result
    
    # Classify query
    query_type = classify_query(query)
    should_refuse_query, refusal_type = should_refuse(query)
    
    # Handle advisory queries with refusal
    if should_refuse_query:
        logger.info(f"Query refused as advisory (type: {refusal_type})")
        result = handle_advisory_query(query, refusal_type)
        
        # Cache the refusal
        if use_cache:
            cache.set(query, result, scheme)
        
        result["cached"] = False
        return result
    
    # Retrieve relevant chunks
    if scheme:
        chunks = retrieve_by_scheme(query, scheme, top_k)
    else:
        chunks = retrieve(query, top_k, similarity_threshold)
    
    logger.info(f"Retrieved {len(chunks)} chunks")
    
    # Handle edge cases (no context, low confidence)
    context, has_context = handle_edge_case(chunks, query, similarity_threshold)
    
    # Generate response
    if has_context:
        result = generate_response(query, context, chunks)
    else:
        result = generate_response(query, "", [])
    
    # Add metadata
    result["query_type"] = query_type
    result["chunks_retrieved"] = len(chunks)
    result["has_context"] = has_context
    
    # Cache the result
    if use_cache and result.get("success"):
        cache.set(query, result, scheme)
    
    result["cached"] = False
    return result


def get_available_schemes() -> list[str]:
    """
    Get list of available schemes from committed chunk files.
    
    Returns:
        List of scheme names
    """
    try:
        import json
        from pathlib import Path
        
        # Try multiple paths for chunks
        chunk_paths = [
            "data/chunks",
            "./data/chunks",
            "Docs/src/data/chunks",
            "./Docs/src/data/chunks",
            "/app/data/chunks",
            str(Path.cwd() / "data" / "chunks"),
        ]
        
        scheme_names = set()
        
        for chunk_path in chunk_paths:
            chunks_dir = Path(chunk_path)
            if chunks_dir.exists() and any(chunks_dir.iterdir()):
                for chunk_file in chunks_dir.glob("*_chunks.json"):
                    try:
                        with open(chunk_file, 'r', encoding='utf-8') as f:
                            chunks = json.load(f)
                            for chunk in chunks:
                                scheme_names.add(chunk['metadata']['scheme_name'])
                        logger.info(f"Loaded schemes from {chunk_file.name}")
                    except Exception as e:
                        logger.error(f"Error loading {chunk_file}: {e}")
                break
        
        if scheme_names:
            return sorted(list(scheme_names))
        else:
            # Fallback to hardcoded schemes if no chunks found
            logger.warning("No chunks found, using fallback schemes")
            return [
                "HDFC Mid-Cap Fund (Direct Growth)",
                "HDFC Equity Fund (Direct Growth)",
                "HDFC Focused Fund (Direct Growth)",
                "HDFC ELSS Tax Saver Fund (Direct Plan Growth)",
                "HDFC Large-Cap Fund (Direct Growth)"
            ]
    
    except Exception as e:
        logger.error(f"Error getting available schemes: {e}")
        # Always return fallback schemes
        return [
            "HDFC Mid-Cap Fund (Direct Growth)",
            "HDFC Equity Fund (Direct Growth)",
            "HDFC Focused Fund (Direct Growth)",
            "HDFC ELSS Tax Saver Fund (Direct Plan Growth)",
            "HDFC Large-Cap Fund (Direct Growth)"
        ]


def initialize_vector_store() -> None:
    """
    Auto-initialize the vector store from processed data if empty.
    Called on app startup to ensure ChromaDB is populated.
    """
    from phase1.vector_store import get_collection_stats, upsert_chunks
    from phase1.chunker import chunk_all_schemes
    from pathlib import Path
    import json
    import os
    import shutil

    logger.info("Checking vector store initialization...")

    try:
        # SCHEMA FIX: Delete existing ChromaDB to avoid schema incompatibility
        from phase1.config import CHROMA_PERSIST_DIR
        chroma_path = Path(CHROMA_PERSIST_DIR)
        
        # Check if we're on deployment (Streamlit Cloud)
        is_deployment = os.getenv("STREAMLIT_SERVER_PORT") or "/app" in os.getcwd()
        
        if is_deployment and chroma_path.exists():
            logger.warning("Deployment detected - deleting existing ChromaDB to avoid schema issues...")
            try:
                shutil.rmtree(chroma_path)
                logger.info(f"Deleted existing ChromaDB at: {chroma_path}")
            except Exception as e:
                logger.error(f"Failed to delete ChromaDB: {e}")
        
        # AGGRESSIVE FIX: Always try to rebuild from committed chunks on deployment
        # This bypasses all path detection issues
        logger.info("Attempting aggressive fix - rebuilding from committed chunks...")
        
        # Check if we have committed chunks
        chunk_paths_to_try = [
            "data/chunks",
            "./data/chunks",
            "Docs/src/data/chunks",
            "./Docs/src/data/chunks",
            "/app/data/chunks",
        ]
        
        chunks = []
        chunks_found = False
        
        for chunk_path in chunk_paths_to_try:
            chunks_dir = Path(chunk_path)
            if chunks_dir.exists() and any(chunks_dir.iterdir()):
                logger.info(f"Found chunks directory at: {chunk_path}")
                for chunk_file in chunks_dir.glob("*_chunks.json"):
                    try:
                        with open(chunk_file, 'r', encoding='utf-8') as f:
                            file_chunks = json.load(f)
                            chunks.extend(file_chunks)
                            logger.info(f"Loaded {len(file_chunks)} chunks from {chunk_file.name}")
                    except Exception as e:
                        logger.error(f"Error loading {chunk_file}: {e}")
                chunks_found = True
                break
        
        if not chunks_found:
            logger.error("No chunks directory found in any expected location!")
            logger.info(f"Current working directory: {os.getcwd()}")
            logger.info(f"Files in current directory: {list(Path('.').rglob('*')[:10])}")
            return
        
        if not chunks:
            logger.error("No chunks loaded from any directory!")
            return
        
        logger.info(f"Total chunks loaded: {len(chunks)}")
        
        # Force rebuild the vector store with these chunks
        # This will work regardless of path issues
        logger.info("Force rebuilding vector store with loaded chunks...")
        result = upsert_chunks(chunks)
        logger.info(f"Force rebuild result: {result}")
        
        # Verify the vector store now has data
        stats = get_collection_stats()
        total_vectors = stats.get("total_vectors", 0)
        logger.info(f"After force rebuild - Vector store stats: {stats}")
        
        if total_vectors > 0:
            logger.info(f"SUCCESS: Vector store initialized with {total_vectors} vectors")
        else:
            logger.error("FAILED: Vector store still empty after force rebuild!")
            
    except Exception as e:
        logger.error(f"Vector store initialization failed: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        logger.warning("Continuing without vector store - queries will return no results")
        # Don't fail the app startup, just log the error
        return


def get_cache_stats() -> dict:
    """Get cache statistics."""
    cache = get_cache()
    return cache.get_stats()


def clear_cache() -> bool:
    """Clear the query cache."""
    cache = get_cache()
    return cache.clear()


if __name__ == "__main__":
    # Test the pipeline
    test_queries = [
        "What is the expense ratio of HDFC Mid Cap Fund?",
        "What is the minimum SIP amount?",
        "Should I invest in HDFC Mid Cap Fund?",
        "Which fund is better for long term investment?"
    ]
    
    print("=" * 80)
    print("RAG Pipeline Test")
    print("=" * 80)
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        result = rag_pipeline(query, use_cache=True)
        
        print(f"Query Type: {result.get('query_type', 'unknown')}")
        print(f"Chunks Retrieved: {result.get('chunks_retrieved', 0)}")
        print(f"Has Context: {result.get('has_context', False)}")
        print(f"Cached: {result.get('cached', False)}")
        print(f"\nAnswer: {result.get('answer', 'No answer generated')}")
        print("-" * 80)
    
    # Display cache stats
    print("\nCache Stats:")
    stats = get_cache_stats()
    print(stats)
