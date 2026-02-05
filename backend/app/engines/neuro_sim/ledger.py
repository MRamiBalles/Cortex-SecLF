import hashlib
import json
import time
from typing import List, Dict, Any

class ConsentLedger:
    def __init__(self):
        self.chain: List[Dict[str, Any]] = []
        self.current_permission = "REVOKED" # Default safe state
        self._genesis_block()

    def _genesis_block(self):
        genesis = {
            "index": 0,
            "timestamp": time.time(),
            "action": "INIT_LEDGER",
            "previous_hash": "0",
            "permission_state": "REVOKED"
        }
        genesis["hash"] = self._calculate_hash(genesis)
        self.chain.append(genesis)

    def _calculate_hash(self, block: Dict[str, Any]) -> str:
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def update_consent(self, action: str) -> Dict[str, Any]:
        """
        GRANT or REVOKE consent. Creates a new immutable block.
        """
        state = "GRANTED" if action == "GRANT" else "REVOKED"
        previous_block = self.chain[-1]
        
        new_block = {
            "index": len(self.chain),
            "timestamp": time.time(),
            "action": action,
            "previous_hash": previous_block["hash"],
            "permission_state": state
        }
        new_block["hash"] = self._calculate_hash(new_block)
        
        self.chain.append(new_block)
        self.current_permission = state
        
        return new_block

    def check_access(self, requester: str) -> Dict[str, Any]:
        """
        Gatekeeper function. Returns True only if latest block is GRANTED.
        """
        # Log the access attempt (Audit Trail)
        access_log = {
            "requester": requester,
            "timestamp": time.time(),
            "decision": "DENIED",
            "reason": "Consent Revoked"
        }
        
        if self.current_permission == "GRANTED":
            access_log["decision"] = "ALLOWED"
            access_log["reason"] = "Valid Consent Found"
            return {"allowed": True, "log": access_log}
        
        return {"allowed": False, "log": access_log}

    def get_ledger(self) -> List[Dict[str, Any]]:
        return self.chain

consent_ledger = ConsentLedger()
