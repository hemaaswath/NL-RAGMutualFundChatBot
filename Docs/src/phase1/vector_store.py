"""
Vector store management for ChromaDB.
"""

import os
from .config import CHROMA_PERSIST_DIR, CHROMA_COLLECTION_NAME

# Completely disable ChromaDB telemetry
os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["CHROMA_TELEMETRY"] = "False"
os.environ["CHROMA_SERVER_HOST"] = "localhost"
os.environ["CHROMA_SERVER_HTTP_PORT"] = "8000"

import chromadb

from .embeddings import generate_embeddings
from .utils import setup_logging

logger = setup_logging("vector_store")


def get_client() -> chromadb.PersistentClient:
    """Get ChromaDB persistent client."""
    import os
    from pathlib import Path
    
    # Ensure the directory exists
    chroma_path = Path(CHROMA_PERSIST_DIR)
    chroma_path.mkdir(parents=True, exist_ok=True)
    
    # Create client (ChromaDB 0.4.x compatible)
    return chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)


def get_or_create_collection(client: chromadb.PersistentClient = None):
    """Get or create the mutual fund FAQ collection."""
    if client is None:
        client = get_client()
    collection = client.get_or_create_collection(
        name=CHROMA_COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )
    return collection


def upsert_chunks(chunks: list[dict], batch_size: int = 50) -> dict:
    """
    Generate embeddings and upsert chunks into ChromaDB.
    Returns stats dict with counts.
    """
    if not chunks:
        logger.warning("[yellow]No chunks to upsert[/]")
        return {"total": 0, "success": 0, "failed": 0}

    collection = get_or_create_collection()
    texts = [c["text"] for c in chunks]
    ids = [c["chunk_id"] for c in chunks]
    metadatas = []
    for c in chunks:
        meta = dict(c["metadata"])
        # ChromaDB metadata values must be str, int, float, or bool
        for k, v in meta.items():
            if v is None:
                meta[k] = ""
            elif isinstance(v, list):
                meta[k] = str(v)
        metadatas.append(meta)

    logger.info(f"[bold]Generating embeddings for {len(texts)} chunks...[/]")
    embeddings = generate_embeddings(texts)

    success = 0
    failed = 0
    for i in range(0, len(chunks), batch_size):
        batch_ids = ids[i:i+batch_size]
        batch_texts = texts[i:i+batch_size]
        batch_meta = metadatas[i:i+batch_size]
        batch_emb = embeddings[i:i+batch_size]

        # Filter out failed embeddings
        valid = [(id_, doc, meta, emb) for id_, doc, meta, emb
                 in zip(batch_ids, batch_texts, batch_meta, batch_emb)
                 if emb is not None]
        if not valid:
            failed += len(batch_ids)
            continue

        v_ids, v_docs, v_meta, v_emb = zip(*valid)
        try:
            collection.upsert(
                ids=list(v_ids),
                documents=list(v_docs),
                metadatas=list(v_meta),
                embeddings=list(v_emb),
            )
            success += len(v_ids)
            failed += len(batch_ids) - len(v_ids)
        except Exception as e:
            logger.error(f"[red]Upsert error:[/] {e}")
            failed += len(batch_ids)

    logger.info(f"[green]✓ Upserted {success} chunks[/] ({failed} failed)")
    return {"total": len(chunks), "success": success, "failed": failed}


def get_collection_stats() -> dict:
    """Return stats about the ChromaDB collection."""
    try:
        collection = get_or_create_collection()
        count = collection.count()
        return {"collection": CHROMA_COLLECTION_NAME, "total_vectors": count}
    except Exception as e:
        return {"error": str(e)}


def query_similar(query_text: str, n_results: int = 5, where: dict = None) -> dict:
    """Query the vector store for similar chunks (for testing)."""
    from .embeddings import generate_single_embedding
    collection = get_or_create_collection()
    embedding = generate_single_embedding(query_text)
    if embedding is None:
        return {"error": "Failed to generate query embedding"}
    kwargs = {"query_embeddings": [embedding], "n_results": n_results,
              "include": ["documents", "metadatas", "distances"]}
    if where:
        kwargs["where"] = where
    results = collection.query(**kwargs)
    return results


if __name__ == "__main__":
    stats = get_collection_stats()
    logger.info(f"Collection stats: {stats}")
