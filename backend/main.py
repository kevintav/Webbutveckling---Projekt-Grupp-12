import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from backend.api.search import router as search_router

app = FastAPI()
app.include_router(search_router)

@app.get("/")
def root():
    file_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    return FileResponse(file_path)