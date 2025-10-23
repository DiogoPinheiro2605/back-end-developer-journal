from rag_loader import load_documents, split_text
from rag_chroma import add_documents_to_collection, search_similar_chunks
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config_LLM import ask_llm

def build_vector_store(data_dir: str, collection_name: str):
    docs = load_documents(data_dir)
    chunks = []
    for doc in docs:
        chunks.extend(split_text(doc))
    add_documents_to_collection(collection_name, chunks) 
    return f"Collection '{collection_name}' built with {len(chunks)}chunks."

def rag_query(user_query: str, collection_name: str, role_prompt: str):
    relevant_chunks = search_similar_chunks(collection_name, user_query)
    context = "\n\n".join(relevant_chunks)

    prompt = f"""
{role_prompt}

Baseia-te apenas no contexto abaixo para responder à pergunta.

Contexto:
{context}

Pergunta: {user_query}
"""
    return ask_llm(prompt)
