import requests

JOBSEARCH_API_URL = "https://jobsearch.api.jobtechdev.se/search"

def fetch_jobs(query: str, municipality: str):
    params = {
        "q": query,
        "region": municipality,
        "limit": 10
    }

    response = requests.get(JOBSEARCH_API_URL, params=params)

    response.raise_for_status()

    data = response.json()

    jobs = []

    for job in data.get("hits", []):
        jobs.append({
            "title": job.get("headline"),
            "employer": job.get("employer", {}).get("name"),
            "location": {
                    "municipality": job.get("workplace_address", {}).get("municipality"),
                    "region": job.get("workplace_address", {}).get("region"),
                },
            "ssyk": job.get("occupation", {}).get("concept_id"),
        })

    return jobs
