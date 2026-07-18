from fastapi import FastAPI

from app.api.v1.auth import router as auth_router
from app.api.v1.customers import router as customer_router
from app.api.v1.vehicles import router as vehicle_router
from app.api.v1.repair_jobs import router as repair_job_router
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

app.include_router(auth_router)
app.include_router(customer_router)
app.include_router(vehicle_router)
app.include_router(repair_job_router)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "application": settings.app_name,
        "version": settings.app_version,
        "status": "running",
    }
