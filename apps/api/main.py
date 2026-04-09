"""GenUIWar API — FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apps.api.routes import calculations, evidence, files, health
from packages.shared.config import get_settings

settings = get_settings()

app = FastAPI(
    title="GenUIWar API",
    description="Ministry-grade analytical conversation system",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[f"http://localhost:{settings.web_port}"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api/v1")
app.include_router(files.router, prefix="/api/v1")
app.include_router(evidence.router, prefix="/api/v1")
app.include_router(calculations.router, prefix="/api/v1")
