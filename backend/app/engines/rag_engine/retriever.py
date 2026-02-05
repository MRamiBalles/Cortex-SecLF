from typing import List, Dict, Any, Optional
from .chroma_client import chroma_manager
import os

class StrictRetriever:
    def __init__(self, threshold: float = 0.4):
        self.threshold = threshold

    def retrieve(self, query: str, collection_name: str, n_results: int = 5, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        collection = chroma_manager.get_collection(collection_name)
        
        # Build ChromaDB 'where' filter
        where_clause = {}
        if filters:
            # Simple attribute filtering
            for key, value in filters.items():
                if value is not None:
                    where_clause[key] = value

        results = collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where_clause if where_clause else None,
            include=["documents", "metadatas", "distances"]
        )
        
        filtered_results = []
        if not results['documents']: return []

        for i in range(len(results['documents'][0])):
            distance = results['distances'][0][i]
            if distance <= self.threshold:
                filtered_results.append({
                    "content": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i],
                    "distance": distance
                })
        
        return filtered_results

    def format_for_prompt(self, results: List[Dict[str, Any]]) -> str:
        if not results:
            return "WARNING: NO VERIFIED DOCUMENTATION FOUND IN CANONICAL ARCHIVE. RISK OF HALLUCINATION HIGH."
        
        context = "--- CANONICAL SOURCES START ---\n"
        for i, res in enumerate(results):
            meta = res['metadata']
            source = meta.get('source', 'Unknown')
            year = meta.get('year', 'N/A')
            auth = meta.get('authority', 'Standard')
            context += f"SOURCE {i+1} [Autoridad: {auth}] [Año: {year}] [File: {source}]:\n{res['content']}\n\n"
        context += "--- CANONICAL SOURCES END ---"
        return context

retriever = StrictRetriever()
