from typing import Any

from fastapi import APIRouter

from app.services.application_tracker import latest_jobs_discovered, list_applications

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary")
async def dashboard_summary() -> dict[str, Any]:
    items = list_applications()
    approved = sum(1 for item in items if item.get("status") == "approved")
    pending = sum(1 for item in items if item.get("status") in {"queued", "pending_review", "draft"})
    return {
        "status": "ok",
        "summary": {
            "jobs_discovered": latest_jobs_discovered(),
            "jobs_matching": len(items),
            "applications_in_progress": len(items),
            "accepted": approved,
            "pending_approval": pending,
        },
        "approval_queue": items,
    }
