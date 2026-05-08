"""
Interactive CLI for Phase 2 RAG Pipeline
Allows users to test queries interactively
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from phase2.pipeline import rag_pipeline, get_available_schemes


def main():
    """Interactive CLI for testing the RAG pipeline."""
    print("=" * 80)
    print("RAG Mutual Fund FAQ Assistant - Interactive Mode")
    print("=" * 80)
    print("\nAvailable Schemes:")
    schemes = get_available_schemes()
    for i, scheme in enumerate(schemes, 1):
        print(f"  {i}. {scheme}")
    
    print("\nCommands:")
    print("  - Type your question to get an answer")
    print("  - Type 'schemes' to see available schemes")
    print("  - Type 'quit' or 'exit' to exit")
    print("=" * 80)
    
    while True:
        try:
            query = input("\nYour question: ").strip()
            
            if not query:
                continue
            
            if query.lower() in ['quit', 'exit']:
                print("\nGoodbye!")
                break
            
            if query.lower() == 'schemes':
                print("\nAvailable Schemes:")
                for scheme in schemes:
                    print(f"  - {scheme}")
                continue
            
            print("\nProcessing query...")
            result = rag_pipeline(query, use_cache=True)
            
            print(f"\nQuery Type: {result.get('query_type', 'unknown')}")
            print(f"Chunks Retrieved: {result.get('chunks_retrieved', 0)}")
            print(f"Cached: {result.get('cached', False)}")
            
            if result.get('refusal_type'):
                print(f"Refusal Type: {result['refusal_type']}")
            
            print(f"\nAnswer:\n{result['answer']}")
            
            if result.get('citations') and len(result['citations']) > 0:
                print(f"\nSource: {result['citations'][0]['source_url']}")
                print(f"Last Updated: {result['citations'][0]['last_updated']}")
            
            print("-" * 80)
        
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")


if __name__ == "__main__":
    main()
