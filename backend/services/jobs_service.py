import requests

JOBSEARCH_API_URL = "https://jobsearch.api.jobtechdev.se/search"

REGION_MAP = {
        "Skåne": "CaRE_1nn_cSU",
        "Stockholm": "oDpK_oZ2_WYt",
        "Västra Götalands": "zdoY_6u5_Krt",
        "Uppsala": "zBon_eET_fFU",
        "Norrbotten": "9hXe_F4g_eTG",
        "Jönköpings": "MtbE_xWT_eMi",
        "Västmanlands": "G6DV_fKE_Viz",
    }

def fetch_jobs(query: str, municipality: str):
    params = {
        "q": query,
        "region": REGION_MAP.get(municipality),
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
