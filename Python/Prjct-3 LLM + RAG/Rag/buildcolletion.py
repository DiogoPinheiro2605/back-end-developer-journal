import os
from langchain_text_splitters import CharacterTextSplitter 
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "..", "Data", "knowledge", "estrategias_venda", "estrategias_venda.txt")

try:
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
except FileNotFoundError:
    print(f"❌ ERRO: Ficheiro não encontrado no caminho: {file_path}")
    exit()

text_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=500,
    chunk_overlap=50
)

chunks = text_splitter.split_text(text)

documents = [Document(page_content=chunk) for chunk in chunks]

from langchain_ollama import OllamaEmbeddings
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

persist_dir = os.path.join(current_dir, "chroma_db", "estrategias_venda")
os.makedirs(persist_dir, exist_ok=True)

collection = Chroma.from_documents(
    documents=documents, 
    embedding=embeddings, 
    collection_name="estrategias_venda",
    persist_directory=persist_dir 
)

print(f"✅ Coleção 'estrategias_venda' construída e persistida com {len(chunks)} chunks.")
print(f"📁 Persistida em: {persist_dir}")