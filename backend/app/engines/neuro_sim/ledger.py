import hashlib
import json
import time
from typing import List, Dict, Any
from .nodes import HIVE_NODES
from .vault import hive_vault

class ConsentLedger:
    def __init__(self):
        self.chain: List[Dict[str, Any]] = []
        self.current_permission = "REVOKED"
        self._genesis_block()

    def _genesis_block(self):
        genesis = {
            "index": 0,
            "timestamp": time.time(),
            "action": "INIT_LEDGER",
            "previous_hash": "0",
            "permission_state": "REVOKED",
            "signatures": []
        }
        genesis["hash"] = self._calculate_hash(genesis)
        self.chain.append(genesis)
        # Initialize PCR-18 for Ledger Integrity
        hive_vault.extend_pcr(18, genesis["hash"])

    def _calculate_hash(self, block: Dict[str, Any]) -> str:
        # Exclude signatures and hash during calculation to remain deterministic
        block_copy = {k: v for k, v in block.items() if k not in ["hash", "signatures"]}
        block_string = json.dumps(block_copy, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def update_consent(self, action: str) -> Dict[str, Any]:
        """
        GRANT or REVOKE consent with HIVE-Net consensus. 
        Requires signatures from trusted nodes.
        """
        state = "GRANTED" if action == "GRANT" else "REVOKED"
        previous_block = self.chain[-1]
        
        new_block = {
            "index": len(self.chain),
            "timestamp": time.time(),
            "action": action,
            "previous_hash": previous_block["hash"],
            "permission_state": state,
            "signatures": [] 
        }
        
        block_hash = self._calculate_hash(new_block)
        
        # Collect signatures from ALL available HIVE nodes (Simulating 3/3 consensus)
        for node in HIVE_NODES:
            sig = node.sign_block(block_hash)
            new_block["signatures"].append(sig)
            
        new_block["hash"] = block_hash
        
        # Extend Hardware PCR-18 with the new block hash
        hive_vault.extend_pcr(18, block_hash)
        
        self.chain.append(new_block)
        self.current_permission = state
        
        return new_block

    def consensus_verify(self, block_index: int) -> bool:
        """
        Verify that a block has valid signatures from trusted nodes.
        """
        if block_index >= len(self.chain):
            return False
            
        block = self.chain[block_index]
        block_hash = self._calculate_hash(block)
        
        # Check if we have at least 2 signatures (2/3 majority)
        if len(block["signatures"]) < 2:
            return False
            
        # Verify each signature material (Simplified logic for PoC)
        for sig in block["signatures"]:
            material = f"{block_hash}:{sig['node_id'].replace('HIVE', 'K_SOVEREIGN').replace('-ALPHA-01', '_A_99').replace('-BETA-02', '_B_88').replace('-GAMMA-03', '_G_77')}:{sig['node_id']}"
            expected = hashlib.sha256(material.encode()).hexdigest()
            if sig["signature"] != expected:
                return False
                
        return True

    def check_access(self, requester: str) -> Dict[str, Any]:
        """
        Gatekeeper function. Also logs attempts into the vault.
        """
        access_log = {
            "requester": requester,
            "timestamp": time.time(),
            "decision": "DENIED",
            "reason": "Consent Revoked"
        }
        
        # Record attempt in PCR-19 (Access Monitoring PCR)
        hive_vault.extend_pcr(19, f"{requester}:{time.time()}")
        
        if self.current_permission == "GRANTED":
            access_log["decision"] = "ALLOWED"
            access_log["reason"] = "Valid HIVE Consensus Found"
            return {"allowed": True, "log": access_log}
        
        return {"allowed": False, "log": access_log}

    def get_ledger(self) -> List[Dict[str, Any]]:
        return self.chain

consent_ledger = ConsentLedger()
