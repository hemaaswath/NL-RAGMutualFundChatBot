"""
Embedding generation for Phase 1.

Uses sentence-transformers (local model) to generate embeddings for document chunks.
No API key required - runs locally.
"""

from sentence_transformers import SentenceTransformer

from .config import EMBEDDING_MODEL
from .utils import setup_logging

logger = setup_logging("embeddings")

# Load model once (singleton pattern)
_model_cache = None


def get_model():
    """Get the sentence-transformers model (cached)."""
    global _model_cache
    if _model_cache is None:
        logger.info(f"Loading embedding model: {EMBEDDING_MODEL}")
        _model_cache = SentenceTransformer(EMBEDDING_MODEL)
        logger.info(f"Model loaded successfully")
    return _model_cache


def generate_embeddings(
    texts: list[str],
    model: str = EMBEDDING_MODEL,
    batch_size: int = 50,
) -> list[list[float]]:
    """
    Generate embeddings for a list of texts using sentence-transformers.
    Processes in batches.
    """
    model = get_model()
    all_embeddings = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        batch_num = (i // batch_size) + 1
        total_batches = (len(texts) + batch_size - 1) // batch_size
        logger.info(f"  Embedding batch {batch_num}/{total_batches} ({len(batch)} texts)")

        batch_embeddings = model.encode(batch, convert_to_numpy=True)
        all_embeddings.extend(batch_embeddings.tolist())

    return all_embeddings


def generate_single_embedding(text: str) -> list[float] | None:
    """Generate embedding for a single text."""
    model = get_model()
    embedding = model.encode([text], convert_to_numpy=True)
    return embedding[0].tolist()
