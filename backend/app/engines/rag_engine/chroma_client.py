import chromadb
from chromadb.config import Settings
import os
import time
import logging

class ChromaClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ChromaClient, cls).__new__(cls)
            cls._instance.logger = logging.getLogger("cslf.chroma")
            
            # Sovereign Mock Support: Fallback to local persistence if Docker is down
            host = os.getenv("CHROMA_DB_HOST", "localhost")
            port = os.getenv("CHROMA_DB_PORT", "8000")
            persist_directory = os.getenv("CHROMA_PERSIST_DIR", "./data/vector_db")
            
            # Retry configuration
            max_retries = 3
            retry_delay = 2

            for attempt in range(max_retries):
                try:
                    # Attempt HTTP first (standard v3.0)
                    cls._instance.client = chromadb.HttpClient(
                        host=host,
                        port=port,
                        settings=Settings(allow_reset=True)
                    )
                    # Verify connectivity
                    cls._instance.client.heartbeat()
                    cls._instance.logger.info(f"CONNECTED: ChromaDB HTTP Client ({host}:{port})")
                    break
                except Exception as e:
                    if attempt < max_retries - 1:
                        cls._instance.logger.warning(f"Connection attempt {attempt+1} failed. Retrying in {retry_delay}s...")
                        time.sleep(retry_delay)
                    else:
                        cls._instance.logger.error(f"HTTP Connection failed after {max_retries} attempts. Falling back to PersistentClient.")
                        cls._instance.client = chromadb.PersistentClient(
                            path=persist_directory,
                            settings=Settings(allow_reset=True)
                        )
                        cls._instance.logger.info(f"SOVEREIGN_FALLBACK: Using ChromaDB Persistent Client (Path: {persist_directory})")
            
            # Initialize collections with lazy-loading safety
            cls._instance.collections = {}
            cls._instance._init_collections()
            
        return cls._instance

    def _init_collections(self):
        """Initializes the standard HIVE-Net collections."""
        try:
            self.collections = {
                "doctrine": self.client.get_or_create_collection(
                    name="cslf_doctrine",
                    metadata={"description": "Legal, Governance & Neuro-Rights"}
                ),
                "trench": self.client.get_or_create_collection(
                    name="cslf_trench",
                    metadata={"description": "Offensive/Defensive Technical Knowledge"}
                ),
                "future": self.client.get_or_create_collection(
                    name="cslf_future",
                    metadata={"description": "PQC, GreenOps & Standards"}
                )
            }
        except Exception as e:
            self.logger.critical(f"COLLECTION_INIT_FAILURE: {e}")

    def get_collection(self, name: str):
        if name not in self.collections:
            # Attempt re-init if not found
            self._init_collections()
            if name not in self.collections:
                raise ValueError(f"Collection '{name}' not found. Use doctrine, trench, or future.")
        return self.collections[name]

    def check_health(self) -> bool:
        """Verifies the vector DB is still alive."""
        try:
            self.client.heartbeat()
            return True
        except Exception:
            return False

chroma_manager = ChromaClient()
