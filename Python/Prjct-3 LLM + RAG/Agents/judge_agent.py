import sys
import os
from typing import Optional

# 1. Ajusta o caminho para incluir a pasta 'Rag/' que está no mesmo nível que 'Agents/'.
# O script está em /Agents/, sobe um nível (..) para /Prjct-3 LLM + RAG/ e entra em /Rag/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Rag'))) 

try:
    # 2. Agora o Python encontra rag_chroma.py e importa a função
    from Rag.rag_chroma import get_or_create_vectordb
except ImportError as e:
    # Se o erro persistir, a exceção é útil
    print(f"❌ ERROR: Could not import get_or_create_vectordb from rag_chroma. Check sys.path and file name. Details: {e}")
    def get_or_create_vectordb(collection_name):
        raise RuntimeError("ERROR: rag_chroma module inaccessible.")
        
def judge_question_with_embeddings(user_query: str, collection_name: str, threshold: float = 9.0) -> bool:
    
    try:
        vectordb = get_or_create_vectordb(collection_name)
        docs_with_scores = vectordb.similarity_search_with_score(user_query, k=1)
        
        if not docs_with_scores:
            return False
            
        doc, distance_score = docs_with_scores[0]
        
        if distance_score <= threshold:
            return True
        else:
            return False
            
    except Exception as e:
        # Se a exceção for devido ao RuntimeError (importação falhada), vai falhar aqui.
        return False