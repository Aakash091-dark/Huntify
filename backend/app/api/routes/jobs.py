from typing import Any

from fastapi import APIRouter, HTTPException, Query

from app.autonomous.agent import run_autonomous_job_hunt

router = APIRouter(prefix="/jobs", tags=["jobs"])

_SAMPLE_JOBS = [
    {
        "id": "job-001",
        "title": "Senior Backend Engineer",
        "company": "Northstar Labs",
        "location": "Remote",
        "source": "LinkedIn",
        "salary": "$180k - $220k",
        "match_score": 92,
    },
    {
        "id": "job-002",
        "title": "Full Stack Python Engineer",
        "company": "Horizon Data",
        "location": "Bengaluru, India",
        "source": "Naukri",
        "salary": "₹20L - ₹32L",
        "match_score": 88,
    },
]


@router.get("/")
async def list_jobs(
    source: str | None = Query(default=None, description="Optional source filter"),
    limit: int = Query(default=25, ge=1, le=100),
) -> dict[str, Any]:
    jobs = _SAMPLE_JOBS
    if source:
        jobs = [job for job in jobs if job["source"].lower() == source.lower()]
    return {"status": "ok", "items": jobs[:limit], "count": len(jobs[:limit])}


@router.post("/autonomous-run")
async def run_job_agent() -> dict[str, Any]:
    result = run_autonomous_job_hunt()
    return {"status": "ok", "agent_result": result}


@router.get("/{job_id}")
async def get_job(job_id: str) -> dict[str, Any]:
    for job in _SAMPLE_JOBS:
        if job["id"] == job_id:
            return {"status": "ok", "job": job}
    raise HTTPException(status_code=404, detail=f"Job '{job_id}' was not found.")
