import requests

JOBSEARCH_API_URL = "https://jobsearch.api.jobtechdev.se/search"

def fetch_jobs(query: str, region: str):
    params = {
        "q": query,
        "region": region,
        "limit": 10
    }

    response = requests.get(JOBSEARCH_API_URL, params=params)

    response.raise_for_status()

    data = response.json()

    jobs = []

    for job in data.get("jobs", []):
        jobs.append({
            "title": job.get("headline"),
            "employer": job.get("employer", {}).get("name"),
            "location": job.get("workplace_address", {}).get("municipality"),
            "ssyk": job.get("occupation", {}).get("concept_id"),
        })

    return jobs
