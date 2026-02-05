import os
from typing import List
from .chroma_client import chroma_manager
import PyPDF2
import markdown
from langchain.text_splitter import RecursiveCharacterTextSplitter, Language

class Ingestor:
    def __init__(self):
        # Specific splitters for different types of content
        self.generic_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100
        )
        
        # Splitter that respects code blocks for the "Trench" collection
        self.code_splitter = RecursiveCharacterTextSplitter.from_language(
            language=Language.PYTHON, # Defaulting to Python for offshore/scapy logic
            chunk_size=1500,
            chunk_overlap=200
        )

    def extract_text_from_pdf(self, file_path: str) -> str:
        text = ""
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text

    def ingest_directory(self, collection_name: str, dir_path: str):
        print(f"Ingesting {collection_name} from {dir_path}...")
        collection = chroma_manager.get_collection(collection_name)
        
        if not os.path.exists(dir_path):
            print(f"Warning: Directory {dir_path} does not exist.")
            return

        for filename in os.listdir(dir_path):
            file_path = os.path.join(dir_path, filename)
            if os.path.isfile(file_path):
                content = ""
                if filename.endswith(".pdf"):
                    content = self.extract_text_from_pdf(file_path)
                elif filename.endswith(".md") or filename.endswith(".txt"):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                
                if content:
                    # Choose splitter based on collection
                    splitter = self.code_splitter if collection_name == "trench" else self.generic_splitter
                    chunks = splitter.split_text(content)
                    
                    ids = [f"{filename}_{i}" for i in range(len(chunks))]
                    metadatas = [{
                        "source": filename,
                        "collection": collection_name,
                        "type": "canonical_archive"
                    } for _ in range(len(chunks))]
                    
                    collection.add(
                        documents=chunks,
                        metadatas=metadatas,
                        ids=ids
                    )
                    print(f"Added {len(chunks)} chunks from {filename} to {collection_name}.")

# Example usage (can be triggered via API or CLI)
if __name__ == "__main__":
    ingestor = Ingestor()
    base_data_path = "/data/documents" # Path inside container
    
    ingestor.ingest_directory("doctrine", f"{base_data_path}/doctrine")
    ingestor.ingest_directory("trench", f"{base_data_path}/trench")
    ingestor.ingest_directory("future", f"{base_data_path}/future")
