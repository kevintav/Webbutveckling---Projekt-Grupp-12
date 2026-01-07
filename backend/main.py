from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.search import router as search_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(search_router)


@app.get("/")
def root():
    return {"status": "ok"}
