import os
import re
from typing import List, Dict, Any
from .chroma_client import chroma_manager
import PyPDF2
from langchain.text_splitter import RecursiveCharacterTextSplitter, Language

class Ingestor:
    def __init__(self):
        # Generic splitter for academic/legal docs
        self.generic_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1200,
            chunk_overlap=150
        )
        
        # 'Context-Aware' splitter for technical docs (Trench)
        # We use a larger chunk size to keep exploit logic together
        self.tech_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=300,
            separators=["\nclass ", "\ndef ", "\n# ", "\n\n", "\n", " "]
        )

    def extract_year(self, text: str, filename: str) -> int:
        # Try finding 4-digit years in filename or first 2000 chars of text
        match = re.search(r'(20\d{2}|19\d{2})', filename)
        if not match:
            match = re.search(r'(20\d{2}|19\d{2})', text[:2000])
        return int(match.group(1)) if match else 2024 # Default to 2024 if unknown

    def detect_language(self, text: str) -> str:
        if "import " in text or "def " in text: return "python"
        if "bash" in text or "apt-get" in text: return "bash"
        if "void main" in text or "#include" in text: return "c/cpp"
        return "text"

    def get_authority(self, collection_name: str, filename: str) -> str:
        if collection_name == "doctrine": return "High (Academic/Legal)"
        if "S4vitar" in filename or "IppSec" in filename: return "High (Technical Expert)"
        return "Medium (Resource)"

    def extract_text_from_pdf(self, file_path: str) -> str:
        text = ""
        try:
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            print(f"Error reading PDF {file_path}: {e}")
        return text

    def ingest_directory(self, collection_name: str, dir_path: str):
        print(f"Ingesting {collection_name} from {dir_path}...")
        collection = chroma_manager.get_collection(collection_name)
        
        if not os.path.exists(dir_path): return

        for filename in os.listdir(dir_path):
            file_path = os.path.join(dir_path, filename)
            if not os.path.isfile(file_path): continue

            content = ""
            if filename.endswith(".pdf"):
                content = self.extract_text_from_pdf(file_path)
            elif filename.endswith((".md", ".txt")):
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
            
            if content:
                year = self.extract_year(content, filename)
                authority = self.get_authority(collection_name, filename)
                
                # Use tech splitter for Trench to preserve exploit logic
                splitter = self.tech_splitter if collection_name == "trench" else self.generic_splitter
                chunks = splitter.split_text(content)
                
                ids = [f"{filename}_{i}" for i in range(len(chunks))]
                metadatas = []
                for chunk in chunks:
                    metadatas.append({
                        "source": filename,
                        "collection": collection_name,
                        "year": year,
                        "authority": authority,
                        "language": self.detect_language(chunk),
                        "type": "canonical_archive"
                    })
                
                collection.add(documents=chunks, metadatas=metadatas, ids=ids)
                print(f"Indexed {filename} ({len(chunks)} chunks) [Year: {year}] [Auth: {authority}]")

# Example usage (can be triggered via API or CLI)
if __name__ == "__main__":
    ingestor = Ingestor()
    base_data_path = "/data/documents" # Path inside container
    
    ingestor.ingest_directory("doctrine", f"{base_data_path}/doctrine")
    ingestor.ingest_directory("trench", f"{base_data_path}/trench")
    ingestor.ingest_directory("future", f"{base_data_path}/future")
