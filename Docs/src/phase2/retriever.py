"""
Retrieval Mechanism for Phase 2: RAG Pipeline
Implements semantic search with metadata filtering
"""

from typing import Optional
from phase1.vector_store import get_client, get_or_create_collection
from phase1.embeddings import generate_single_embedding
from .config import TOP_K, SIMILARITY_THRESHOLD, CHROMA_COLLECTION_NAME
from .utils import setup_logging

logger = setup_logging("retriever")


def retrieve(
    query: str,
    top_k: int = TOP_K,
    similarity_threshold: float = SIMILARITY_THRESHOLD,
    where: Optional[dict] = None,
    scheme: Optional[str] = None,
) -> list[dict]:
    """
    Retrieve relevant chunks from vector database using semantic search.
    
    Args:
        query: User query text
        top_k: Number of results to retrieve
        similarity_threshold: Minimum similarity score (0-1)
        where: Additional metadata filters
        scheme: Filter by specific scheme name
    
    Returns:
        List of retrieved chunks with metadata and scores
    """
    try:
        # Generate embedding for query
        logger.info(f"Generating embedding for query: {query[:50]}...")
        embedding = generate_single_embedding(query)
        
        if embedding is None:
            logger.error("Failed to generate query embedding")
            return []
        
        # Get collection
        client = get_client()
        collection = get_or_create_collection(client)
        
        # Build metadata filters
        filters = {}
        if scheme:
            filters["scheme_name"] = scheme
        if where:
            filters.update(where)
        
        # Query vector database
        logger.info(f"Querying vector database (top_k={top_k})...")
        kwargs = {
            "query_embeddings": [embedding],
            "n_results": top_k,
            "include": ["documents", "metadatas", "distances"]
        }
        
        if filters:
            kwargs["where"] = filters
        
        results = collection.query(**kwargs)
        
        # Process results
        retrieved = []
        if results["documents"] and len(results["documents"]) > 0:
            for i in range(len(results["documents"][0])):
                # Convert distance to similarity score (1 - distance for cosine)
                distance = results["distances"][0][i]
                similarity = 1 - distance
                
                # Filter by similarity threshold
                if similarity >= similarity_threshold:
                    retrieved.append({
                        "text": results["documents"][0][i],
                        "metadata": results["metadatas"][0][i],
                        "similarity": similarity,
                        "distance": distance
                    })
        
        logger.info(f"Retrieved {len(retrieved)} chunks (above threshold {similarity_threshold})")
        return retrieved
    
    except Exception as e:
        logger.error(f"Error during retrieval: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return []


def retrieve_by_scheme(query: str, scheme: str, top_k: int = TOP_K) -> list[dict]:
    """
    Retrieve chunks for a specific scheme.
    
    Args:
        query: User query text
        scheme: Scheme name to filter by
        top_k: Number of results to retrieve
    
    Returns:
        List of retrieved chunks
    """
    return retrieve(query, top_k=top_k, scheme=scheme)


def retrieve_by_category(query: str, category: str, top_k: int = TOP_K) -> list[dict]:
    """
    Retrieve chunks for a specific category (e.g., Mid Cap, Large Cap).
    
    Args:
        query: User query text
        category: Category to filter by
        top_k: Number of results to retrieve
    
    Returns:
        List of retrieved chunks
    """
    return retrieve(query, top_k=top_k, where={"category": category})


def retrieve_with_reranking(query: str, top_k: int = TOP_K, rerank_top: int = 10) -> list[dict]:
    """
    Retrieve chunks with re-ranking (simple implementation).
    
    Args:
        query: User query text
        top_k: Final number of results to return
        rerank_top: Number of results to retrieve for re-ranking
    
    Returns:
        List of re-ranked retrieved chunks
    """
    # Retrieve more results first
    retrieved = retrieve(query, top_k=rerank_top)
    
    if not retrieved:
        return []
    
    # Simple re-rank based on keyword matching in addition to semantic similarity
    query_words = set(query.lower().split())
    
    for chunk in retrieved:
        text_lower = chunk["text"].lower()
        # Count how many query words appear in the chunk
        word_matches = sum(1 for word in query_words if word in text_lower)
        # Boost score based on word matches
        chunk["rerank_score"] = chunk["similarity"] + (word_matches * 0.05)
    
    # Sort by re-rank score
    retrieved.sort(key=lambda x: x["rerank_score"], reverse=True)
    
    # Return top-k
    return retrieved[:top_k]


if __name__ == "__main__":
    # Test retrieval
    test_query = "What is the expense ratio of HDFC Mid Cap Fund?"
    results = retrieve(test_query)
    
    print(f"\nQuery: {test_query}")
    print(f"Retrieved {len(results)} chunks\n")
    
    for i, result in enumerate(results):
        print(f"--- Result {i+1} ---")
        print(f"Similarity: {result['similarity']:.3f}")
        print(f"Scheme: {result['metadata']['scheme_name']}")
        print(f"Section: {result['metadata']['section']}")
        print(f"Text: {result['text'][:200]}...")
        print()
