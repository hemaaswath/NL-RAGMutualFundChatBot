"""
Query Classification for Phase 2: RAG Pipeline
Classifies queries as factual or advisory/refusal
"""

from typing import Literal
import re
from .config import ADVISORY_KEYWORDS, FACTUAL_KEYWORDS
from .utils import setup_logging

logger = setup_logging("classifier")


def classify_query(query: str) -> Literal["factual", "advisory", "refusal"]:
    """
    Classify a query as factual, advisory, or refusal type.
    
    Args:
        query: User query string
    
    Returns:
        Query type: "factual", "advisory", or "refusal"
    """
    query_lower = query.lower().strip()
    
    # Check for advisory keywords
    advisory_score = 0
    for keyword in ADVISORY_KEYWORDS:
        if keyword in query_lower:
            advisory_score += 1
    
    # Check for factual keywords
    factual_score = 0
    for keyword in FACTUAL_KEYWORDS:
        if keyword in query_lower:
            factual_score += 1
    
    # Determine classification
    if advisory_score >= 1:
        logger.info(f"Query classified as ADVISORY: {query[:50]}...")
        return "advisory"
    elif factual_score >= 1:
        logger.info(f"Query classified as FACTUAL: {query[:50]}...")
        return "factual"
    else:
        # Default to factual if no clear indicators
        logger.info(f"Query classified as FACTUAL (default): {query[:50]}...")
        return "factual"


def get_refusal_type(query: str) -> Literal["investment_advice", "performance_comparison", "recommendation_request", "default"]:
    """
    Determine the specific type of refusal needed.
    
    Args:
        query: User query string
    
    Returns:
        Refusal type for template selection
    """
    query_lower = query.lower()
    
    # Performance comparison
    comparison_keywords = ["compare", "better", "vs", "versus", "which is better", "performance comparison"]
    if any(keyword in query_lower for keyword in comparison_keywords):
        return "performance_comparison"
    
    # Recommendation request
    recommendation_keywords = ["recommend", "suggest", "should i invest", "which fund should"]
    if any(keyword in query_lower for keyword in recommendation_keywords):
        return "recommendation_request"
    
    # Investment advice (general)
    advice_keywords = ["advice", "investment advice", "financial advice", "guidance"]
    if any(keyword in query_lower for keyword in advice_keywords):
        return "investment_advice"
    
    return "default"


def should_refuse(query: str) -> tuple[bool, str]:
    """
    Determine if a query should be refused and the refusal type.
    
    Args:
        query: User query string
    
    Returns:
        Tuple of (should_refuse: bool, refusal_type: str)
    """
    query_type = classify_query(query)
    
    if query_type == "advisory":
        refusal_type = get_refusal_type(query)
        return True, refusal_type
    
    return False, ""


if __name__ == "__main__":
    # Test classification
    test_queries = [
        "What is the expense ratio of HDFC Mid Cap Fund?",
        "Should I invest in HDFC Mid Cap Fund?",
        "Which fund is better for long term?",
        "What is the minimum SIP amount?",
        "Can you recommend a good mid cap fund?"
    ]
    
    for query in test_queries:
        query_type = classify_query(query)
        should_ref, refusal_type = should_refuse(query)
        print(f"Query: {query}")
        print(f"Type: {query_type}")
        print(f"Should refuse: {should_ref}")
        if should_ref:
            print(f"Refusal type: {refusal_type}")
        print()
