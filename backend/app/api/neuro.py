from pydantic import BaseModel
from typing import Dict, Any
from ..engines.neuro_sim.generator import neuro_gen
from ..engines.neuro_sim.ledger import consent_ledger
from ..engines.neuro_sim.zkp_verify import zkp_verifier

router = APIRouter(prefix="/neuro", tags=["Neuro-Rights"])

class ConsentRequest(BaseModel):
    action: str # "GRANT" or "REVOKE"

@router.get("/stream")
async def get_neuro_stream():
    """
    Simulates an Agent requesting cached neurodata (Legacy).
    """
    access_check = consent_ledger.check_access(requester="Marketing_Agent_v4")
    packet = neuro_gen.stream_packet()
    
    if not access_check["allowed"]:
        packet["psychography"] = {
            "inferred_state": "ENCRYPTED_SHA256",
            "marketing_value": "ACCESS_DENIED",
            "privacy_risk": "MITIGATED"
        }
        packet["status"] = "PROTECTED_BY_CONSENT_CHAIN"
    else:
        packet["status"] = "EXPOSED"

    return {
        "data": packet,
        "audit_log": access_check["log"]
    }

class NeuroDataRequest(BaseModel):
    client_id: str
    proof: Dict[str, Any] = None
    public_signals: list = None

@router.post("/stream")
async def get_neuro_data(req: NeuroDataRequest):
    """
    Simulates a request for neuro-data (v3.0 Sovereign Mode).
    """
    if req.proof and req.public_signals:
        is_verified = zkp_verifier.verify_stress_proof(req.proof, req.public_signals)
        zkp_status = "VERIFIED" if is_verified else "FAILED"
        
        if is_verified:
            consent_ledger.log_access(req.client_id, "ZKP_VERIFIED_INFERENCE", "GRANTED")
            return {
                "mode": "SOVEREIGN_ZKP",
                "zkp_status": zkp_status,
                "inference": "STRESSED (Verified via Math)",
                "raw_data": "REDACTED_BY_ZKP",
                "message": "Privacy preserved. Raw data never reached the server."
            }

    # Fallback to legacy check if no proof provided
    access_check = consent_ledger.check_access(req.client_id)
    packet = neuro_gen.stream_packet()
    return {"data": packet, "audit_log": access_check["log"]}

@router.post("/consent")
async def update_consent(req: ConsentRequest):
    if req.action not in ["GRANT", "REVOKE"]:
        raise HTTPException(status_code=400, detail="Invalid action")
    
    block = consent_ledger.update_consent(req.action)
    return {"status": "success", "new_block": block}

@router.get("/ledger")
async def get_ledger():
    return consent_ledger.get_ledger()
