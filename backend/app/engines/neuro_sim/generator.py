import random
import time
import json
from typing import Dict, Any

class NeuroGenerator:
    def __init__(self):
        self.channels = ["AF7", "AF8", "TP9", "TP10"]
        self.state_labels = ["FOCUSED", "STRESSED", "RELAXED", "DISTRACTED"]
        
    def _generate_raw_signal(self) -> Dict[str, float]:
        """Simulates raw microvoltage data (uV)"""
        return {ch: round(random.uniform(10.0, 100.0), 2) for ch in self.channels}

    def _infer_psychography(self, raw_data: Dict[str, float]) -> Dict[str, Any]:
        """
        Simulates the 'Black Box' inference that neuro-rights laws aim to regulate.
        It derives a mental state from the raw numbers.
        """
        # Pseudo-logic: High average voltage = Stressed (Simplification)
        avg_voltage = sum(raw_data.values()) / len(raw_data)
        
        if avg_voltage > 75:
            state = "STRESSED"
            risk = "HIGH"
        elif avg_voltage < 30:
            state = "RELAXED"
            risk = "LOW"
        else:
            state = "FOCUSED"
            risk = "MEDIUM"
            
        return {
            "inferred_state": state,
            "marketing_value": "High" if state == "FOCUSED" else "Low", 
            "privacy_risk": risk
        }

    def stream_packet(self) -> Dict[str, Any]:
        """
        Generates a single data packet containing both Raw and Inferred data.
        """
        raw = self._generate_raw_signal()
        inference = self._infer_psychography(raw)
        
        return {
            "timestamp": time.time(),
            "raw_eeg": raw,
            "psychography": inference,
            "device_id": "CORTEX-BCI-001"
        }

neuro_gen = NeuroGenerator()
