"""
Context Assembly for Phase 2: RAG Pipeline
Manages prompt templates and context window management
"""

from typing import Optional
from .config import MAX_CONTEXT_TOKENS, SYSTEM_PROMPT, MAX_SENTENCES
from .utils import setup_logging, format_context, truncate_context, count_tokens

logger = setup_logging("context")


def assemble_context(
    query: str,
    chunks: list[dict],
    max_tokens: int = MAX_CONTEXT_TOKENS
) -> str:
    """
    Assemble context from retrieved chunks with proper formatting.
    
    Args:
        query: User query
        chunks: Retrieved chunks
        max_tokens: Maximum tokens for context
    
    Returns:
        Formatted context string
    """
    if not chunks:
        logger.warning("No chunks provided for context assembly")
        return ""
    
    # Format chunks into context
    formatted_context = format_context(chunks)
    
    # Truncate if needed
    if count_tokens(formatted_context) > max_tokens:
        logger.info(f"Context exceeds {max_tokens} tokens, truncating...")
        formatted_context = truncate_context(formatted_context, max_tokens)
    
    return formatted_context


def build_prompt(query: str, context: str) -> str:
    """
    Build the complete prompt for LLM with system prompt and context.
    
    Args:
        query: User query
        context: Retrieved context
    
    Returns:
        Complete prompt string
    """
    prompt = f"""{SYSTEM_PROMPT}

Context:
{context}

Question: {query}

Answer:"""
    
    return prompt


def build_prompt_no_context(query: str) -> str:
    """
    Build prompt when no relevant context is found.
    
    Args:
        query: User query
    
    Returns:
        Prompt string for no-context scenario
    """
    prompt = f"""{SYSTEM_PROMPT}

Context: No relevant information found in the available documents.

Question: {query}

Answer: I'm sorry, but I couldn't find relevant information about this in the available fund documents."""
    
    return prompt


def handle_edge_case(
    chunks: list[dict],
    query: str,
    similarity_threshold: float = 0.7
) -> tuple[str, bool]:
    """
    Handle edge cases in retrieval (no results, low confidence, etc.).
    
    Args:
        chunks: Retrieved chunks
        query: User query
        similarity_threshold: Minimum similarity threshold
    
    Returns:
        Tuple of (context, has_relevant_context)
    """
    if not chunks:
        logger.warning("No chunks retrieved - using no-context prompt")
        return "", False
    
    # Check if any chunks meet similarity threshold
    relevant_chunks = [c for c in chunks if c.get("similarity", 0) >= similarity_threshold]
    
    if not relevant_chunks:
        logger.warning(f"No chunks above similarity threshold {similarity_threshold}")
        return "", False
    
    # Use relevant chunks for context
    context = assemble_context(query, relevant_chunks)
    return context, True


def extract_answer_text(response: str, max_sentences: int = MAX_SENTENCES) -> str:
    """
    Extract and limit answer text to specified sentence count.
    
    Args:
        response: Full LLM response
        max_sentences: Maximum sentences to keep
    
    Returns:
        Limited answer text
    """
    if not response:
        return ""
    
    # Split into sentences
    sentences = []
    current_sentence = []
    
    for char in response:
        current_sentence.append(char)
        if char in '.!?':
            sentence = ''.join(current_sentence).strip()
            if sentence:
                sentences.append(sentence)
            current_sentence = []
    
    # Add any remaining text
    if current_sentence:
        sentence = ''.join(current_sentence).strip()
        if sentence:
            sentences.append(sentence)
    
    # Limit to max sentences
    if len(sentences) > max_sentences:
        sentences = sentences[:max_sentences]
        return '. '.join(sentences) + '.'
    
    return '. '.join(sentences)


def format_response_with_footer(
    answer: str,
    citations: list[dict],
    include_footer: bool = True
) -> str:
    """
    Format response with answer and footer containing citations.
    
    Args:
        answer: Answer text
        citations: List of citation dictionaries
        include_footer: Whether to include footer
    
    Returns:
        Formatted response string
    """
    if not include_footer or not citations:
        return answer
    
    # Get most recent date from citations
    last_updated = max([c["last_updated"] for c in citations])
    
    # Get unique source URLs
    source_urls = list(set([c["source_url"] for c in citations]))
    
    footer = f"\n\n---\nSource: {source_urls[0]}\nLast Updated: {last_updated}"
    
    return answer + footer


if __name__ == "__main__":
    # Test context assembly
    test_chunks = [
        {
            "text": "The expense ratio of HDFC Mid Cap Fund is 1.25%.",
            "metadata": {
                "scheme_name": "HDFC Mid-Cap Fund (Direct Growth)",
                "section": "Expense Ratio",
                "source_url": "https://groww.in/mutual-funds/hdfc-mid-cap-fund-direct-growth",
                "last_updated": "2026-05-07"
            },
            "similarity": 0.85
        }
    ]
    
    context = assemble_context("What is the expense ratio?", test_chunks)
    print("Context:")
    print(context)
