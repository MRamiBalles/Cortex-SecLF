from fastapi import APIRouter, HTTPException
from ..engines.gap_detector.detector import gap_detector
from ..engines.scientist.hive.orchestrator import HiveOrchestrator
from ..engines.rag_engine.crawler import ArchiveCrawler
import asyncio

router = APIRouter(prefix="/bridge", tags=["HIVE Bridge"])
orchestrator = HiveOrchestrator()
crawler = ArchiveCrawler()

@router.post("/auto-patch")
async def trigger_auto_patch():
    """
    Bridge: Detects gaps and automatically spawns a Scientist research cycle.
    """
    stats = gap_detector.analyze_coverage()
    if not stats["missing_topics"]:
        return {"status": "skipped", "reason": "No gaps detected"}
    
    prompt = gap_detector.generate_research_prompt(stats)
    
    # Spawn research in background to not block the API
    asyncio.create_task(orchestrator.execute_complete_cycle(prompt))
    
    return {
        "status": "triggered",
        "target_gaps": [g["topic"] for g in stats["missing_topics"]],
        "research_prompt": prompt
    }

@router.post("/deep-expansion")
async def trigger_deep_expansion(target: str = "MITRE_ATTACK"):
    """
    Bridge: Actively crawls external/internal targets to expand the archive.
    """
    result = crawler.crawl_and_ingest(target)
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return result
