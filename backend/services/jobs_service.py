import datetime

import requests
import json
from pathlib import Path

JOBSEARCH_API_URL = "https://jobsearch.api.jobtechdev.se/search"

BASE_DIR = Path(__file__).resolve().parent.parent
REGION_MAP_FILE = BASE_DIR / "config" / "regions.json"

with REGION_MAP_FILE.open(encoding="utf-8") as f:
    REGION_MAP = json.load(f)


def fetch_jobs(query: str, region_name: str):
    region_concept_id = REGION_MAP.get(region_name)

    params = {
        "q": query,
        "limit": 10,
        "region_concept_id": region_concept_id
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
            "scope_of_work": job.get("scope_of_work"),
            "Working_hours_type": job.get("working_hours_type"),
            "published": job.get("timestamp"),
            "url": job.get("webpage_url"),
            "ssyk": job.get("occupation_group", {}).get("concept_id")
        })

    return jobs

def extract_requirements(job: dict):
    must_have = job.get("must_have", {})
    nice_to_have = job.get("nice_to_have", {})

    return {
        "must_have": {
            "skills": must_have.get("skills", []),
            "languages": must_have.get("languages", []),
            "work_experiences": must_have.get("work_experiences", []),
            "education": must_have.get("education", []),
            "education_level": must_have.get("education_level", [])
        },
        "nice_to_have": {
            "skills": nice_to_have.get("skills", []),
            "languages": nice_to_have.get("languages", []),
            "work_experiences": nice_to_have.get("work_experiences", []),
            "education": nice_to_have.get("education", []),
            "education_level": nice_to_have.get("education_level", [])
        }
    }

def extract_contacts(job: dict):
    contacts = []

    for contact in job.get("application_contacts", []):
        contacts.append({
            "name": contact.get("name"),
            "email": contact.get("email"),
            "telephone": contact.get("telephone"),
            "role": contact.get("contact_type"),
            "description": contact.get("description")
        })

    return contacts

def extract_scope_of_work(job: dict):
    scope = job.get("scope_of_work", {})

    return {
        "min": scope.get("min"),
        "max": scope.get("max")
    }

def extract_employment_type(job: dict):
    emp = job.get("employment_type", {})

    return {
        "concept_id": emp.get("concept_id"),
        "label": emp.get("label")
    }

def fetch_job_details(job: dict):
    return {
        "requirements": extract_requirements(job),
        "contacts": extract_contacts(job),
        "scope_of_work": extract_scope_of_work(job),
        "employment_type": extract_employment_type(job),
        "logo_url": job.get("logo_url")
    }
