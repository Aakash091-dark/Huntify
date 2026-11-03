from __future__ import annotations

from pathlib import Path

def prepare_submission(job: dict, resume_path: str | Path) -> dict:
    return {
        "status": "ready_for_approval",
        "job_id": job.get("id", "unknown-job"),
        "job_title": job.get("title", "Open Role"),
        "company": job.get("company", "Target Company"),
        "resume_path": str(resume_path),
        "submit_url": job.get("url"),
        "approval_required": True,
    }
