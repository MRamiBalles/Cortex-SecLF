from typing import List, Dict, Any, Optional
from .chroma_client import chroma_manager
import os

class StrictRetriever:
    def __init__(self, threshold: float = 0.4):
        """
        Threshold: distance in vector space. 
        In Chroma (l2), lower is better. 
        0.4 is a strict cut-off for 'Ground Truth'.
        """
        self.threshold = threshold

    def retrieve(self, query: str, collection_name: str, n_results: int = 5) -> List[Dict[str, Any]]:
        collection = chroma_manager.get_collection(collection_name)
        
        results = collection.query(
            query_texts=[query],
            n_results=n_results,
            include=["documents", "metadatas", "distances"]
        )
        
        filtered_results = []
        
        if not results['documents']:
            return []

        # Iterate through results and apply threshold
        # Chroma format: results['documents'][0] is the list of docs for the first query
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
            source = res['metadata'].get('source', 'Unknown')
            context += f"SOURCE {i+1} [{source}]:\n{res['content']}\n\n"
        context += "--- CANONICAL SOURCES END ---"
        return context

retriever = StrictRetriever()
