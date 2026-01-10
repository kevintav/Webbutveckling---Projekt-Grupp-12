import json
from pathlib import Path

from backend.services.jobs_service import fetch_jobs
from backend.services.salary_service import fetch_salary

BASE_DIR = Path(__file__).resolve().parent.parent
SSYK_MAP_FILE = BASE_DIR / "config" / "ssyk_to_occupation_group.json"

with SSYK_MAP_FILE.open(encoding="utf-8") as f:
    SSYK_MAP = json.load(f)

def fetch_combined_jobs(query: str, municipality: str) -> list[dict]:
    jobs = fetch_jobs(query, municipality)
    combined = []

    for job in jobs:
        occupation_group_concept_id = job.get("ssyk")
        ssyk_2012 = SSYK_MAP.get(occupation_group_concept_id)

        salary = None
        if ssyk_2012:
            try:
                salary = fetch_salary(ssyk_2012).get("average_salary")
            except Exception:
                salary = None

        combined.append({
            "title": job.get("title"),
            "employer": job.get("employer"),
            "location": f"{job.get('location', {}).get('municipality')}, "
                        f"{job.get('location', {}).get('region')}",
            "salary": salary,
            "url": job.get("url"),
            "ssyk": occupation_group_concept_id,
        })

    return combined
