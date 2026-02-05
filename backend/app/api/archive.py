from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional
from .retriever import retriever
from .ingestor import Ingestor
import os

router = APIRouter(prefix="/archive", tags=["Archive"])

class QueryRequest(BaseModel):
    query: str
    collection: str = "doctrine"
    n_results: int = 3
    min_year: Optional[int] = None
    authority: Optional[str] = None
    language: Optional[str] = None

class SearchResult(BaseModel):
    content: str
    source: str
    distance: float
    year: Optional[int]
    authority: Optional[str]
    language: Optional[str]

class QueryResponse(BaseModel):
    results: List[SearchResult]
    context: str
    hallucination_risk: bool

@router.post("/search", response_model=QueryResponse)
async def search_archive(request: QueryRequest):
    if request.collection not in ["doctrine", "trench", "future"]:
        raise HTTPException(status_code=400, detail="Invalid collection")
    
    # Build filters for retriever
    filters = {}
    if request.min_year: filters["year"] = {"$gte": request.min_year}
    if request.authority: filters["authority"] = request.authority
    if request.language: filters["language"] = request.language

    results = retriever.retrieve(request.query, request.collection, request.n_results, filters=filters)
    context = retriever.format_for_prompt(results)
    
    formatted_results = [
        SearchResult(
            content=res['content'],
            source=res['metadata'].get('source', 'Unknown'),
            distance=res['distance'],
            year=res['metadata'].get('year'),
            authority=res['metadata'].get('authority'),
            language=res['metadata'].get('language')
        ) for res in results
    ]
    
    return QueryResponse(
        results=formatted_results,
        context=context,
        hallucination_risk=len(results) == 0
    )

@router.post("/ingest/trigger")
async def trigger_ingestion(background_tasks: BackgroundTasks):
    """
    Triggers the ingestion of local files in the data directory.
    Running in background to avoid timeout.
    """
    def run_ingestion():
        ingestor = Ingestor()
        base_path = "/data/documents"
        ingestor.ingest_directory("doctrine", f"{base_path}/doctrine")
        ingestor.ingest_directory("trench", f"{base_path}/trench")
        ingestor.ingest_directory("future", f"{base_path}/future")
        
    background_tasks.add_task(run_ingestion)
    return {"message": "Ingestion started in background."}
