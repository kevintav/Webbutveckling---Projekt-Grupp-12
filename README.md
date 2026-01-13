# Karriärkollen

Karriärkollen är en webbtjänst som kombinerar platsannonser och lönestatistik från både Arbetsförmedlingen och SCB(Statistikmyndigheten). Användare kan söka efter yrken och få aktuella platsannonser med relevant data för yrke-området.

## Funktionalitet

- Sök efter lediga jobb baserat på:
  - yrketitel i fritext
  - region
- Visa relevanta platsannonser
- Visa lönestatistik för yrkeområdet:
  - genomsnittlig månadlön
  - median
  - lönespridning (10:e, 25:e, 75:e och 90:e percentilen)

## Teknikstacken

### Frontend

- HTML
- CSS
- JavaScript

### Backend

- Python
- FastAPI

## Externa API:er

- Arbetsförmedlingen JobSearch API
  - Offrar aktuella platsannonser för hela Sverige
- SCB PxWebApi 2.0
  - Offrar officiell lönestatistik som tabeller för olika yrken

## Databehandling & Begränsningar

JobTech och SCB använder olika taxonomi för yrken.

För att kunna kombinera data från API:erna så utförs en backend data-mapping mellan 
- JobTechs occupation_group concept_id, exempel -> `rwpH_6RA_XTT`
- SCB ssyk_2012, exempel -> `2146`

Denna mappingen hanteras via en lokal JSON fil som sedan används av backend för att aggregera <br />data från båda API:erna och skickar vidare det till frontend som ett gemensamt svar

OBS! Tjänstens begränsningar beror på att de två API:erna använder olika klassificeringssystem och yrkestitlar för samma underliggande yrke, vilket kräver manuell mappning för att uppnå kompatibilitet.

## Installation & körning

1. Klona github repo
2. Skapa och aktivera venv virtuella python-miljö
3. Installera beroende via pip `pip install -r requirements.txt`
4. Starta FastAPI genom terminalen `fastapi dev backend/main.py`
5. Öppna applikationen via `http://localhost:8000`

### API Dokumentation

Autogenereras av FastAPI och finns tillgänglig via `http://localhost:8000/docs`