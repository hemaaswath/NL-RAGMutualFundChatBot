"""
Embedding generation for Phase 1.

Uses OpenAI text-embedding-3-small to generate embeddings for document chunks.
Implements batch processing and retry logic.
"""

import time
from openai import OpenAI

from src.phase1.config import EMBEDDING_DIMENSIONS, EMBEDDING_MODEL, OPENAI_API_KEY
from src.phase1.utils import setup_logging

logger = setup_logging("embeddings")


def get_client() -> OpenAI:
    """Get OpenAI client."""
    if not OPENAI_API_KEY or OPENAI_API_KEY == "your_openai_api_key_here":
        raise ValueError(
            "OPENAI_API_KEY not set. Copy .env.example to .env and add your key."
        )
    return OpenAI(api_key=OPENAI_API_KEY)


def generate_embeddings(
    texts: list[str],
    model: str = EMBEDDING_MODEL,
    batch_size: int = 50,
    max_retries: int = 3,
) -> list[list[float]]:
    """
    Generate embeddings for a list of texts using OpenAI API.
    Processes in batches with retry logic.
    """
    client = get_client()
    all_embeddings = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        batch_num = (i // batch_size) + 1
        total_batches = (len(texts) + batch_size - 1) // batch_size
        logger.info(f"  Embedding batch {batch_num}/{total_batches} ({len(batch)} texts)")

        for attempt in range(1, max_retries + 1):
            try:
                response = client.embeddings.create(
                    input=batch,
                    model=model,
                    dimensions=EMBEDDING_DIMENSIONS,
                )
                batch_embeddings = [item.embedding for item in response.data]
                all_embeddings.extend(batch_embeddings)
                break
            except Exception as e:
                logger.error(f"  [red]Attempt {attempt}/{max_retries} failed:[/] {e}")
                if attempt < max_retries:
                    wait = 2 ** attempt
                    logger.info(f"  Retrying in {wait}s...")
                    time.sleep(wait)
                else:
                    logger.error(f"  [red]All retries exhausted for batch {batch_num}[/]")
                    # Fill with None for failed embeddings
                    all_embeddings.extend([None] * len(batch))

    return all_embeddings


def generate_single_embedding(text: str) -> list[float] | None:
    """Generate embedding for a single text."""
    results = generate_embeddings([text])
    return results[0] if results else None
