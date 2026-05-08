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
    Get list of available schemes from the vector database.
    
    Returns:
        List of scheme names
    """
    from phase1.vector_store import get_client, get_or_create_collection
    
    try:
        client = get_client()
        collection = get_or_create_collection(client)
        
        results = collection.get(include=["metadatas"])
        scheme_names = set()
        
        for metadata in results["metadatas"]:
            scheme_names.add(metadata["scheme_name"])
        
        return sorted(list(scheme_names))
    
    except Exception as e:
        logger.error(f"Error getting available schemes: {e}")
        return []


def initialize_vector_store() -> None:
    """
    Auto-initialize the vector store from processed data if empty.
    Called on app startup to ensure ChromaDB is populated.
    """
    from phase1.vector_store import get_collection_stats, upsert_chunks
    from phase1.chunker import chunk_all_schemes

    logger.info("Checking vector store initialization...")

    stats = get_collection_stats()
    total_vectors = stats.get("total_vectors", 0)

    if total_vectors > 0:
        logger.info(f"Vector store already initialized ({total_vectors} vectors)")
        return

    logger.warning("Vector store is empty. Building from processed data...")

    chunks = chunk_all_schemes()
    if not chunks:
        logger.error("No chunks generated from processed data")
        return

    result = upsert_chunks(chunks)
    logger.info(f"Vector store initialized: {result['success']} chunks indexed")


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
