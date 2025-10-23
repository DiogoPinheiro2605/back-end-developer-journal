from rag_engine import build_vector_store, rag_query

# 1️⃣ Cria a coleção e adiciona textos
print(build_vector_store("../Data/knowledge/estrategias_venda", "estrategias_venda"))

# 2️⃣ Faz uma pergunta ao RAG
resposta = rag_query("Como posso vender uma casa mais rápido?", "estrategias_venda", "És um especialista em vendas imobiliárias.")
print(resposta)
