import os
import re
import logging
import hashlib
from typing import List, Dict, Any, Optional
from concurrent.futures import ProcessPoolExecutor
from .chroma_client import chroma_manager
from ..shared.telemetry import lattice_monitor
import PyPDF2
from langchain.text_splitter import RecursiveCharacterTextSplitter

class Ingestor:
    """
    Automates the ingestion and vectorization of canonical archives.
    Implements context-aware splitting and parallel processing.
    """
    def __init__(self):
        self.logger = logging.getLogger("cslf.ingestor")
        self.state_file = "./data/ingestion_state.json"
        
        # Generic splitter for academic/legal docs
        self.generic_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1200,
            chunk_overlap=200,
            add_start_index=True
        )
        
        # 'Trench-Aware' splitter for technical docs/exploits
        self.tech_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2500,
            chunk_overlap=400,
            separators=["\nclass ", "\ndef ", "\n# ", "\n\n", "\n", " "],
            add_start_index=True
        )

    def compute_file_hash(self, file_path: str) -> str:
        """Computes SHA-256 hash of a file for change tracking."""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def extract_year(self, text: str, filename: str) -> int:
        match = re.search(r'(20\d{2}|19\d{2})', filename)
        if not match:
            match = re.search(r'(20\d{2}|19\d{2})', text[:3000])
        return int(match.group(1)) if match else 2025

    def detect_language(self, text: str) -> str:
        text_lower = text.lower()
        if any(x in text for x in ["import ", "def ", 'if __name__ == "__main__"']): return "python"
        if any(x in text_lower for x in ["apt-get ", "sudo ", "curl -", "grep "]): return "bash"
        if any(x in text for x in ["void main", "#include <", "public class "]): return "compiled_lang"
        if "select " in text_lower and "from " in text_lower: return "sql"
        return "natural_language"

    def get_authority_score(self, collection_name: str, filename: str) -> str:
        fn = filename.lower()
        if "nist" in fn or "iso" in fn or "whitepaper" in fn: return "Authority (Standard/Formal)"
        if collection_name == "trench": return "Expert (Technical/Adversarial)"
        return "General (Foundation)"

    def extract_text_from_pdf(self, file_path: str) -> str:
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

    def process_file(self, collection_name: str, file_path: str) -> Optional[Dict[str, Any]]:
        """Core logic for processing a single file. Suitable for parallel execution."""
        filename = os.path.basename(file_path)
        try:
            content = ""
            if filename.endswith(".pdf"):
                content = self.extract_text_from_pdf(file_path)
            elif filename.endswith((".md", ".txt", ".py", ".c")):
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
            
            if not content.strip(): return None

            year = self.extract_year(content, filename)
            auth = self.get_authority_score(collection_name, filename)
            
            splitter = self.tech_splitter if collection_name == "trench" else self.generic_splitter
            chunks = splitter.split_text(content)
            
            ids = [f"{filename}_{i}" for i in range(len(chunks))]
            metadatas = [{
                "source": filename,
                "collection": collection_name,
                "year": year,
                "authority": auth,
                "language": self.detect_language(chunk),
                "ingested_at": time.time()
            } for chunk in chunks]
            
            return {"chunks": chunks, "metadatas": metadatas, "ids": ids}
        except Exception as e:
            self.logger.error(f"Process failure for {filename}: {e}")
            return None

    def ingest_directory(self, collection_name: str, dir_path: str):
        """Indexes directory with parallel processing and state persistence."""
        self.logger.info(f"SYNCHRONIZING: {collection_name} | {dir_path}")
        lattice_monitor.update_heartbeat("rag", status="INGESTING")
        
        try:
            collection = chroma_manager.get_collection(collection_name)
        except Exception as e:
            self.logger.critical(f"CHROMA_FAILURE: {e}")
            return

        if not os.path.exists(dir_path):
            return

        all_files = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
        
        # Parallel Execution
        with ProcessPoolExecutor() as executor:
            futures = [executor.submit(self.process_file, collection_name, fp) for fp in all_files]
            
            for future in futures:
                result = future.result()
                if result:
                    try:
                        collection.add(
                            documents=result["chunks"],
                            metadatas=result["metadatas"],
                            ids=result["ids"]
                        )
                        self.logger.info(f"INDEXED: {result['metadatas'][0]['source']} ({len(result['chunks'])} chunks)")
                    except Exception as e:
                        self.logger.error(f"DB insertion error: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ingestor = Ingestor()
    path_map = {"doctrine": "./data/documents/doctrine", "trench": "./data/documents/trench"}
    for col, path in path_map.items():
        ingestor.ingest_directory(col, path)
