from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..engines.dojo_ctrl.manager import dojo_manager

router = APIRouter(prefix="/dojo", tags=["Dojo Control"])

class LabActionRequest(BaseModel):
    lab_id: str

@router.get("/labs")
async def get_labs():
    """
    Returns the list of all available vulnerable labs.
    """
    return dojo_manager.list_labs()

@router.post("/start")
async def start_lab(req: LabActionRequest):
    """
    Spins up a new instance of a vulnerable laboratory.
    """
    result = dojo_manager.start_lab(req.lab_id)
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["msg"])
    return result

@router.post("/stop")
async def stop_lab(req: LabActionRequest):
    """
    Terminates and removes a specific lab instance.
    """
    result = dojo_manager.stop_lab(req.lab_id)
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["msg"])
    return result

@router.get("/status/{lab_id}")
async def get_lab_status(lab_id: str):
    """
    Returns current container status for a specific lab.
    """
    return dojo_manager.get_status(lab_id)
