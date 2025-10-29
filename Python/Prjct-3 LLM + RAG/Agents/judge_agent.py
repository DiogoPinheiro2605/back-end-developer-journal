from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

embeddings = OllamaEmbeddings(model="mxbai-embed-large")
_vectordb_cache = {}

def get_vectordb(collection_name: str):
    if collection_name not in _vectordb_cache:
        _vectordb_cache[collection_name] = Chroma(
            persist_directory=f"chroma/{collection_name}",
            embedding_function=embeddings
        )
    return _vectordb_cache[collection_name]

def judge_question_with_embeddings(question: str, collection_name: str, threshold: float = 0.5) -> bool:
    vectordb = get_vectordb(collection_name)
    results = vectordb.similarity_search_with_score(question, k=1)

    if not results:
        print("⚠️ Nenhum resultado encontrado.")
        return False

    doc, score = results[0]
    print(f"🔎 Similaridade calculada: {score:.3f}")
    print(f"📄 Documento mais próximo: {doc.page_content[:100]}...")  # mostra os primeiros 100 caracteres

    return score < threshold  # correto se score é distância
