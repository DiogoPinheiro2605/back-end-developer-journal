import sys
import os
from typing import Optional, Literal

# Adiciona o diretório Prjct-3 LLM + RAG/ ao PATH para encontrar config_LLM.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) 

try:
    from config_LLM import ask_llm
except ImportError:
    def ask_llm(prompt):
        return "ERROR: config_LLM module not loaded."

# Defina os temas válidos (coleções Chroma)
VALID_TOPICS = ["estrategias_venda", "marketing"]

def route_query_to_topic(user_query: str) -> Optional[str]:
    """
    Asks the LLM to classify the user's query into one of the available knowledge topics.
    Returns the selected topic/collection name or None if classification fails.
    """
    
    topic_list = ", ".join(VALID_TOPICS)
    
    routing_prompt = f"""
Analyze the following user query and classify its topic.
Your response MUST be ONLY ONE of the following valid collection names: {topic_list}.
If the query does not clearly fit any topic, respond ONLY with "unknown".

Topics:
- estrategias_venda: Topics related to closing deals, customer service, follow-up, and quick house sales.
- marketing: Topics related to digital promotion, content creation, social media, and market analysis.

User Query: "{user_query}"

Selected Topic:
"""
    
    print("🧠 Mother Agent: Classifying query intent...")
    
    try:
        llm_response = ask_llm(routing_prompt).strip().lower()
    except Exception as e:
        print(f"❌ LLM call failed during routing: {e}")
        return None

    # Tenta corresponder a resposta do LLM a um tópico válido
    if llm_response in VALID_TOPICS:
        print(f"✅ Mother Agent: Classified as '{llm_response}'")
        return llm_response
    else:
        print(f"⚠️ Mother Agent: Classification failed or is 'unknown'. LLM response: {llm_response}")
        return None