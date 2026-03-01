import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.engines.rag_engine.ingestor import Ingestor
from app.engines.rag_engine.chroma_client import chroma_manager

def verify_seeding():
    print("--- CORTEX-SEC RAG TEST: Ingestion Verification ---")
    
    ingestor = Ingestor()
    # Use real local paths for testing outside container
    base_data_path = "data/documents"
    
    print("Ingesting Doctrine...")
    ingestor.ingest_directory("doctrine", os.path.join(base_data_path, "doctrine"))
    
    print("Ingesting Trench...")
    ingestor.ingest_directory("trench", os.path.join(base_data_path, "trench"))
    
    print("\nVerifying retrieval...")
    collection = chroma_manager.get_collection("doctrine")
    results = collection.query(query_texts=["Watcher Paradox"], n_results=1)
    
    if results["documents"][0]:
        print(f"SUCCESS: Found document containing: {results['documents'][0][0][:50]}...")
    else:
        print("FAILURE: Document not found in collection.")

if __name__ == "__main__":
    # Ensure directories exists for the test script
    # (They should exist from previous steps)
    verify_seeding()
