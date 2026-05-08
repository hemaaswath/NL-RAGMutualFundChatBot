"""
Script to view embeddings stored in ChromaDB.
"""
from Docs.src.phase1.vector_store import get_client, get_or_create_collection

# Get client and collection
client = get_client()
collection = get_or_create_collection(client)

# Retrieve all embeddings
results = collection.get(include=['embeddings', 'metadatas', 'documents'])

print(f"Total vectors in database: {len(results['embeddings'])}")
print(f"Embedding dimension: {len(results['embeddings'][0])}")
print()

# Show first few chunks
for i in range(min(3, len(results['embeddings']))):
    print(f"--- Chunk {i+1} ---")
    print(f"Scheme: {results['metadatas'][i]['scheme_name']}")
    print(f"Section: {results['metadatas'][i]['section']}")
    print(f"Embedding (first 10 values): {results['embeddings'][i][:10]}")
    print(f"Document (first 200 chars): {results['documents'][i][:200]}...")
    print()
