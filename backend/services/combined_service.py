import json
from pathlib import Path

from backend.services.jobs_service import fetch_jobs
from backend.services.salary_service import fetch_salary
import asyncio

BASE_DIR = Path(__file__).resolve().parent.parent
SSYK_MAP_FILE = BASE_DIR / "config" / "ssyk_to_occupation_group.json"

with SSYK_MAP_FILE.open(encoding="utf-8") as f:
    SSYK_MAP = json.load(f)

_salary_cache: dict[str, int | None] = {}

def workload_scope(scope: dict | None) -> str | None:
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
    combined = []

    async def get_salary(ssyk_code: str | None) -> int | None:
        if not ssyk_code:
            return None
        if ssyk_code in _salary_cache:
            return _salary_cache[ssyk_code]
        try:
            salary_data = await fetch_salary(ssyk_code)
            salary = salary_data.get("average_salary")
            _salary_cache[ssyk_code] = salary
            return salary
        except Exception:
            _salary_cache[ssyk_code] = None
            return None

    tasks = [get_salary(SSYK_MAP.get(job.get("ssyk"))) for job in jobs]
    salaries = await asyncio.gather(*tasks)

    for job, salary in zip(jobs, salaries):
        combined.append({
            "title": job.get("title"),
            "employer": job.get("employer"),
            "location": f"{job.get('location', {}).get('municipality')}, "
                        f"{job.get('location', {}).get('region')}",
            "workload": workload_scope(job.get("scope_of_work")),
            "salary": salary,
            "url": job.get("url"),
            "ssyk": job.get("ssyk"),
        })

    return combined