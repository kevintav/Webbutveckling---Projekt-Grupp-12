from fastapi import FastAPI
from backend.api.search import router as search_router

app = FastAPI()
app.include_router(search_router)

@app.get("/")
def root():
    return {"status": "ok"}