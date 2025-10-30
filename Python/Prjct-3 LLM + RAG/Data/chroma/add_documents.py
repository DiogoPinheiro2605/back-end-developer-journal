import os
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import DirectoryLoader, TextLoader # Importa TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter 
from langchain_ollama import OllamaEmbeddings
from typing import List

# 💥 CONFIGURAÇÃO DE CAMINHOS ABSOLUTOS
# Isto aponta para o diretório onde o script está: .../Data/chroma
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 

# 1. Diretório de ORIGEM dos dados (Data/knowledge)
# É preciso subir um nível (..) de 'chroma/' e entrar em 'knowledge/'
DATA_DIR = os.path.join(BASE_DIR, "..", "knowledge") 

# 2. Diretório de PERSISTÊNCIA do Chroma (Data/chroma/chroma_db)
CHROMA_DIR = os.path.join(BASE_DIR, "chroma_db") 
os.makedirs(CHROMA_DIR, exist_ok=True) 

# 🔄 CONFIGURAÇÃO DE EMBEDDINGS
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

# --- FUNÇÕES DE CARREGAMENTO E PROCESSAMENTO ---

def load_documents_from_directory(directory_path: str) -> List[Document]:
    """
    Carrega documentos de um diretório usando TextLoader para evitar a dependência 'unstructured'.
    Assume que os ficheiros são .txt
    """
    print(f"🔄 A carregar ficheiros do diretório: {directory_path}...")
    
    if not os.path.exists(directory_path):
        print(f"❌ ERRO: Diretório não encontrado: '{directory_path}'")
        return []
    
    # Usar TextLoader para ficheiros .txt evita a dependência 'unstructured'
    loader = DirectoryLoader(
        path=directory_path,
        glob="**/*.txt",           # Apenas carrega ficheiros .txt
        show_progress=True,
        loader_cls=TextLoader,     # Força o uso do TextLoader simples
        loader_kwargs={"encoding": "utf-8"} 
    )
    
    documents = loader.load()
    print(f"✅ Carregados {len(documents)} documentos.")
    return documents

def split_documents(documents: List[Document]) -> List[Document]:
    """Divide os documentos em chunks mais pequenos."""
    print("🔄 A dividir documentos em chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_documents(documents)
    print(f"✅ Dividido em {len(chunks)} chunks.")
    return chunks

def get_or_create_vectordb(collection_name: str) -> Chroma:
    """Carrega uma coleção Chroma existente ou cria uma nova, garantindo persistência."""
    persist_dir = os.path.join(CHROMA_DIR, collection_name)
    os.makedirs(persist_dir, exist_ok=True)
    
    print(f"\n🔄 Tentando carregar/criar coleção '{collection_name}' em {persist_dir}...")
    
    vectordb = Chroma(
        persist_directory=persist_dir,
        embedding_function=embeddings,
        collection_name=collection_name
    )
    
    doc_count = vectordb._collection.count()
    print(f"✅ Coleção pronta. Documentos existentes: {doc_count}")
    return vectordb

def add_documents_to_collection(collection_name: str, documents: List[Document]):
    """Adiciona documentos processados à coleção Chroma, com verificação de duplicação."""
    
    vectordb = get_or_create_vectordb(collection_name)
    
    # Adicionar apenas se for uma primeira execução (Verificação Anti-Duplicação Simples)
    initial_count = vectordb._collection.count()
    
    if initial_count == 0:
        vectordb.add_documents(documents)
        
        final_count = vectordb._collection.count()
        print(f"✅ Coleção '{collection_name}' inicializada! Adicionados {len(documents)} chunks.")
    else:
        print(f"ℹ️ Coleção '{collection_name}' já contém {initial_count} chunks. Nada adicionado para evitar duplicação.")

# --- FLUXO PRINCIPAL ---
if __name__ == "__main__":
    
    # 💥 DEFINA A LISTA DE PASTAS QUE QUER PROCESSAR AQUI
    # Cada nome deve corresponder a uma subpasta em Data/knowledge/
    collections_to_process = ["estrategias_venda", "marketing"] 
    
    for collection_name in collections_to_process:
        
        # O caminho de origem é: Data/knowledge/{collection_name}
        target_data_path = os.path.join(DATA_DIR, collection_name)
        
        # 1. Carregar documentos (lida com múltiplos ficheiros .txt)
        all_documents = load_documents_from_directory(target_data_path)
        
        if all_documents:
            # 2. Dividir documentos em chunks
            all_chunks = split_documents(all_documents)
            
            # 3. Adicionar chunks à Chroma DB
            add_documents_to_collection(collection_name, all_chunks)
        else:
            print(f"⚠️ Ignorando coleção '{collection_name}'. Não foram encontrados documentos .txt.")