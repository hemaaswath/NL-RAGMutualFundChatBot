"""
Document chunker for Phase 1.

Splits processed text into semantically coherent chunks with metadata,
using tiktoken for token counting and respecting section boundaries.
"""

import re
import json
from pathlib import Path
import tiktoken

from .config import (
    CHUNK_OVERLAP, CHUNK_SIZE, DATA_CHUNKS_DIR, DATA_PROCESSED_DIR,
    SCHEMES, TOKENIZER_MODEL,
)
from .utils import (
    ensure_directory, get_today_iso, load_json, load_text,
    save_json, setup_logging,
)

logger = setup_logging("chunker")

_encoder = tiktoken.get_encoding(TOKENIZER_MODEL)


def count_tokens(text: str) -> int:
    return len(_encoder.encode(text))


def split_into_sentences(text: str) -> list[str]:
    """Split text into sentences using regex."""
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]


def create_chunks(text: str, chunk_size: int = CHUNK_SIZE,
                  chunk_overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Split text into token-bounded chunks with overlap, respecting sentence boundaries."""
    sentences = split_into_sentences(text)
    if not sentences:
        return [text] if text.strip() else []

    chunks = []
    current_chunk = []
    current_tokens = 0

    for sentence in sentences:
        sent_tokens = count_tokens(sentence)
        if sent_tokens > chunk_size:
            if current_chunk:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
                current_tokens = 0
            # Split long sentence by words
            words = sentence.split()
            word_chunk = []
            word_tokens = 0
            for word in words:
                wt = count_tokens(word + " ")
                if word_tokens + wt > chunk_size and word_chunk:
                    chunks.append(" ".join(word_chunk))
                    overlap_text = " ".join(word_chunk)
                    overlap_sents = split_into_sentences(overlap_text)
                    word_chunk = overlap_sents[-2:] if len(overlap_sents) > 2 else []
                    word_tokens = count_tokens(" ".join(word_chunk))
                word_chunk.append(word)
                word_tokens += wt
            if word_chunk:
                current_chunk = word_chunk
                current_tokens = word_tokens
            continue

        if current_tokens + sent_tokens > chunk_size and current_chunk:
            chunks.append(" ".join(current_chunk))
            # Overlap: keep last few sentences
            overlap_tokens = 0
            overlap_start = len(current_chunk)
            for j in range(len(current_chunk) - 1, -1, -1):
                t = count_tokens(current_chunk[j])
                if overlap_tokens + t > chunk_overlap:
                    break
                overlap_tokens += t
                overlap_start = j
            current_chunk = current_chunk[overlap_start:]
            current_tokens = sum(count_tokens(s) for s in current_chunk)

        current_chunk.append(sentence)
        current_tokens += sent_tokens

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def chunk_scheme(scheme: dict) -> list[dict]:
    """Chunk a single scheme's processed text and attach metadata."""
    text_path = DATA_PROCESSED_DIR / f"{scheme['slug']}.txt"
    json_path = DATA_PROCESSED_DIR / f"{scheme['slug']}.json"

    if not text_path.exists():
        logger.warning(f"[yellow]Processed text not found: {text_path}[/]")
        return []

    full_text = load_text(text_path)
    sections_data = []
    if json_path.exists():
        meta = load_json(json_path)
        sections_data = meta.get("sections", [])

    # Chunk by sections first, then within sections
    all_chunks = []
    if sections_data:
        for sec in sections_data:
            sec_chunks = create_chunks(sec["content"])
            for chunk_text in sec_chunks:
                all_chunks.append({"text": chunk_text, "section": sec["section"]})
    else:
        raw_chunks = create_chunks(full_text)
        for chunk_text in raw_chunks:
            all_chunks.append({"text": chunk_text, "section": "General"})

    # Add context header and metadata
    today = get_today_iso()
    total = len(all_chunks)
    result = []
    for idx, chunk in enumerate(all_chunks):
        context_header = (
            f"Scheme: {scheme['name']} | Category: {scheme['category']} "
            f"| Source: {scheme['url']}"
        )
        full_chunk_text = f"{context_header}\n\n{chunk['text']}"
        result.append({
            "chunk_id": f"{scheme['slug']}_chunk_{idx:03d}",
            "text": full_chunk_text,
            "metadata": {
                "scheme_name": scheme["name"],
                "scheme_slug": scheme["slug"],
                "source_url": scheme["url"],
                "document_type": scheme.get("document_type", "scheme_page"),
                "category": scheme["category"],
                "section": chunk["section"],
                "last_updated": today,
                "chunk_index": idx,
                "total_chunks": total,
                "token_count": count_tokens(full_chunk_text),
            },
        })
    return result


def chunk_all_schemes(schemes: list[dict] | None = None) -> list[dict]:
    """Chunk all schemes and save to data/chunks/."""
    if schemes is None:
        schemes = SCHEMES
    ensure_directory(DATA_CHUNKS_DIR)
    all_results = []
    for i, scheme in enumerate(schemes):
        logger.info(f"\n[bold cyan]── Chunking {i+1}/{len(schemes)}: {scheme['name']} ──[/]")
        chunks = chunk_scheme(scheme)
        if chunks:
            save_json(chunks, DATA_CHUNKS_DIR / f"{scheme['slug']}_chunks.json")
            tokens = [c["metadata"]["token_count"] for c in chunks]
            logger.info(f"  [green]✓ {len(chunks)} chunks[/] (tokens: min={min(tokens)}, max={max(tokens)}, avg={sum(tokens)//len(tokens)})")
        else:
            logger.warning(f"  [yellow]No chunks generated[/]")
        all_results.extend(chunks)
    logger.info(f"\n[bold green]Total chunks: {len(all_results)}[/]")
    return all_results


if __name__ == "__main__":
    chunk_all_schemes()
