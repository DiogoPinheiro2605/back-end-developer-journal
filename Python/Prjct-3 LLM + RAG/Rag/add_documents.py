# add_documents.py
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
import os

# Configura embeddings
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

# Cache para vectorstores
_vectordb_cache = {}

def get_vectordb(collection_name: str):
    if collection_name not in _vectordb_cache:
        persist_dir = f"chroma/{collection_name}"
        os.makedirs(persist_dir, exist_ok=True)
        _vectordb_cache[collection_name] = Chroma(
            persist_directory=persist_dir,
            embedding_function=embeddings
        )
    return _vectordb_cache[collection_name]

def add_documents_to_collection(collection_name: str, texts: list[str]):
    vectordb = get_vectordb(collection_name)
    # Adiciona textos diretamente
    vectordb.add_texts(texts)
    # Não é necessário chamar persist() nas versões novas
    print(f"✅ Adicionados {len(texts)} documentos à coleção '{collection_name}'")

# Textos reais
textos = [
    "Para vender um imóvel rapidamente, é essencial fazer uma boa apresentação do imóvel...",
    "O marketing digital é uma ferramenta poderosa para corretores de imóveis...",
    "Para conquistar clientes, é importante criar um relacionamento próximo e de confiança...",
    "Realizar visitas virtuais aos imóveis pode aumentar significativamente o interesse dos compradores...",
    "Uma estratégia eficiente de prospecção de clientes é segmentar o público-alvo...",
    "Acompanhar métricas de vendas é fundamental...",
    "Oferecer conteúdo educativo para clientes potenciais posiciona o corretor como especialista...",
    "A negociação de imóveis deve ser transparente e justa..."
]

if __name__ == "__main__":
    add_documents_to_collection("marketing", textos)
