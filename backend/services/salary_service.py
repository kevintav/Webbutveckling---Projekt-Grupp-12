import requests

SCB_API_URL = "https://api.scb.se/OV0104/v1/doris/sv/AM/AM0110/AM0110A/LonYrkeRegion4A"


def fetch_salary(ssyk: str, region: str) -> dict:
    payload = {
        "query": [
            {"code": "Yrke2012", "selection": {"filter": "item", "values": [ssyk]}},
            {"code": "Region", "selection": {"filter": "item", "values": [region]}},
            {"code": "ContentsCode", "selection": {"filter": "item", "values": ["000000BW"]}},
        ],
        "response": {"format": "json"}
    }

    response = requests.post(SCB_API_URL, json=payload)
    response.raise_for_status()

    data = response.json()

    try:
        value = data["data"][0]["values"][0]
        return {"average_salary": int(value)}
    except (IndexError, KeyError, ValueError):
        return {"average_salary": None}
