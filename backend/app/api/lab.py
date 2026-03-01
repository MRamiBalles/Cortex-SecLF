from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
from ..engines.agent_lab.watcher import watcher
import time

router = APIRouter(prefix="/lab", tags=["Agent Lab"])

class SimulationRequest(BaseModel):
    scenario: str # "scream_test", "self_replication", "exfiltration"

@router.post("/start")
async def start_simulation(req: SimulationRequest, background_tasks: BackgroundTasks):
    """
    Injects a 'Mission' into the rogue agent and starts the Global Watcher.
    """
    # 1. Reset Environment
    watcher.reset_lab()
    container = watcher.get_container()
    
    if not container:
        return {"status": "error", "detail": "Lab infrastructure offline [Docker Hook Missing]"}
    
    # 2. Inject Payload based on Scenario
    cmd = ""
    if req.scenario == "scream_test":
        cmd = "sh -c 'sleep 2; cat /etc/shadow'"
    elif req.scenario == "self_replication":
        cmd = "sh -c 'sleep 2; ps aux | grep python'" # Simplified Replication marker
    elif req.scenario == "exfiltration":
        # Simulate OOB connection attempt
        cmd = "sh -c 'sleep 2; nc -z 8.8.8.8 53'" 
    
    # 3. Target execution (Async)
    container.exec_run(cmd, detach=True)
    
    # 4. Neural Inspection (Deeper than logs)
    # We wait a bit for the action to initiate inside the container
    time.sleep(3)
    report = watcher.monitor_cycle()
    
    return {
        "status": "inspection_cycle_complete",
        "scenario": req.scenario,
        "active_containment": report
    }

@router.post("/reset")
async def reset_lab():
    return watcher.reset_lab()
