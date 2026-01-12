from backend.services.jobs_service import fetch_jobs
from backend.services.salary_service import fetch_salary
from pathlib import Path
import asyncio
import json
from typing import Optional

BASE_DIR = Path(__file__).resolve().parent.parent
SSYK_MAP_FILE = BASE_DIR / "config" / "ssyk_to_occupation_group.json"

with SSYK_MAP_FILE.open(encoding="utf-8") as f:
    SSYK_MAP: dict[str, str] = json.load(f)

_salary_cache: dict[str, Optional[int]] = {}


def workload_scope(scope: dict | None) -> str:
    if not scope:
        return "Unknown"

    min_pct = scope.get("min")
    max_pct = scope.get("max")

    if min_pct == 100 and max_pct == 100:
        return "Full-time"
    if max_pct is not None and max_pct < 100:
        return "Part-time"
    if min_pct is not None and max_pct is not None:
        return "Variable"

    return "Unknown"


async def fetch_combined_jobs(query: str, municipality: str) -> list[dict]:
    jobs = fetch_jobs(query, municipality)
    combined: list[dict] = []

    async def get_salary_for_job(job: dict) -> Optional[int]:

        occupation_id = job.get("ssyk")
        ssyk_2012 = SSYK_MAP.get(occupation_id)

        if not ssyk_2012:
            return None

        if ssyk_2012 in _salary_cache:
            return _salary_cache[ssyk_2012]

        try:
            salary_data = await fetch_salary(ssyk_2012)
            salary = salary_data.get("average_salary")
            _salary_cache[ssyk_2012] = salary
            return salary
        except Exception:
            _salary_cache[ssyk_2012] = None
            return None


    salary_tasks = [get_salary_for_job(job) for job in jobs]
    salaries = await asyncio.gather(*salary_tasks)

    for job, salary in zip(jobs, salaries):
        combined.append({
            "title": job.get("title"),
            "employer": job.get("employer"),
            "location": (
                f"{job.get('location', {}).get('municipality')}, "
                f"{job.get('location', {}).get('region')}"
            ),
            "salary": salary,
            "url": job.get("url"),
            "ssyk": job.get("ssyk"),
        })

    return combined
