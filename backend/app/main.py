from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api.router import api_router

app = FastAPI(
    title="ApplyPilot AI API",
    description="AI that applies to jobs exactly like a top candidate would.",
    version="1.0.0",
    docs_url="/docs" if settings.APP_ENV != "production" else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/v1")


@app.get("/health")
async def health():
    return {"status": "ok", "version": "1.0.0", "env": settings.APP_ENV}
