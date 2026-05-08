"""
Test cases for Phase 2 Query Classifier
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "Docs" / "src"))

from phase2.classifier import classify_query, should_refuse, get_refusal_type


class TestQueryClassification:
    """Test query classification logic."""
    
    def test_factual_query_classification(self):
        """Test that factual queries are classified correctly."""
        factual_queries = [
            "What is the expense ratio?",
            "How much is the minimum SIP?",
            "What is the NAV?",
            "What is the exit load?",
            "Who is the fund manager?"
        ]
        
        for query in factual_queries:
            query_type = classify_query(query)
            assert query_type == "factual", f"Query should be factual: {query}"
    
    def test_advisory_query_classification(self):
        """Test that advisory queries are classified correctly."""
        advisory_queries = [
            "Should I invest in this fund?",
            "Which fund is better?",
            "Can you recommend a fund?",
            "What should I buy?",
            "Is this a good investment?"
        ]
        
        for query in advisory_queries:
            query_type = classify_query(query)
            assert query_type == "advisory", f"Query should be advisory: {query}"
    
    def test_should_refuse_true(self):
        """Test that advisory queries should be refused."""
        advisory_queries = [
            "Should I invest?",
            "Which is better?",
            "Recommend a fund"
        ]
        
        for query in advisory_queries:
            should_refuse_query, _ = should_refuse(query)
            assert should_refuse_query, f"Should refuse: {query}"
    
    def test_should_refuse_false(self):
        """Test that factual queries should not be refused."""
        factual_queries = [
            "What is the expense ratio?",
            "What is the NAV?",
            "Minimum SIP amount"
        ]
        
        for query in factual_queries:
            should_refuse_query, _ = should_refuse(query)
            assert not should_refuse_query, f"Should not refuse: {query}"
    
    def test_refusal_type_investment_advice(self):
        """Test investment advice refusal type detection."""
        query = "Should I invest in HDFC Mid Cap Fund?"
        refusal_type = get_refusal_type(query)
        assert refusal_type in ["investment_advice", "recommendation_request"]
    
    def test_refusal_type_performance_comparison(self):
        """Test performance comparison refusal type detection."""
        query = "Which fund is better - HDFC Mid Cap or HDFC Large Cap?"
        refusal_type = get_refusal_type(query)
        assert refusal_type == "performance_comparison"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
