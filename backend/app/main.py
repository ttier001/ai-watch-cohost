"""AI Watch Co-Host API"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.api import classify, generate
from app.config import settings

load_dotenv()

app = FastAPI(
    title="AI Watch Co-Host API",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(classify.router, prefix="/api", tags=["classify"])
app.include_router(generate.router, prefix="/api", tags=["generate"])

@app.get("/")
def read_root():
    return {
        "status": "ok",
        "message": "AI Watch Co-Host API",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
