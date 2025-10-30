import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rag_engine import rag_query 
from Agents.judge_agent import judge_question_with_embeddings
from Agents.mother_agent import route_query_to_topic # IMPORTAÇÃO ATUALIZADA

user_query = "Como é que as fotos e vídeos nas redes sociais me ajudam a vender uma casa?"
ROLE_PROMPTS = {
    "estrategias_venda": "You are an expert assistant in house sales, customer service, and closing deals.",
    "marketing": "You are a specialist in digital marketing and content strategy for the real estate market."
}
DEFAULT_ROLE_PROMPT = "You are an expert assistant in the real estate sector."

DISTANCE_THRESHOLD = 9 

print(f"Query: '{user_query}' | Threshold (L2): {DISTANCE_THRESHOLD}")
print("-" * 70)

try:
    collection_name = route_query_to_topic(user_query)
    
    if collection_name is None:
        print("\n❌ Execution Halted: Query could not be routed to a valid knowledge topic.")
        print("💡 Suggestion: Provide a general, non-contextual answer using the default role.")

        sys.exit()

    role_prompt = ROLE_PROMPTS.get(collection_name, DEFAULT_ROLE_PROMPT)
    print(f"✅ Selected Collection: {collection_name}")
    print(f"🎯 Assigned Role: {role_prompt}")
    print("-" * 70)


    if judge_question_with_embeddings(user_query, collection_name, threshold=DISTANCE_THRESHOLD):
        print("✅ Judgment Approved. Consulting RAG...")
        
        response = rag_query(user_query, collection_name, role_prompt)
        print("\n💬 Final LLM Response:\n", response)
    else:
        print("\n⚠️ RAG not executed due to query rejection (distance too high).")
        
except Exception as e:
    print(f"\n❌ FATAL ERROR during execution: {e}")