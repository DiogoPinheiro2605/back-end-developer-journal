import os
from langchain_core.documents import Document
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
KNOWLEDGE_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "Data", "knowledge")) 

def load_documents(collection_name: str) -> List[Document]:
    directory_path = os.path.join(KNOWLEDGE_DIR, collection_name)

    if not os.path.exists(directory_path):
        return []
        
    loader = DirectoryLoader(
        path=directory_path,
        glob="**/*.txt",
        show_progress=True,
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"} 
    )
    
    documents = loader.load()
    return documents

def split_text(document: Document) -> List[Document]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""]
    )
    return text_splitter.split_documents([document])