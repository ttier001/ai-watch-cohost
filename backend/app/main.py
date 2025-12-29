"""AI Watch Co-Host API"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.api import classify, generate, user_analysis
from app.config import settings

load_dotenv()

app = FastAPI(
    title="Go Live AI Co-Host API",
    description="AI assistant for live commerce sellers",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
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
app.include_router(user_analysis.router, prefix="/api", tags=["user_analysis"])

@app.get("/")
def read_root():
    return {
        "status": "ok",
        "message": "Go Live AI Co-Host API",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
