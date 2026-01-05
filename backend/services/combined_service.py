from backend.services.jobs_service import fetch_jobs
from backend.services.salary_service import fetch_salary
from backend.services.ssyk_map import JOBTECH_TO_SSYK

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


def fetch_combined_jobs(query: str, municipality: str) -> list[dict]:
    jobs = fetch_jobs(query, municipality)
    combined = []

    for job in jobs:
        jobtech_id = job.get("ssyk")
        ssyk_code = JOBTECH_TO_SSYK.get(jobtech_id)

        salary = None
        if ssyk_code is not None:
            try:
                salary = fetch_salary(ssyk_code).get("average_salary")
            except Exception:
                salary = None

        combined.append({
            "title": job.get("title"),
            "employer": job.get("employer"),
            "location": f"{job.get('location', {}).get('municipality')}, "
                        f"{job.get('location', {}).get('region')}",
            "workload": workload_scope(job.get("scope_of_work")),
            "salary": salary,
            "url": job.get("webpage_url"),
            "ssyk": job.get("ssyk"),
        })

    return combined
