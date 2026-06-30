# rag/ingest.py
# Run once to build the vector database from your PDFs
# Usage: python3 rag/ingest.py

import os
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
from chromadb.utils import embedding_functions

# ingest.py is at: customer-support-ai/backend/rag/ingest.py
# We need to go up 2 levels to reach customer-support-ai/, then into knowledge_base/
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
KNOWLEDGE_BASE_DIR = os.path.join(PROJECT_ROOT, "knowledge_base")
VECTORSTORE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "rag", "vectorstore")
COLLECTION_NAME = "techmart_knowledge"


# ── 1. Extract text from every PDF ─────────────────────────────────────────────

def extract_text_from_pdf(filepath: str) -> str:
    reader = PdfReader(filepath)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text


def load_all_documents() -> list[dict]:
    """Returns a list of {filename, text} for every PDF in knowledge_base/"""
    documents = []
    for filename in os.listdir(KNOWLEDGE_BASE_DIR):
        if filename.endswith(".pdf"):
            filepath = os.path.join(KNOWLEDGE_BASE_DIR, filename)
            text = extract_text_from_pdf(filepath)
            documents.append({"filename": filename, "text": text})
            print(f"Loaded: {filename} ({len(text)} characters)")
    return documents


# ── 2. Split each document into chunks ─────────────────────────────────────────

def chunk_documents(documents: list[dict]) -> list[dict]:
    """
    Splits long text into smaller overlapping chunks.
    Overlap helps avoid cutting a sentence in half between chunks.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,       # characters per chunk
        chunk_overlap=50,     # overlap between consecutive chunks
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    chunks = []
    for doc in documents:
        pieces = splitter.split_text(doc["text"])
        for i, piece in enumerate(pieces):
            chunks.append({
                "id": f"{doc['filename']}_{i}",
                "text": piece,
                "source": doc["filename"],
            })
    print(f"\nTotal chunks created: {len(chunks)}")
    return chunks


# ── 3. Embed and store in ChromaDB ─────────────────────────────────────────────

def build_vectorstore(chunks: list[dict]):
    # This embedding function runs locally on your M3 — no API key needed
    embedder = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    client = chromadb.PersistentClient(path=VECTORSTORE_DIR)

    # Delete old collection if it exists, so re-running this script is safe
    try:
        client.delete_collection(COLLECTION_NAME)
        print(f"Deleted existing collection: {COLLECTION_NAME}")
    except Exception:
        pass  # Collection didn't exist yet — that's fine

    collection = client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedder,
    )

    collection.add(
        ids=[c["id"] for c in chunks],
        documents=[c["text"] for c in chunks],
        metadatas=[{"source": c["source"]} for c in chunks],
    )

    print(f"\nStored {len(chunks)} chunks in ChromaDB at: {VECTORSTORE_DIR}")


# ── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Step 1: Loading PDFs...\n")
    documents = load_all_documents()

    print("\nStep 2: Chunking text...")
    chunks = chunk_documents(documents)

    print("\nStep 3: Generating embeddings and storing in ChromaDB...")
    print("(This downloads a small AI model the first time — ~90MB)")
    build_vectorstore(chunks)

    print("\n✅ Ingestion complete. Your knowledge base is ready to search.")