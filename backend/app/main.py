from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import asyncio

# Fix for Windows + Playwright async
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from app.api.routes.applications import router as applications_router
from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.jobs import router as jobs_router
from app.api.routes.matching import router as matching_router
from app.api.routes.resume import router as resume_router
from app.config import settings

app = FastAPI(
    title=settings.app_name,
    description="AI-powered job discovery and application platform",
    version=settings.app_version,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resume_router, prefix="/api/v1")
app.include_router(jobs_router, prefix="/api/v1")
app.include_router(matching_router, prefix="/api/v1")
app.include_router(applications_router, prefix="/api/v1")
app.include_router(dashboard_router, prefix="/api/v1")


@app.get("/")
def home() -> dict[str, str]:
    return {
        "message": "Job Agent AI is running",
        "status": "success",
    }


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "healthy"}
