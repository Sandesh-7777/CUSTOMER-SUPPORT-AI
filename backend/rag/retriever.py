# rag/retriever.py
# Searches the ChromaDB vector store for chunks relevant to a query
# Used by main.py every time a user sends a message
import os
import chromadb
from chromadb.utils import embedding_functions

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # backend/
VECTORSTORE_DIR = os.path.join(BASE_DIR, "rag", "vectorstore")
COLLECTION_NAME = "techmart_knowledge"

# Load the embedder once when this module is imported (not on every call)
_embedder = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# Connect to the same persistent ChromaDB we built in ingest.py
_client = chromadb.PersistentClient(path=VECTORSTORE_DIR)
_collection = _client.get_collection(
    name=COLLECTION_NAME,
    embedding_function=_embedder,
)


def retrieve_context(query: str, top_k: int = 3) -> str:
    """
    Takes a user query, searches ChromaDB, and returns the most relevant
    chunks joined into a single string — ready to inject into an LLM prompt.
    """
    results = _collection.query(
        query_texts=[query],
        n_results=top_k,
    )

    chunks = results["documents"][0]   # list of matched text chunks
    sources = results["metadatas"][0]  # list of {source: filename}

    if not chunks:
        return "No relevant information found in the knowledge base."

    # Format nicely so the LLM can see where each chunk came from
    formatted = []
    for chunk, meta in zip(chunks, sources):
        formatted.append(f"[From {meta['source']}]\n{chunk}")

    return "\n\n".join(formatted)


# ── Quick test when running this file directly ────────────────────────────────
if __name__ == "__main__":
    test_query = input("Enter a test question: ")
    context = retrieve_context(test_query)
    print("\n--- Retrieved Context ---\n")
    print(context)