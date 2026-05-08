"""
Utility functions for Phase 2: RAG Pipeline
"""

import sys
from pathlib import Path
from rich.console import Console
from rich.logging import RichHandler
import logging

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from .config import LOG_LEVEL


def setup_logging(name: str) -> logging.Logger:
    """Set up logging with rich formatting."""
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOG_LEVEL.upper()))
    
    if not logger.handlers:
        console = Console()
        handler = RichHandler(console=console, rich_tracebacks=True)
        handler.setFormatter(logging.Formatter("%(message)s", datefmt="[%X]"))
        logger.addHandler(handler)
    
    return logger


def format_context(chunks: list[dict]) -> str:
    """
    Format retrieved chunks into context string for LLM.
    
    Args:
        chunks: List of retrieved chunks with metadata
    
    Returns:
        Formatted context string
    """
    context_parts = []
    
    for i, chunk in enumerate(chunks):
        metadata = chunk["metadata"]
        text = chunk["text"]
        
        context_part = f"""
[Source {i+1}]
Scheme: {metadata['scheme_name']}
Section: {metadata['section']}
Source URL: {metadata['source_url']}
Last Updated: {metadata['last_updated']}

{text}
"""
        context_parts.append(context_part)
    
    return "\n".join(context_parts)


def extract_citations(chunks: list[dict]) -> list[dict]:
    """
    Extract citation information from retrieved chunks.
    
    Args:
        chunks: List of retrieved chunks
    
    Returns:
        List of citation dictionaries
    """
    citations = []
    
    for chunk in chunks:
        metadata = chunk["metadata"]
        citations.append({
            "scheme_name": metadata["scheme_name"],
            "source_url": metadata["source_url"],
            "last_updated": metadata["last_updated"],
            "section": metadata["section"]
        })
    
    return citations


def count_tokens(text: str) -> int:
    """Count tokens in text using tiktoken."""
    try:
        import tiktoken
        encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(text))
    except ImportError:
        # Fallback to character count
        return len(text) // 4


def truncate_context(context: str, max_tokens: int = 2000) -> str:
    """
    Truncate context to fit within token limit.
    
    Args:
        context: Context string
        max_tokens: Maximum tokens allowed
    
    Returns:
        Truncated context string
    """
    current_tokens = count_tokens(context)
    
    if current_tokens <= max_tokens:
        return context
    
    # Simple truncation by character count
    max_chars = int((max_tokens / current_tokens) * len(context))
    return context[:max_chars] + "\n\n[Context truncated due to length limit]"
