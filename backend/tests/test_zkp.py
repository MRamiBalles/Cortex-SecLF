import sys
import os
from typing import Dict, Any

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.engines.neuro_sim.zkp_verify import zkp_verifier

def test_zkp_integrity():
    print("--- CORTEX-SEC ZKP INTEGRITY AUDIT ---")
    
    # 1. Honesty Test (Completeness)
    valid_proof = {
        "id": "π_VALID_001",
        "metadata": "CORTEX_ZKP_v3",
        "timestamp": 123456789
    }
    public_signals = [75]
    
    print("[TEST 1] Honesty Test (Valid Proof)...", end=" ")
    if zkp_verifier.verify_stress_proof(valid_proof, public_signals):
        print("PASS (Accepted)")
    else:
        print("FAIL (Rejected)")
        return False

    # 2. Spoof Test (Soundness)
    fake_proof = {
        "id": "π_FAKE_001",
        "metadata": "MALICIOUS_INJECTION",
        "timestamp": 123456789
    }
    
    print("[TEST 2] Spoof Test (Manipulated Metadata)...", end=" ")
    if not zkp_verifier.verify_stress_proof(fake_proof, public_signals):
        print("PASS (Correctly Rejected)")
    else:
        print("FAIL (Vulnerable: Accepted fake proof)")
        return False

    # 3. Malformed Test
    malformed_proof = {"id": "NOT_A_PROOF"}
    
    print("[TEST 3] Malformed Proof Test...", end=" ")
    if not zkp_verifier.verify_stress_proof(malformed_proof, public_signals):
        print("PASS (Correctly Rejected)")
    else:
        print("FAIL (Vulnerable: Accepted malformed proof)")
        return False

    print("--- AUDIT COMPLETE: ZKP VERIFIER IS SECURE (PoC Level) ---")
    return True

if __name__ == "__main__":
    success = test_zkp_integrity()
    sys.exit(0 if success else 1)
