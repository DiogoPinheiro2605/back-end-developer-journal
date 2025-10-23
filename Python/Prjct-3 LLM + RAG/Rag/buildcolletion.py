from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain_community.vectorstores import Chroma

# Lê o conteúdo do ficheiro txt
with open("../Data/knowledge/estrategias_venda/estrategias_venda.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Dividir o texto em chunks
text_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=500,
    chunk_overlap=50
)

chunks = text_splitter.split_text(text)

# Transformar em documentos para o ChromaDB
documents = [Document(page_content=chunk) for chunk in chunks]

# Criar/atualizar a coleção
collection = Chroma.from_documents(documents, collection_name="estrategias_venda")

print(f"Collection 'estrategias_venda' construída com {len(chunks)} chunks.")
