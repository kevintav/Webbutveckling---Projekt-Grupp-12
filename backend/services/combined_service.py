from backend.services.jobs_service import fetch_jobs
from backend.services.salary_service import fetch_salary

SCB_REGION_MAP = {
    "Stockholm": "01",
    "Uppsala": "03",
    "Södermanland": "04",
    "Östergötland": "05",
    "Jönköping": "06",
    "Kronoberg": "07",
    "Kalmar": "08",
    "Gotland": "09",
    "Blekinge": "10",
    "Skåne": "12",
    "Halland": "13",
    "Västra Götaland": "14",
    "Värmland": "17",
    "Örebro": "18",
    "Västmanland": "19",
    "Dalarna": "20",
    "Gävleborg": "21",
    "Västernorrland": "22",
    "Jämtland": "23",
    "Västerbotten": "24",
    "Norrbotten": "25"
}


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

    scb_region = SCB_REGION_MAP.get(municipality)
    if not scb_region:
        return []

    combined = []

    for job in jobs:
        ssyk = job.get("ssyk")

        salary_value = None
        if ssyk:
            salary_data = fetch_salary(ssyk, scb_region)
            salary_value = salary_data.get("average_salary")

        combined.append({
            "title": job.get("title"),
            "employer": job.get("employer"),
            "location": f'{job.get("location", {}).get("municipality")}, {job.get("location", {}).get("region")}',
            "workload": workload_scope(job.get("scope_of_work")),
            "salary": salary_value,
            "url": job.get("webpage_url")
        })

    return combined
