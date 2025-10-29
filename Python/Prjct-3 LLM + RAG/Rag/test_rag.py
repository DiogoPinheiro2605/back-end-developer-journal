import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rag_engine import rag_query
from Agents.judge_agent import judge_question_with_embeddings

collection_name = "estrategias_venda"
role_prompt = "És um especialista em vendas de casas e marketing imobiliário."
user_query = "Como posso vender um imóvel rapidamente?"

# 🔍 Passo 1: Validação com embeddings
if judge_question_with_embeddings(user_query, collection_name):
    # ✅ Passo 2: Segue para o RAG normal
    resposta = rag_query(user_query, collection_name, role_prompt)
    print("💬 Resposta do LLM:", resposta)
else:
    # ❌ Pergunta fora de contexto
    print("⚠️ Pergunta rejeitada: não parece relacionada com o tema da coleção.")
