import os
import chromadb

# Persistent path for ChromaDB
DB_PATH = os.path.join(os.path.dirname(__file__), "chroma_db")

client = chromadb.PersistentClient(path=DB_PATH)
collection_name = "advisor_prep_docs"

# Get or create the collection
collection = client.get_or_create_collection(
    name=collection_name,
    metadata={"hnsw:space": "cosine"}
)

def add_document_chunks(client_id: str, document_name: str, chunks: list[dict]):
    """
    Adds chunks to the ChromaDB collection.
    chunks format: [{"text": "...", "page": 1}, ...]
    """
    ids = []
    documents = []
    metadatas = []
    
    for i, chunk in enumerate(chunks):
        ids.append(f"{client_id}_{document_name}_{i}")
        documents.append(chunk["text"])
        metadatas.append({
            "client_id": client_id,
            "document_name": document_name,
            "page": chunk["page"]
        })
        
    if ids:
        collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )

def get_relevant_chunks(client_id: str, query: str, n_results: int = 10):
    """
    Queries ChromaDB for relevant document chunks for a specific client.
    """
    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        where={"client_id": client_id}
    )
    
    if not results or not results["documents"] or not results["documents"][0]:
        return []
        
    extracted = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        extracted.append({
            "text": doc,
            "document_name": meta["document_name"],
            "page": meta["page"]
        })
    return extracted

def is_document_ingested(client_id: str, document_name: str) -> bool:
    """
    Checks if a document has already been ingested to avoid duplicates.
    """
    results = collection.get(
        where={"$and": [{"client_id": client_id}, {"document_name": document_name}]},
        limit=1
    )
    return len(results.get("ids", [])) > 0
