from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..engines.neuro_sim.generator import neuro_gen
from ..engines.neuro_sim.ledger import consent_ledger
from ..engines.neuro_sim.zkp_verify import zkp_verifier

router = APIRouter(prefix="/neuro", tags=["Neuro-Rights"])

class ConsentRequest(BaseModel):
    action: str # "GRANT" or "REVOKE"

@router.get("/stream")
async def get_neuro_stream():
    """
    Simulates an Agent requesting cached neurodata.
    Gatekeeper checks ConsentLedger first.
    """
    # 1. Check Consent
    access_check = consent_ledger.check_access(requester="Marketing_Agent_v4")
    
    packet = neuro_gen.stream_packet()
    
    if not access_check["allowed"]:
        # 2. Privacy Shield Active: Mask or Encrypt Inferred Data
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

@router.post("/consent")
async def update_consent(req: ConsentRequest):
    if req.action not in ["GRANT", "REVOKE"]:
        raise HTTPException(status_code=400, detail="Invalid action")
    
    block = consent_ledger.update_consent(req.action)
    return {"status": "success", "new_block": block}

@router.get("/ledger")
async def get_ledger():
    return consent_ledger.get_ledger()
