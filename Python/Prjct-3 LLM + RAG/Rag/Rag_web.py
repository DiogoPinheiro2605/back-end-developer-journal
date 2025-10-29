# Rag_web.py
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_chroma import Chroma
from langchain_community.utilities import SerpAPIWrapper

# =========================
# CONFIGURAÇÃO
# =========================

# Embeddings e base de dados local
embeddings = OllamaEmbeddings(model="mxbai-embed-large")
vectordb = Chroma(
    persist_directory="chroma/marketing",
    embedding_function=embeddings
)
retriever = vectordb.as_retriever(search_kwargs={"k": 3})

# LLM
llm = OllamaLLM(model="mxbai")

# SerpAPI
search = SerpAPIWrapper(
    serpapi_api_key="b987cbefd854f06631d4c4a784c216a4f51a7717981a312a14e9e3463535ee36"
)

# Prompt template
BASE_PROMPT = """
Usa o contexto abaixo para responder à pergunta do utilizador.
Se não houver informação suficiente no contexto, diz claramente que não sabes.

Contexto:
{context}

Pergunta:
{question}

Resposta clara e objetiva:
"""

# =========================
# FUNÇÕES AUXILIARES
# =========================

def build_context(docs, max_chars=4000):
    """Concatena documentos em um contexto, respeitando o limite de caracteres"""
    parts = []
    total = 0
    for d in docs:
        text = getattr(d, "page_content", str(d))
        if not text:
            continue
        if total + len(text) > max_chars:
            remaining = max_chars - total
            if remaining <= 0:
                break
            parts.append(text[:remaining])
            total += remaining
            break
        parts.append(text)
        total += len(text)
    return "\n\n---\n\n".join(parts)


def hybrid_rag(query: str):
    # 1️⃣ Recupera documentos locais (fallback para método interno)
    try:
        docs = retriever._get_relevant_documents(query)  # ⚠️ método interno
    except Exception:
        docs = []

    # 2️⃣ Monta contexto
    context = build_context(docs)

    # 3️⃣ Cria prompt
    prompt = BASE_PROMPT.format(context=context, question=query)

    # 4️⃣ Chama LLM local
    try:
        answer_local = llm(prompt)
        if isinstance(answer_local, dict) and "text" in answer_local:
            answer_local = answer_local["text"]
        elif not isinstance(answer_local, str):
            answer_local = str(answer_local)
    except Exception:
        answer_local = "[Erro ao chamar LLM local]"

    # 5️⃣ Busca web
    try:
        web_answer = search.run(query)
    except Exception:
        web_answer = "[Erro na pesquisa web]"

    # 6️⃣ Combina respostas
    final_answer = (
        f"=== Resposta Local ===\n{answer_local}\n\n"
        f"=== Informação Web ===\n{web_answer}\n\n"
        f"=== Documentos Consultados (resumo) ===\n"
        + ("\n\n".join([d.metadata.get("source", "") + ": " + (d.page_content[:250] + "...")
                        for d in docs]) if docs else "Nenhum")
    )

    return final_answer

if __name__ == "__main__":
    pergunta = "Como aumentar vendas de imóveis em 2025?"
    resposta = hybrid_rag(pergunta)
    print(resposta)
