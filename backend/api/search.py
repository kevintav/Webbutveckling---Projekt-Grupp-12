from fastapi import APIRouter, Query
from backend.services.jobs_service import fetch_jobs

router = APIRouter()

@router.get("/search")
def search(
        q: str = Query(..., description="Job title"),
        municipality: str = Query(..., description="Municipality")
):

    return fetch_jobs(q, municipality)


