from __future__ import annotations

from pathlib import Path

from app.application_agent.submitter import prepare_submission
from app.job_discovery.discovery import DEFAULT_SOURCE_CONNECTORS, discover_jobs_for_resume
from app.resume_engine.parser import BASE_RESUME_PATH, extract_resume_summary
from app.resume_tailoring.tailor import tailor_resume_for_job

ROOT_DIR = Path(__file__).resolve().parents[2]


def _match_score(resume_summary: dict, job: dict) -> float:
    skills = {skill.lower() for skill in resume_summary.get("skills", [])}
    description = (job.get("description") or "").lower()
    overlap = sum(1 for skill in skills if skill in description)
    score = min(0.82, (overlap / max(len(skills), 1)) + 0.35)
    if "python" in description and "python" in skills:
        score += 0.10
    return round(min(score, 0.99), 2)


def run_autonomous_job_hunt(base_resume_path: str | Path | None = None, sources: list[str] | None = None) -> dict:
    resume_path = Path(base_resume_path) if base_resume_path else BASE_RESUME_PATH
    resume_summary = extract_resume_summary(resume_path)
    discovered_jobs = discover_jobs_for_resume(resume_summary, sources=sources)

    shortlisted = []
    for job in discovered_jobs:
        score = _match_score(resume_summary, job)
        if score >= 0.65:
            tailored = tailor_resume_for_job(resume_summary, job)
            submission = prepare_submission(job, tailored["file_path"])
            shortlisted.append(
                {
                    "job": job,
                    "match_score": score,
                    "tailored_resume": tailored,
                    "submission": submission,
                }
            )

    return {
        "status": "ok",
        "resume_summary": resume_summary,
        "sources_checked": sources or list(DEFAULT_SOURCE_CONNECTORS.keys()),
        "jobs_evaluated": len(discovered_jobs),
        "shortlisted_jobs": len(shortlisted),
        "results": shortlisted,
    }
