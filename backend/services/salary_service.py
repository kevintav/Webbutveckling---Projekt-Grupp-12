import httpx

PXWEB_V2_URL = (
    "https://statistikdatabasen.scb.se/api/v2/"
    "tables/TAB5932/data"
)

CONTENTS_CODES = [
    "000007CD",  # mean
    "000007CE",  # median
    "000007CF",  # p10
    "000007CG",  # p25
    "000007CH",  # p75
    "000007CI",  # p90
]

async def fetch_salary_distribution(ssyk_2012: str) -> dict:
    params = {
        "lang": "sv",
        "valueCodes[Sektor]": "0",
        "valueCodes[Yrke2012]": ssyk_2012,
        "valueCodes[Tid]": "2024",
        "valueCodes[ContentsCode]": ",".join(CONTENTS_CODES),
        "outputFormat": "json-stat2",
    }

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(PXWEB_V2_URL, params=params)
        response.raise_for_status()
        data = response.json()

    try:
        values = data["value"]

        return {
            "year": 2024,
            "currency": "SEK",
            "mean": int(values[0]),
            "median": int(values[1]),
            "percentiles": {
                "p10": int(values[2]),
                "p25": int(values[3]),
                "p75": int(values[4]),
                "p90": int(values[5]),
            },
            "source": "SCB",
            "table": "TAB5932",
        }

    except (KeyError, IndexError, ValueError):
        return {
            "year": 2024,
            "currency": "SEK",
            "mean": None,
            "median": None,
            "percentiles": {
                "p10": None,
                "p25": None,
                "p75": None,
                "p90": None,
            },
            "source": "SCB",
            "table": "TAB5932",
        }