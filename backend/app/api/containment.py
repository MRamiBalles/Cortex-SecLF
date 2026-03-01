from fastapi import APIRouter, HTTPException
from ..engines.policy_engine.engine import policy_engine
from ..engines.agent_lab.incident_ledger import incident_ledger
from pydantic import BaseModel
from typing import List, Dict, Any

router = APIRouter(prefix="/containment", tags=["Containment"])

class PolicyUpdate(BaseModel):
    policy: str

@router.get("/policy")
async def get_policy():
    """Returns the currently active security policy."""
    return {
        "active_policy": policy_engine.current_policy_name,
        "details": policy_engine.get_current_policy(),
        "available_policies": list(policy_engine.POLICIES.keys())
    }

@router.post("/policy")
async def update_policy(data: PolicyUpdate):
    """Updates the active security policy."""
    success = policy_engine.set_policy(data.policy)
    if not success:
        raise HTTPException(status_code=400, detail="Invalid policy name")
    return {"status": "success", "new_policy": data.policy}

@router.get("/incidents")
async def get_incidents():
    """Returns the forensic incident log."""
    return {
        "incidents": incident_ledger.get_incidents(),
        "total_count": len(incident_ledger.get_incidents())
    }
