import requests

PXWEB_V2_URL = (
    "https://statistikdatabasen.scb.se/api/v2/"
    "tables/TAB5932/data"
)

def fetch_salary(ssyk_2012: str) -> dict:
    params = {
        "lang": "en",
        "valueCodes[ContentsCode]": "000007CD",
        "valueCodes[Sektor]": "0",
        "valueCodes[Yrke2012]": ssyk_2012,
        "valueCodes[Kon]": "1,2,1+2",
        "valueCodes[Tid]": "2024",
        "outputFormat": "json-stat2",
    }

    response = requests.get(PXWEB_V2_URL, params=params)
    response.raise_for_status()

    data = response.json()

    try:
        return {"average_salary": int(data["value"][0])}
    except (KeyError, IndexError, ValueError):
        return {"average_salary": None}

