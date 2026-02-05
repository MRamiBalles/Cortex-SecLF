import chromadb
from chromadb.config import Settings
import os

class ChromaClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ChromaClient, cls).__new__(cls)
            
            # Sovereign Mock Support: Fallback to local persistence if Docker is down
            host = os.getenv("CHROMA_DB_HOST", "localhost")
            port = os.getenv("CHROMA_DB_PORT", "8000")
            persist_directory = os.getenv("CHROMA_PERSIST_DIR", "./data/vector_db")
            
            try:
                # Attempt HTTP first (standard v3.0)
                cls._instance.client = chromadb.HttpClient(
                    host=host,
                    port=port,
                    settings=Settings(allow_reset=True)
                )
                print(f"DEBUG: Using ChromaDB HTTP Client ({host}:{port})")
            except Exception:
                # Fallback to local PersistentClient (Sovereign Mock)
                cls._instance.client = chromadb.PersistentClient(
                    path=persist_directory,
                    settings=Settings(allow_reset=True)
                )
                print(f"DEBUG: Using ChromaDB Persistent Client (Path: {persist_directory})")
            
            # Initialize collections
            cls._instance.collections = {
                "doctrine": cls._instance.client.get_or_create_collection(
                    name="cslf_doctrine",
                    metadata={"description": "Legal, Governance & Neuro-Rights"}
                ),
                "trench": cls._instance.client.get_or_create_collection(
                    name="cslf_trench",
                    metadata={"description": "Offensive/Defensive Technical Knowledge"}
                ),
                "future": cls._instance.client.get_or_create_collection(
                    name="cslf_future",
                    metadata={"description": "PQC, GreenOps & Standards"}
                )
            }
            
        return cls._instance

    def get_collection(self, name: str):
        if name not in self.collections:
            raise ValueError(f"Collection '{name}' not found. Use doctrine, trench, or future.")
        return self.collections[name]

chroma_manager = ChromaClient()
