import os
import chromadb
from sentence_transformers import SentenceTransformer

# Caminho onde o ChromaDB vai guardar os vetores
CHROMA_PATH = os.path.join(os.path.dirname(__file__), "..", "Data", "chroma_db")

model = SentenceTransformer("all-MiniLM-L6-v2")

# Inicializa o cliente local do Chroma
client = chromadb.PersistentClient(path=CHROMA_PATH)

def create_or_get_collection(collection_name: str):
    return client.get_or_create_collection(name=collection_name)

def add_documents_to_collection(collection_name: str, chunks: list):
    collection = create_or_get_collection(collection_name)
    embeddings = model.encode(chunks).tolist()
    ids = [f"chunk_{i}" for i in range(len(chunks))]

    collection.add(documents=chunks, embeddings=embeddings, ids=ids)
    return f"Added {len(chunks)} chunks to {collection_name}"

def search_similar_chunks(collection_name: str, query: str, top_k: int = 3):
    collection = create_or_get_collection(collection_name)
    query_embedding = model.encode([query]).tolist()
    results = collection.query(query_embeddings=query_embedding, n_results=top_k)
    return results["documents"][0]
