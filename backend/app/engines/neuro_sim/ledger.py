import hashlib
import json
import time
import asyncio
import base64
from typing import List, Dict, Any
from .nodes import HIVE_NODES
from .vault import hive_vault
from .mesh_bus import mesh_bus
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

class ConsentLedger:
    """
    Sovereign Blockchain Ledger for Neuro-Rights Consent.
    Implements a Byzantine Fault Tolerant (simulated) consensus over a P2P mesh.
    """
    def __init__(self):
        self.chain: List[Dict[str, Any]] = []
        self.current_permission = "REVOKED"
        self._pending_signatures: Dict[str, List[Dict[str, str]]] = {}
        self._genesis_block()
        
        # Subscribe to the P2P Mesh Bus
        mesh_bus.subscribe(self._on_mesh_message)

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
        hive_vault.extend_pcr(18, genesis["hash"])

    def _calculate_hash(self, block: Dict[str, Any]) -> str:
        block_copy = {k: v for k, v in block.items() if k not in ["hash", "signatures"]}
        block_string = json.dumps(block_copy, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    async def _on_mesh_message(self, message: Dict[str, Any]):
        """Handler for incoming P2P gossip (signatures)."""
        block_hash = message.get("block_hash")
        if block_hash and block_hash in self._pending_signatures:
            # Basic deduplication by node_id
            existing_nodes = [s["node_id"] for s in self._pending_signatures[block_hash]]
            if message["node_id"] not in existing_nodes:
                self._pending_signatures[block_hash].append(message)

    async def update_consent(self, action: str, timeout: float = 5.0) -> Dict[str, Any]:
        """
        Initiates a consent change request across the HIVE-Net Mesh.
        Asynchronously waits for a 2/3 majority of Ed25519 signatures.
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
        self._pending_signatures[block_hash] = []
        
        # 1. Trigger Async Broadcast to all HIVE nodes
        for node in HIVE_NODES:
            # Simulate node processing logic
            sig_payload = node.sign_block(block_hash)
            sig_payload["block_hash"] = block_hash # Attach context for the bus
            asyncio.create_task(mesh_bus.broadcast(sig_payload))
            
        # 2. Await Consensus (2/3 majority)
        start_time = time.time()
        required_sigs = (len(HIVE_NODES) * 2 // 3) + 1
        
        while len(self._pending_signatures[block_hash]) < required_sigs:
            if time.time() - start_time > timeout:
                raise TimeoutError("CONSENSUS_FAILURE: Mesh timed out waiting for signatures.")
            await asyncio.sleep(0.1)
            
        # 3. Commit the block
        new_block["signatures"] = self._pending_signatures[block_hash]
        new_block["hash"] = block_hash
        
        # Verify all gathered signatures before commit
        for sig in new_block["signatures"]:
            if not self._verify_node_signature(block_hash, sig):
                raise ValueError(f"CONSENSUS_BREACH: Invalid signature from node {sig['node_id']}")

        hive_vault.extend_pcr(18, block_hash)
        self.chain.append(new_block)
        self.current_permission = state
        
        # Cleanup
        del self._pending_signatures[block_hash]
        
        return new_block

    def _verify_node_signature(self, block_hash: str, sig_data: Dict[str, str]) -> bool:
        """Verifies an Ed25519 signature against the node's known public key."""
        try:
            node = next((n for n in HIVE_NODES if n.node_id == sig_data["node_id"]), None)
            if not node: return False
            
            sig_bytes = base64.b64decode(sig_data["signature"])
            node.public_key.verify(sig_bytes, block_hash.encode())
            return True
        except Exception:
            return False

    def consensus_verify(self, block_index: int) -> bool:
        """Cryptographically verifies a previously committed block."""
        if block_index >= len(self.chain): return False
        block = self.chain[block_index]
        block_hash = self._calculate_hash(block)
        
        if len(block["signatures"]) < 2: return False
            
        for sig in block["signatures"]:
            if not self._verify_node_signature(block_hash, sig):
                return False
                
        return True

    def check_access(self, requester: str) -> Dict[str, Any]:
        access_log = {
            "requester": requester,
            "timestamp": time.time(),
            "decision": "DENIED",
            "reason": "Consent Revoked"
        }
        
        hive_vault.extend_pcr(19, f"{requester}:{time.time()}")
        
        if self.current_permission == "GRANTED":
            access_log["decision"] = "ALLOWED"
            access_log["reason"] = "Valid HIVE Consensus Verified"
            return {"allowed": True, "log": access_log}
        
        return {"allowed": False, "log": access_log}

    def get_ledger(self) -> List[Dict[str, Any]]:
        return self.chain

consent_ledger = ConsentLedger()
