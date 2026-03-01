import json
import os
import time
from typing import List, Dict, Any

class IncidentLedger:
    """
    Forensic registry for Active Containment events.
    Records every time an agent is paused or killed.
    """
    def __init__(self, storage_path: str = "D:/Cortex-SecLF/data/forensics/incidents.json"):
        self.storage_path = storage_path
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        if not os.path.exists(self.storage_path):
            with open(self.storage_path, 'w') as f:
                json.dump([], f)

    def log_incident(self, agent_id: str, policy: str, breach_type: str, evidence: str, action: str):
        incident = {
            "id": f"INC-{int(time.time())}",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "agent_id": agent_id,
            "policy": policy,
            "breach_type": breach_type,
            "evidence": evidence,
            "action": action
        }
        
        try:
            with open(self.storage_path, 'r+') as f:
                data = json.load(f)
                data.insert(0, incident) # Keep newest first
                f.seek(0)
                json.dump(data[:100], f, indent=2) # Keep last 100
                f.truncate()
        except Exception as e:
            print(f"Failed to log incident: {e}")

    def get_incidents(self) -> List[Dict[str, Any]]:
        try:
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        except:
            return []

incident_ledger = IncidentLedger()
