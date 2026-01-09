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
    "Östergötlands": "oLT3_Q9p_3nn",
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

    jobs_list = []

    for job in data.get("hits", []):
        must_have = job.get("must_have", {})
        nice_to_have = job.get("nice_to_have", {})

        contacts = []
        for contact in job.get("application_contacts", []):
            contacts.append({
                "name": contact.get("name"),
                "description": contact.get("description"),
                "email": contact.get("email"),
                "telephone": contact.get("telephone"),
                "contact_type": contact.get("contact_type")
            })

        jobs_list.append({
            "title": job.get("headline"),
            "employer": job.get("employer", {}).get("name"),
            "location": {
                "municipality": job.get("workplace_address", {}).get("municipality"),
                "region": job.get("workplace_address", {}).get("region")
            },
            "logo_url": job.get("logo_url"),
            "webpage_url": job.get("webpage_url"),
            "scope_of_work": {
                "min": job.get("scope_of_work", {}).get("min"),
                "max": job.get("scope_of_work", {}).get("max")
            },
            "ssyk": job.get("occupation", {}).get("concept_id"),
            "timestamp": job.get("timestamp"),
            "employment_type": {
                "concept_id": job.get("employment_type", {}).get("concept_id"),
                "label": job.get("employment_type", {}).get("label")
            },

            "must_have_skills": must_have.get("skills", []),
            "must_have_languages": must_have.get("languages", []),
            "must_have_work_experiences": must_have.get("work_experiences", []),
            "must_have_education": must_have.get("education", []),
            "must_have_education_level": must_have.get("education_level", []),

            "nice_to_have_skills": nice_to_have.get("skills", []),
            "nice_to_have_languages": nice_to_have.get("languages", []),
            "nice_to_have_work_experiences": nice_to_have.get("work_experiences", []),
            "nice_to_have_education": nice_to_have.get("education", []),
            "nice_to_have_education_level": nice_to_have.get("education_level", []),

            "contacts": contacts
        })

    return jobs_list
