"""
Simple script to test the chatbot from command line
"""

import sys
from pathlib import Path

# Add Docs/src to Python path
sys.path.insert(0, str(Path(__file__).parent / "Docs" / "src"))

from phase2.pipeline import rag_pipeline

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_chatbot.py \"Your question here\"")
        print("Example: python test_chatbot.py \"What is the expense ratio?\"")
        sys.exit(1)
    
    query = " ".join(sys.argv[1:])
    print(f"\nQuery: {query}")
    print("-" * 80)
    
    result = rag_pipeline(query, use_cache=True)
    
    print(f"Query Type: {result.get('query_type', 'unknown')}")
    print(f"Chunks Retrieved: {result.get('chunks_retrieved', 0)}")
    print(f"Cached: {result.get('cached', False)}")
    
    if result.get('refusal_type'):
        print(f"Refusal Type: {result['refusal_type']}")
    
    print(f"\nAnswer: {result.get('answer', 'No answer generated')}")
    
    if result.get('citations') and len(result['citations']) > 0:
        print(f"\nSource: {result['citations'][0]['source_url']}")
        print(f"Last Updated: {result['citations'][0]['last_updated']}")
    
    print("-" * 80)
