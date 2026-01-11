from fastapi import APIRouter, Query
from backend.services.combined_service import fetch_jobs, fetch_combined_jobs

router = APIRouter()


@router.get("/search")
def search(
        q: str = Query(..., description="Job title"),
        municipality: str = Query(..., description="Municipality")
):
    return fetch_jobs(q, municipality)

@router.get("/search/combined")
async def search_combined(
        q: str = Query(..., description="Job title"),
        municipality: str = Query(..., description="Municipality")
):
    result = await fetch_combined_jobs(q, municipality)
    return result