import time
import base64
from typing import Dict, Any
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

class HIVENode:
    """
    Simulates a distributed node in the HIVE-Net consensus network.
    Uses industrial-grade Ed25519 for verifiable digital identities.
    """
    def __init__(self, node_id: str, private_key_hex: str):
        self.node_id = node_id
        # In a real system, keys would be loaded from a secure enclave/TPM
        # Here we derive a stable private key from the provided hex string
        seed = private_key_hex.encode().ljust(32, b'0')[:32]
        self._private_key = ed25519.Ed25519PrivateKey.from_private_bytes(seed)
        self.public_key = self._private_key.public_key()

    def get_public_key_bytes(self) -> bytes:
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )

    def get_fingerprint(self) -> str:
        """Returns a human-readable identifier for the node's public key."""
        pk_bytes = self.get_public_key_bytes()
        return base64.b64encode(pk_bytes).decode('utf-8')

    def sign_block(self, block_hash: str) -> Dict[str, str]:
        """
        Signs a block hash using the node's Ed25519 private key.
        Provides mathematical proof of node identity and data integrity.
        """
        signature = self._private_key.sign(block_hash.encode())
        
        return {
            "node_id": self.node_id,
            "signature": base64.b64encode(signature).decode('utf-8'),
            "fingerprint": self.get_fingerprint(),
            "timestamp": str(time.time()),
            "algo": "Ed25519"
        }

# Pre-defined HIVE nodes with stable seeds
HIVE_NODES = [
    HIVENode("HIVE-ALPHA-01", "SEED_SOVEREIGN_A_99_STABLE_V6"),
    HIVENode("HIVE-BETA-02", "SEED_SOVEREIGN_B_88_STABLE_V6"),
    HIVENode("HIVE-GAMMA-03", "SEED_SOVEREIGN_G_77_STABLE_V6"),
]
