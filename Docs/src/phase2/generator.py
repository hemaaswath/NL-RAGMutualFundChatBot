"""
Response Generation for Phase 2: RAG Pipeline
Implements LLM integration with Groq
"""

from typing import Optional
from openai import OpenAI
from .config import GROQ_API_KEY, GROQ_API_URL, LLM_MODEL, MAX_SENTENCES, INCLUDE_CITATIONS, INCLUDE_FOOTER
from .context import build_prompt, build_prompt_no_context, extract_answer_text, format_response_with_footer
from .utils import setup_logging, extract_citations

logger = setup_logging("generator")


def get_llm_client() -> OpenAI:
    """Get Groq client (OpenAI-compatible)."""
    if not GROQ_API_KEY or GROQ_API_KEY == "your_groq_api_key_here":
        raise ValueError("GROQ_API_KEY not set. Please set it in .env file.")
    
    return OpenAI(
        api_key=GROQ_API_KEY,
        base_url=GROQ_API_URL
    )


def generate_response(
    query: str,
    context: str,
    chunks: Optional[list[dict]] = None,
    max_retries: int = 3
) -> dict:
    """
    Generate response using LLM with provided context.
    
    Args:
        query: User query
        context: Retrieved context
        chunks: Retrieved chunks (for citations)
        max_retries: Maximum retry attempts
    
    Returns:
        Dictionary with answer, citations, and metadata
    """
    try:
        client = get_llm_client()
        
        # Build prompt
        if context:
            prompt = build_prompt(query, context)
        else:
            prompt = build_prompt_no_context(query)
        
        logger.info(f"Generating response for query: {query[:50]}...")
        
        # Call LLM
        for attempt in range(1, max_retries + 1):
            try:
                response = client.chat.completions.create(
                    model=LLM_MODEL,
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.1,  # Low temperature for factual responses
                    max_tokens=300
                )
                
                answer = response.choices[0].message.content.strip()
                
                # Limit to max sentences
                answer = extract_answer_text(answer, MAX_SENTENCES)
                
                # Extract citations if chunks provided
                citations = []
                if chunks and INCLUDE_CITATIONS:
                    citations = extract_citations(chunks)
                
                # Format with footer if enabled
                if INCLUDE_FOOTER and citations:
                    answer = format_response_with_footer(answer, citations)
                
                logger.info("Response generated successfully")
                
                return {
                    "answer": answer,
                    "citations": citations,
                    "model": LLM_MODEL,
                    "success": True
                }
            
            except Exception as e:
                logger.error(f"Attempt {attempt}/{max_retries} failed: {e}")
                if attempt < max_retries:
                    continue
                else:
                    raise
        
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        
        return {
            "answer": "I apologize, but I encountered an error generating the response. Please try again.",
            "citations": [],
            "model": LLM_MODEL,
            "success": False,
            "error": str(e)
        }


def generate_refusal_response(refusal_type: str, refusal_templates: dict) -> dict:
    """
    Generate refusal response for advisory queries.
    
    Args:
        refusal_type: Type of refusal (investment_advice, performance_comparison, etc.)
        refusal_templates: Dictionary of refusal templates
    
    Returns:
        Dictionary with refusal message
    """
    refusal_message = refusal_templates.get(refusal_type, refusal_templates.get("default"))
    
    return {
        "answer": refusal_message,
        "citations": [],
        "model": None,
        "success": True,
        "query_type": "advisory",
        "refusal_type": refusal_type
    }


if __name__ == "__main__":
    # Test response generation
    test_query = "What is the expense ratio of HDFC Mid Cap Fund?"
    test_context = """
[Source 1]
Scheme: HDFC Mid-Cap Fund (Direct Growth)
Section: Expense Ratio
Source URL: https://groww.in/mutual-funds/hdfc-mid-cap-fund-direct-growth
Last Updated: 2026-05-07

The expense ratio of HDFC Mid Cap Fund is 1.25%.
"""
    
    result = generate_response(test_query, test_context)
    print("\nQuery:", test_query)
    print("\nAnswer:", result["answer"])
    print("\nSuccess:", result["success"])
