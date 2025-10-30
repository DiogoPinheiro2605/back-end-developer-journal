import sys
import os
from rag_chroma import search_similar_chunks

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))) 

# Importa o novo agente
from Agents.summarize_agent import summarize_response

def rag_query(user_query: str, collection_name: str, role_prompt: str):
    """
    Performs the full RAG query: retrieves relevant chunks and delegates 
    the final response generation to the Summarize Agent.
    """
    
    # 1. RETRIEVAL: Search for relevant chunks
    relevant_chunks = search_similar_chunks(collection_name, user_query, k=4) 
    
    context = "\n\n".join(relevant_chunks)

    if not context.strip():
        return "The knowledge base did not return any relevant information for this query."

    print("📝 Sending context and query to Summarize Agent...")
    
    final_answer = summarize_response(
        user_query=user_query,
        context=context,
        role_prompt=role_prompt
    )

    return final_answer