from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..engines.scientist.lab_coat import lab_coat
from ..engines.scientist.peer_review import peer_reviewer

router = APIRouter(prefix="/scientist", tags=["AI Scientist"])

class ResearchRequest(BaseModel):
    topic: str

@router.post("/research")
async def conduct_autonomous_research(req: ResearchRequest):
    """
    Triggers the Autonomous Research Loop:
    1. Scientist generates Hypothesis and Experiment.
    2. Scientist (Simulated) executes Experiment.
    3. Peer Reviewer critiques the findings.
    """
    if not req.topic:
        raise HTTPException(status_code=400, detail="Topic required")

    # 1. Research Phase
    research_artifact = lab_coat.conduct_research(req.topic)
    
    # 2. Review Phase
    review_artifact = peer_reviewer.review_research(research_artifact)

    return {
        "status": "completed",
        "paper": research_artifact,
        "review": review_artifact
    }
