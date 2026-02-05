from fastapi import APIRouter
from ..engines.gap_detector.detector import gap_detector

router = APIRouter(prefix="/gaps", tags=["Gap Analysis"])

@router.get("/analyze")
async def analyze_gaps():
    """
    Performs a live analysis of the VectorDB to identify knowledge gaps
    and Red/Blue asymmetry.
    """
    stats = gap_detector.analyze_coverage()
    return stats
