from typing import List, Dict, Any
from ..rag_engine.chroma_client import chroma_manager
import datetime

# Simplified MITRE / OWASP Reference for Baseline Comparison
MITRE_REFERENCE = {
    "SQL Injection": {"id": "T1190", "keywords": ["sqli", "sql injection", "union select", "database error"]},
    "XXE": {"id": "T1612", "keywords": ["xxe", "xml external entity", "dtd"]},
    "SSRF": {"id": "T1190", "keywords": ["ssrf", "server side request forgery"]},
    "Buffer Overflow": {"id": "T1203", "keywords": ["buffer overflow", "stack overflow", "rop chain", "eip"]},
    "Cross-Site Scripting": {"id": "T1059", "keywords": ["xss", "cross-site scripting"]},
    "Neuro-Rights": {"id": "N/A", "keywords": ["neurodata", "brain-computer interface", "mental privacy", "neurorights"]},
    "Agent Control": {"id": "N/A", "keywords": ["kill-switch", "agent containment", "ai safety", "alignment"]}
}

class GapDetector:
    def __init__(self):
        self.client = chroma_manager
        
    def _is_offensive(self, text: str) -> bool:
        offensive_terms = ["exploit", "poc", "attack", "payload", "shell", "reverse connection", "bypass"]
        return any(term in text.lower() for term in offensive_terms)

    def _is_defensive(self, text: str) -> bool:
        defensive_terms = ["mitigation", "patch", "defense", "detection", "rule", "harden", "prevention", "sigma", "yara"]
        return any(term in text.lower() for term in defensive_terms)

    def analyze_coverage(self) -> Dict[str, Any]:
        """
        Scans the 'trench' and 'doctrine' collections to build a heatmap of coverage.
        Returns statistics on Red vs Blue balance and Missing Topics.
        """
        # We'll simple-scan a subset or all documents (Chroma get())
        # For production, this should be optimized. Here we fetch metadata.
        
        collections_to_scan = ["trench", "doctrine"]
        
        stats = {
            "total_docs": 0,
            "red_blue_balance": {"red": 0, "blue": 0, "neutral": 0},
            "topic_coverage": {topic: 0 for topic in MITRE_REFERENCE.keys()},
            "temporal_distribution": {}, # Year -> Count
            "missing_topics": []
        }

        all_docs = []
        for col_name in collections_to_scan:
            try:
                col = self.client.get_collection(col_name)
                # Fetch all metadata and small content preview. 
                # Limit to 500 for performance in this "Step-by-Step" simulation
                data = col.get(include=["metadatas", "documents"], limit=500) 
                
                if data["ids"]:
                    for i, doc_text in enumerate(data["documents"]):
                        meta = data["metadatas"][i]
                        stats["total_docs"] += 1
                        
                        # Temporal Analysis
                        year = meta.get("year", "Unknown")
                        if year != "Unknown":
                            stats["temporal_distribution"][year] = stats["temporal_distribution"].get(year, 0) + 1
                        
                        # Red/Blue Analysis
                        is_red = self._is_offensive(doc_text)
                        is_blue = self._is_defensive(doc_text)
                        
                        if is_red and not is_blue: stats["red_blue_balance"]["red"] += 1
                        elif is_blue and not is_red: stats["red_blue_balance"]["blue"] += 1
                        else: stats["red_blue_balance"]["neutral"] += 1
                        
                        # Topic Analysis
                        for topic, info in MITRE_REFERENCE.items():
                            if any(k in doc_text.lower() for k in info["keywords"]):
                                stats["topic_coverage"][topic] += 1
            except Exception as e:
                print(f"Error scanning collection {col_name}: {e}")

        # Determine Gaps
        for topic, count in stats["topic_coverage"].items():
            if count < 3: # Arbitrary threshold for "Gap"
                stats["missing_topics"].append({
                    "topic": topic,
                    "count": count,
                    "status": "CRITICAL GAP" if count == 0 else "LOW COVERAGE"
                })

        return stats

gap_detector = GapDetector()
