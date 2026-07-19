from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.v1.auth import router as auth_router
from app.api.v1.customers import router as customer_router
from app.api.v1.vehicles import router as vehicle_router
from app.api.v1.repair_jobs import router as repair_job_router
from app.api.v1.ai import router as ai_router
from app.core.config import settings
from app.web.routes import router as web_router

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

# Static files (CSS, JavaScript, images)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# API Routers
app.include_router(auth_router)
app.include_router(customer_router)
app.include_router(vehicle_router)
app.include_router(repair_job_router)
app.include_router(ai_router)

# Web Pages
app.include_router(web_router)


@app.get("/api")
async def api_health():
    """Health check endpoint."""
    return {
        "application": settings.app_name,
        "version": settings.app_version,
        "status": "running",
    }
