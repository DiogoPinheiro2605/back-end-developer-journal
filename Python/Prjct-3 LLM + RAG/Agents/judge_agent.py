import sys
import os
from typing import Optional

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Rag'))) 

try:
    from rag_chroma import get_or_create_vectordb
except ImportError:
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
        return False