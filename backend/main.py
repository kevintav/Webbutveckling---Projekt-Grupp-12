from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.api.search import router as search_router

app = FastAPI()
app.mount("/static", StaticFiles(directory="frontend"), name="static")

app.include_router(search_router)


@app.get("/")
def serve_frontend():
    return FileResponse("frontend/index.html")
