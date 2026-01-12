from fastapi import APIRouter, Query
from backend.services.combined_service import fetch_jobs, fetch_combined_jobs

router = APIRouter()


@router.get("/search")
def search(
        q: str = Query(..., description="Job title"),
        region: str = Query(..., description="Region name, e.g. Skåne, Stockholm")
):
    return fetch_jobs(q, region)

@router.get("/search/combined")
async def search_combined(
        q: str = Query(..., description="Job title"),
        region: str = Query(..., description="Region name, e.g. Skåne, Stockholm")
):
    return await fetch_combined_jobs(q, region)