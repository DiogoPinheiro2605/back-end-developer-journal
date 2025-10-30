# Rag_web.py
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_chroma import Chroma
from langchain_community.utilities import SerpAPIWrapper
from datetime import datetime

embeddings = OllamaEmbeddings(model="mxbai-embed-large")
vectordb = Chroma(
    persist_directory="chroma/marketing",
    embedding_function=embeddings
)
retriever = vectordb.as_retriever(search_kwargs={"k": 3})

# LLMs
llm_main = OllamaLLM(model="mxbai")
llm_judge = OllamaLLM(model="llama3")   
llm_summary = OllamaLLM(model="mistral")    

# SerpAPI
search = SerpAPIWrapper(
    serpapi_api_key="b987cbefd854f06631d4c4a784c216a4f51a7717981a312a14e9e3463535ee36"
)

# =============== PROMPTS ===============
PROMPT_MAIN = """
Usa o contexto abaixo e, se necessário, pesquisa web para responder à pergunta do utilizador.
Se não houver informação suficiente, diz claramente que não sabes.

Contexto:
{context}

Pergunta:
{question}

Resposta clara e objetiva:
"""

PROMPT_JUDGE = """
És um avaliador especializado. Recebeste uma resposta de uma IA para uma pergunta.

Pergunta: {question}
Resposta: {answer}

Analisa se a resposta é factual e confiável.
Responde APENAS com "APROVADA" se for fidedigna, ou "REPROVADA" se parecer imprecisa.
"""

PROMPT_SUMMARY = """
Recebeste a seguinte resposta aprovada:

{answer}

Reescreve-a de forma mais curta, clara e profissional, mantendo a precisão.
"""

# =============== FUNÇÕES ===============

def build_context(docs, max_chars=4000):
    parts, total = [], 0
    for d in docs:
        text = getattr(d, "page_content", str(d))
        if not text:
            continue
        if total + len(text) > max_chars:
            parts.append(text[:max_chars - total])
            break
        parts.append(text)
        total += len(text)
    return "\n\n---\n\n".join(parts)


def hybrid_rag(query: str):
    try:
        docs = retriever._get_relevant_documents(query)
    except Exception:
        docs = []

    context = build_context(docs)
    prompt = PROMPT_MAIN.format(context=context, question=query)

    try:
        answer_local = llm_main(prompt)
        if isinstance(answer_local, dict) and "text" in answer_local:
            answer_local = answer_local["text"]
        elif not isinstance(answer_local, str):
            answer_local = str(answer_local)
    except Exception:
        answer_local = "[Erro ao gerar resposta local]"
    try:
        web_answer = search.run(query)
    except Exception:
        web_answer = "[Erro na pesquisa web]"

    full_answer = f"{answer_local}\n\nInformação Web:\n{web_answer}"
    return full_answer, docs


def evaluate_answer(question: str, answer: str) -> bool:
    """Verifica se a resposta é fidedigna"""
    prompt = PROMPT_JUDGE.format(question=question, answer=answer)
    result = llm_judge.invoke(prompt)
    result_text = str(result).strip().upper()
    return "APROVADA" in result_text


def summarize_answer(answer: str) -> str:
    """Simplifica e clarifica a resposta"""
    prompt = PROMPT_SUMMARY.format(answer=answer)
    summary = llm_summary.invoke(prompt)
    return str(summary).strip()


def save_to_vectordb(question: str, answer: str):
    """Guarda a resposta aprovada no ChromaDB"""
    vectordb.add_texts(
        texts=[f"Pergunta: {question}\nResposta: {answer}"],
        metadatas=[{"timestamp": datetime.now().isoformat()}]
    )
    print("✅ Resposta aprovada e guardada na base de dados!")


if __name__ == "__main__":
    pergunta = "Como aumentar as vendas de imóveis em 2025?"
    resposta, docs = hybrid_rag(pergunta)
    print("=== Resposta Original ===")
    print(resposta)

    # 1️⃣ Avaliar resposta
    if evaluate_answer(pergunta, resposta):
        print("\n✅ A resposta foi aprovada pelo AI Judge.")
        resumo = summarize_answer.invoke(resposta)
        print("\n=== Resumo Final ===")
        print(resumo)
        save_to_vectordb(pergunta, resumo)
    else:
        print("\n❌ A resposta foi reprovada pelo AI Judge e não será guardada.")
