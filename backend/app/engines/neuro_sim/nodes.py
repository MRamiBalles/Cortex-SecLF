import hashlib
import time
from typing import Dict, Any

class HIVENode:
    """
    Simulates a distributed node in the HIVE-Net consensus network.
    Each node has its own identity and signs consensus blocks.
    """
    def __init__(self, node_id: str, secret_key: str):
        self.node_id = node_id
        self.secret_key = secret_key

    def sign_block(self, block_hash: str) -> Dict[str, str]:
        """
        Calculates a signature for a block hash using the node's secret key.
        In a real system, this would use Ed25519 or similar.
        """
        signature_material = f"{block_hash}:{self.secret_key}:{self.node_id}"
        signature = hashlib.sha256(signature_material.encode()).hexdigest()
        
        return {
            "node_id": self.node_id,
            "signature": signature,
            "timestamp": str(time.time())
        }

# Pre-defined trusted HIVE nodes for the PoC
HIVE_NODES = [
    HIVENode("HIVE-ALPHA-01", "K_SOVEREIGN_A_99"),
    HIVENode("HIVE-BETA-02", "K_SOVEREIGN_B_88"),
    HIVENode("HIVE-GAMMA-03", "K_SOVEREIGN_G_77"),
]
