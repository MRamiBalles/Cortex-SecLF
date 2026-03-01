import os
import re
import logging
from typing import List, Dict, Any, Optional
from .chroma_client import chroma_manager
import PyPDF2
from langchain.text_splitter import RecursiveCharacterTextSplitter

class Ingestor:
    """
    Automates the ingestion and vectorization of canonical archives.
    Implements context-aware splitting to preserve semantic logic in technical docs.
    """
    def __init__(self):
        self.logger = logging.getLogger("cslf.ingestor")
        
        # Generic splitter for academic/legal docs (Higher overlap for conceptual continuity)
        self.generic_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1200,
            chunk_overlap=200,
            add_start_index=True
        )
        
        # 'Trench-Aware' splitter for technical docs/exploits
        # Optimized to keep functional code blocks or exploit chains together
        self.tech_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2500,
            chunk_overlap=400,
            separators=["\nclass ", "\ndef ", "\n# ", "\n\n", "\n", " "],
            add_start_index=True
        )

    def extract_year(self, text: str, filename: str) -> int:
        """Heuristic discovery of document timestamp."""
        # Check filename first (common pattern in archives)
        match = re.search(r'(20\d{2}|19\d{2})', filename)
        if not match:
            # Check early text for copyright or date signatures
            match = re.search(r'(20\d{2}|19\d{2})', text[:3000])
        return int(match.group(1)) if match else 2025

    def detect_language(self, text: str) -> str:
        """Improved heuristic for programming language detection in chunks."""
        text_lower = text.lower()
        if any(x in text for x in ["import ", "def ", 'if __name__ == "__main__"']): return "python"
        if any(x in text_lower for x in ["apt-get ", "sudo ", "curl -", "grep "]): return "bash"
        if any(x in text for x in ["void main", "#include <", "public class "]): return "compiled_lang"
        if "select " in text_lower and "from " in text_lower: return "sql"
        return "natural_language"

    def get_authority_score(self, collection_name: str, filename: str) -> str:
        """Categorizes document trust levels for weighted retrieval."""
        fn = filename.lower()
        if "nist" in fn or "iso" in fn or "whitepaper" in fn: return "Authority (Standard/Formal)"
        if collection_name == "trench": return "Expert (Technical/Adversarial)"
        return "General (Foundation)"

    def extract_text_from_pdf(self, file_path: str) -> str:
        """Robust PDF text extraction with basic error isolation."""
        text = ""
        try:
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page_num, page in enumerate(reader.pages):
                    page_text = page.extract_text()
                    if page_text:
                        text += f"[PAGE {page_num+1}]\n{page_text}\n"
        except Exception as e:
            self.logger.error(f"Failed to parse PDF {file_path}: {e}")
        return text

    def ingest_directory(self, collection_name: str, dir_path: str):
        """Indexes an entire directory into the specified Chroma collection."""
        self.logger.info(f"Synchronizing collection '{collection_name}' with source: {dir_path}")
        
        try:
            collection = chroma_manager.get_collection(collection_name)
        except Exception as e:
            self.logger.critical(f"VectorDB Connection Failure: {e}")
            return

        if not os.path.exists(dir_path):
            self.logger.warning(f"Source path dormant: {dir_path}")
            return

        for filename in os.listdir(dir_path):
            file_path = os.path.join(dir_path, filename)
            if not os.path.isfile(file_path): continue

            self.logger.debug(f"Processing: {filename}")
            content = ""
            try:
                if filename.endswith(".pdf"):
                    content = self.extract_text_from_pdf(file_path)
                elif filename.endswith((".md", ".txt", ".py", ".c")):
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                
                if not content.strip(): continue

                year = self.extract_year(content, filename)
                auth = self.get_authority_score(collection_name, filename)
                
                # Split strategy selection
                splitter = self.tech_splitter if collection_name == "trench" else self.generic_splitter
                chunks = splitter.split_text(content)
                
                # Metadata preparation
                ids = [f"{filename}_{i}" for i in range(len(chunks))]
                metadatas = [{
                    "source": filename,
                    "collection": collection_name,
                    "year": year,
                    "authority": auth,
                    "language": self.detect_language(chunk),
                    "ingested_at": os.path.getmtime(file_path)
                } for chunk in chunks]
                
                collection.add(documents=chunks, metadatas=metadatas, ids=ids)
                self.logger.info(f"Indexed {filename} | Chunks: {len(chunks)} | Collection: {collection_name}")

            except Exception as e:
                self.logger.error(f"Ingestion crash for {filename}: {e}")

if __name__ == "__main__":
    # Base configuration for containerized runs
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ingestor = Ingestor()
    path_map = {"doctrine": "/data/documents/doctrine", "trench": "/data/documents/trench"}
    for col, path in path_map.items():
        ingestor.ingest_directory(col, path)
