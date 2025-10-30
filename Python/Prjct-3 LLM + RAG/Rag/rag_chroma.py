import os
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from typing import List
from langchain_chroma import Chroma

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
CHROMA_DIR = os.path.join(BASE_DIR, "..", "Data", "chroma", "chroma_db") 
os.makedirs(CHROMA_DIR, exist_ok=True) 

embeddings = OllamaEmbeddings(model="mxbai-embed-large")

_vectordb_cache = {}

def get_or_create_vectordb(collection_name: str) -> Chroma:
    if collection_name in _vectordb_cache:
        return _vectordb_cache[collection_name]

    persist_dir = os.path.join(CHROMA_DIR, collection_name)
    os.makedirs(persist_dir, exist_ok=True)
        
    vectordb = Chroma(
        persist_directory=persist_dir,
        embedding_function=embeddings,
        collection_name=collection_name
    )
    
    _vectordb_cache[collection_name] = vectordb
    return vectordb

def add_documents_to_collection(collection_name: str, documents: List[Document]):
    vectordb = get_or_create_vectordb(collection_name)
    initial_count = vectordb._collection.count()
    
    if initial_count == 0:
        vectordb.add_documents(documents)

def search_similar_chunks(collection_name: str, query: str, k: int = 4) -> List[str]:
    vectordb = get_or_create_vectordb(collection_name)
    docs = vectordb.similarity_search(query, k=k)
    return [doc.page_content for doc in docs]