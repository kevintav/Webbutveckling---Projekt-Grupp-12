from fastapi import APIRouter, Query
from backend.services.jobs_service import fetch_jobs

router = APIRouter()

@router.get("/search")
def search(
        q: str = Query(..., description="Job title"),
        municipality: str = Query(..., description="Municipality")
):

    REGION_MAP = {
        "Skåne": "CaRE_1nn_cSU",
        "Stockholm": "oDpK_oZ2_WYt",
        "Västra Götalands": "zdoY_6u5_Krt",
        "Uppsala": "zBon_eET_fFU",
        "Norrbotten": "9hXe_F4g_eTG",
        "Jönköpings": "MtbE_xWT_eMi",
        "Västmanlands": "G6DV_fKE_Viz",
    }

    region_id = REGION_MAP.get(municipality)

    return fetch_jobs(q, region_id)


