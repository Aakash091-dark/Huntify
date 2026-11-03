from __future__ import annotations

from uuid import uuid4

_APPLICATIONS: list[dict] = []
_LATEST_JOBS_DISCOVERED = 0


def record_discovery_count(count: int) -> None:
    global _LATEST_JOBS_DISCOVERED
    _LATEST_JOBS_DISCOVERED = count


def latest_jobs_discovered() -> int:
    return _LATEST_JOBS_DISCOVERED


def create_application(job: dict, match_score: float, tailored_resume: dict) -> dict:
    job_url = job.get("url")
    for application in _APPLICATIONS:
        if job_url and application.get("job_url") == job_url:
            return application

    application = {
        "id": str(uuid4()),
        "job_id": job.get("id"),
        "company": job.get("company", "Unknown company"),
        "role": job.get("title", "Untitled role"),
        "source": job.get("source", "Unknown source"),
        "job_url": job_url,
        "match_score": match_score,
        "resume_path": tailored_resume.get("file_path"),
        "status": "pending_review",
        "status_message": "Tailored resume prepared; waiting for your approval.",
    }
    _APPLICATIONS.append(application)
    return application


def track_application(application_id: str, status: str) -> dict | None:
    for item in _APPLICATIONS:
        if item["id"] == application_id:
            item["status"] = status
            return item
    return None


def list_applications() -> list[dict]:
    return list(_APPLICATIONS)


def get_application_status(application_id: str) -> dict | None:
    for item in _APPLICATIONS:
        if item["id"] == application_id:
            return {"application_id": application_id, "status": item["status"]}
    return None
