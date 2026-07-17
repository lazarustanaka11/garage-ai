from fastapi import FastAPI

from app.api.v1.auth import router as auth_router
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

app.include_router(auth_router)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "application": settings.app_name,
        "version": settings.app_version,
        "status": "running",
    }
