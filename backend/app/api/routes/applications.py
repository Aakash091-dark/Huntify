from typing import Any

from fastapi import APIRouter, HTTPException, Query

from app.autonomous.agent import run_autonomous_job_hunt
from app.autonomous.auto_agent import run_fully_automated_hunt
from app.services.application_tracker import (
    create_application,
    get_application_status,
    record_discovery_count,
    list_applications,
    track_application,
)

router = APIRouter(prefix="/applications", tags=["applications"])

@router.get("/")
async def list_applications_route() -> dict[str, Any]:
    items = list_applications()
    return {"status": "ok", "items": items, "count": len(items)}


@router.post("/start")
async def start_applying() -> dict[str, Any]:
    result = run_autonomous_job_hunt()
    record_discovery_count(result["jobs_evaluated"])
    applications = [
        create_application(
            item["job"],
            item["match_score"],
            item["tailored_resume"],
        )
        for item in result["results"]
    ]
    return {
        "status": "completed",
        "message": (
            "Matching jobs were prepared for your approval."
            if applications
            else "No verifiable job listings were returned by the configured sources."
        ),
        "jobs_evaluated": result["jobs_evaluated"],
        "applications_created": len(applications),
        "applications": applications,
        "sources_checked": result["sources_checked"],
    }


@router.get("/queue")
async def application_queue() -> dict[str, Any]:
    items = list_applications()
    pending = [item for item in items if item.get("status") in {"pending_review", "queued", "draft"}]
    return {"status": "ok", "items": pending, "count": len(pending)}


@router.get("/{application_id}/status")
async def application_status(application_id: str) -> dict[str, Any]:
    status = get_application_status(application_id)
    if status is None:
        raise HTTPException(status_code=404, detail=f"Application '{application_id}' was not found.")
    return status


@router.post("/{application_id}/approve")
async def approve_application(application_id: str) -> dict[str, Any]:
    application = track_application(application_id, "approved")
    if application is None:
        raise HTTPException(status_code=404, detail=f"Application '{application_id}' was not found.")
    application["status_message"] = "Approved by you; ready for the next submission step."
    return {"status": "ok", "application": application}


@router.post("/auto-apply")
async def auto_apply_to_jobs(
    min_score: float = Query(default=0.60, ge=0.0, le=1.0, description="Minimum match score"),
    max_jobs: int = Query(default=10, ge=1, le=50, description="Maximum applications to submit"),
    headless: bool = Query(default=False, description="Run browser in headless mode"),
    sources: str | None = Query(default=None, description="Comma-separated list of sources"),
) -> dict[str, Any]:
    """
    Fully automated job application workflow:
    1. Scrapes jobs from web based on your resume
    2. Matches and filters relevant positions
    3. Tailors resumes for each job
    4. Automatically applies via browser automation
    """
    source_list = sources.split(",") if sources else None
    
    result = run_fully_automated_hunt(
        sources=source_list,
        min_match_score=min_score,
        max_applications=max_jobs,
        headless=headless,
        auto_submit=True,
    )
    
    # Record applications in tracker
    for app in result.get("applications", []):
        if app.get("status") in {"submitted", "partially_completed"}:
            try:
                create_application(
                    {"title": app["job_title"], "company": app["company"], "url": app.get("url", "")},
                    app.get("match_score", 0.0),
                    {"file_path": app.get("resume_path", "")},
                )
            except Exception:
                pass
    
    return {
        "status": result["status"],
        "message": result["message"],
        "jobs_evaluated": result.get("jobs_evaluated", 0),
        "jobs_matched": result.get("jobs_matched", 0),
        "applications_submitted": result.get("applications_submitted", 0),
        "applications": result.get("applications", []),
    }
