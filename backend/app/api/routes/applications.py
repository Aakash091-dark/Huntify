from typing import Any

from fastapi import APIRouter, HTTPException, Query

from app.autonomous.agent import run_autonomous_job_hunt
from app.autonomous.auto_agent import run_fully_automated_hunt
from app.application_agent.live_browser_agent import LiveBrowserAgent
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
    Fully automated job application workflow - runs as background subprocess
    """
    import subprocess
    import json
    from pathlib import Path
    
    backend_dir = Path(__file__).parent.parent.parent.parent
    script_path = backend_dir / "run_auto_apply.py"
    
    # Build command
    cmd = [
        "python",
        str(script_path),
        "--max-jobs", str(max_jobs),
        "--min-score", str(min_score),
    ]
    
    if headless:
        cmd.append("--headless")
    
    if sources:
        cmd.extend(["--sources", sources])
    
    try:
        # Run in background
        process = subprocess.Popen(
            cmd,
            cwd=str(backend_dir),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Don't wait for completion - let it run in background
        return {
            "status": "started",
            "message": f"Auto-apply process started in background. Processing up to {max_jobs} jobs with min score {min_score}. Check logs at backend/huntify_automation.log",
            "settings": {
                "max_jobs": max_jobs,
                "min_score": min_score,
                "headless": headless,
                "sources": sources or "all",
            },
            "log_file": "backend/huntify_automation.log"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to start auto-apply process: {str(e)}",
            "error": str(e)
        }



@router.post("/live-browser-apply")
async def live_browser_apply(
    search_query: str = Query(default="Python Backend Developer", description="Job search query"),
    sources: str = Query(default="Naukri,Indeed", description="Comma-separated list of sources"),
    max_per_source: int = Query(default=5, ge=1, le=20, description="Max applications per source"),
    headless: bool = Query(default=False, description="Run browser in headless mode"),
) -> dict[str, Any]:
    """
    Live browser application:
    1. Opens job board in browser
    2. Searches for jobs using your query
    3. Clicks on each job
    4. Applies in real-time
    """
    source_list = [s.strip() for s in sources.split(",")]
    
    agent = LiveBrowserAgent(headless=headless)
    result = agent.run_live_application_session(
        search_query=search_query,
        sources=source_list,
        max_per_source=max_per_source
    )
    
    return {
        "status": result["status"],
        "message": f"Live browser session completed. Attempted {result['total_attempted']}, Successful {result['total_successful']}",
        "search_query": result["search_query"],
        "sources": result["sources_processed"],
        "total_attempted": result["total_attempted"],
        "total_successful": result["total_successful"],
        "details": result["details_by_source"],
    }
