"""
Refusal Handling for Phase 2: RAG Pipeline
Manages refusal responses for advisory queries
"""

from .config import REFUSAL_TEMPLATES
from .utils import setup_logging

logger = setup_logging("refusal")


def get_refusal_message(refusal_type: str) -> str:
    """
    Get refusal message for a specific refusal type.
    
    Args:
        refusal_type: Type of refusal (investment_advice, performance_comparison, etc.)
    
    Returns:
        Refusal message string
    """
    return REFUSAL_TEMPLATES.get(refusal_type, REFUSAL_TEMPLATES.get("default"))


def handle_advisory_query(query: str, refusal_type: str) -> dict:
    """
    Handle advisory queries with appropriate refusal message.
    
    Args:
        query: User query
        refusal_type: Type of refusal
    
    Returns:
        Dictionary with refusal response
    """
    logger.info(f"Handling advisory query with refusal type: {refusal_type}")
    
    refusal_message = get_refusal_message(refusal_type)
    
    return {
        "answer": refusal_message,
        "citations": [],
        "query_type": "advisory",
        "refusal_type": refusal_type,
        "success": True,
        "chunks_retrieved": 0,
        "cached": False
    }


def add_educational_resources(refusal_message: str) -> str:
    """
    Add educational resource links to refusal message.
    
    Args:
        refusal_message: Base refusal message
    
    Returns:
        Refusal message with educational resources
    """
    # Educational resources are already included in the templates
    return refusal_message


if __name__ == "__main__":
    # Test refusal handling
    test_cases = [
        ("investment_advice", "Should I invest in HDFC Mid Cap Fund?"),
        ("performance_comparison", "Which fund is better - HDFC Mid Cap or HDFC Large Cap?"),
        ("recommendation_request", "Can you recommend a good mutual fund?")
    ]
    
    for refusal_type, query in test_cases:
        result = handle_advisory_query(query, refusal_type)
        print(f"\nQuery: {query}")
        print(f"Refusal Type: {refusal_type}")
        print(f"Response: {result['answer']}")
