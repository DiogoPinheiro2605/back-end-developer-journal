import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rag_engine import rag_query 
from Agents.judge_agent import judge_question_with_embeddings

collection_name = "estrategias_venda" 
user_query = "I want a marketing tip for real estate brokers."
role_prompt = "You are an expert assistant in house sales and real estate marketing."


DISTANCE_THRESHOLD = 9

print(f"Collection: {collection_name} | Query: '{user_query}' | Threshold (L2): {DISTANCE_THRESHOLD}")
print("-" * 70)

try:
    if judge_question_with_embeddings(user_query, collection_name, threshold=DISTANCE_THRESHOLD):
        print("Judgment Approved. Consulting RAG...")
        
        response = rag_query(user_query, collection_name, role_prompt)
        print("\nLLM Response:\n", response)
    else:
        print("\nWARNING: RAG not executed due to query rejection.")
        
except Exception as e:
    print(f"\nFATAL ERROR during execution: {e}")