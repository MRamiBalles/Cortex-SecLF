import hashlib
import json
import time
from typing import Dict, Any, Optional

class TPMManager:
    """
    Simulates a Trusted Platform Module (TPM 2.0).
    Provides hardware-rooted identity, NVRAM storage, and PCR-based attestation.
    """
    def __init__(self):
        # PCRs (Platform Configuration Registers) - Simulated
        # PCR 0: BIOS / Boot Loader
        # PCR 10: Application State / Agent Integrity
        self.pcrs = {
            "0": "f2e1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0",
            "10": "8a3f7d2e1c0b9a8f7e6d5c4b3a2f1e0d9c8b7a6f"
        }
        
        # NVRAM (Non-Volatile RAM) - Stores node seeds cryptographically
        self.nvram = {
            "HIVE-ALPHA-01": "SEED_TPM_ALPHA_VAULT_77",
            "HIVE-BETA-02": "SEED_TPM_BETA_VAULT_88",
            "HIVE-GAMMA-03": "SEED_TPM_GAMMA_VAULT_99"
        }

    def get_seed(self, node_id: str) -> str:
        """
        Securely retrieves a seed from TPM NVRAM.
        In a real TPM, this would require owner authorization.
        """
        return self.nvram.get(node_id, "DEFAULT_SOVEREIGN_SEED")

    def create_quote(self, nonce: str, pcr_selection: list = ["10"]) -> Dict[str, Any]:
        """
        Generates a TPM Quote: A signed attestation of the current PCR values.
        """
        selected_pcrs = {pcr: self.pcrs[pcr] for pcr in pcr_selection if pcr in self.pcrs}
        
        # Combine PCRs and Nonce into a hashable blob
        pcr_blob = json.dumps(selected_pcrs, sort_keys=True)
        attestation_data = f"{nonce}|{pcr_blob}"
        
        # In a real TPM, the TPM's private Attestation Key (AK) would sign this
        # Here we simulate the signature with a hash
        signature = hashlib.sha256(f"TPM_AK_SIG|{attestation_data}".encode()).hexdigest()
        
        return {
            "quote": attestation_data,
            "signature": signature,
            "pcr_values": selected_pcrs,
            "nonce": nonce,
            "timestamp": time.time(),
            "tpm_version": "2.0_EMULATED"
        }

    def extend_pcr(self, pcr_index: str, data: str):
        """
        Extends a PCR: PCR_new = Hash(PCR_old | Hash(data))
        """
        if pcr_index not in self.pcrs:
            self.pcrs[pcr_index] = "0" * 40
            
        old_val = self.pcrs[pcr_index]
        new_hash = hashlib.sha256(data.encode()).hexdigest()
        extended_val = hashlib.sha256(f"{old_val}{new_hash}".encode()).hexdigest()
        self.pcrs[pcr_index] = extended_val[:40] # Keep it 40 chars for PoC visual

tpm_manager = TPMManager()
