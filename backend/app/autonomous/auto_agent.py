"""Fully automated job hunting agent - finds jobs, tailors resumes, and applies automatically."""
from __future__ import annotations

import logging
from pathlib import Path

from app.application_agent.auto_applier import AutoJobApplier
from app.job_discovery.discovery import DEFAULT_SOURCE_CONNECTORS, discover_jobs_for_resume
from app.resume_engine.parser import BASE_RESUME_PATH, extract_resume_summary
from app.resume_tailoring.tailor import tailor_resume_for_job

logger = logging.getLogger(__name__)


def _match_score(resume_summary: dict, job: dict) -> float:
    """Calculate match score between resume and job."""
    skills = {skill.lower() for skill in resume_summary.get("skills", [])}
    description = (job.get("description") or "").lower()
    title = (job.get("title") or "").lower()
    
    # Check skill overlap in description
    overlap = sum(1 for skill in skills if skill in description or skill in title)
    score = min(0.82, (overlap / max(len(skills), 1)) + 0.35)
    
    # Bonus for specific skills
    if "python" in description and "python" in skills:
        score += 0.10
    if "fastapi" in description and "fastapi" in skills:
        score += 0.05
    if "ai" in title or "ml" in title or "machine learning" in title:
        score += 0.08
    
    return round(min(score, 0.99), 2)


async def run_fully_automated_hunt(
    base_resume_path: str | Path | None = None,
    sources: list[str] | None = None,
    min_match_score: float = 0.60,
    max_applications: int = 10,
    headless: bool = False,
    auto_submit: bool = True,
) -> dict:
    """
    Run fully automated job hunt: discover jobs, match, tailor resumes, and apply.
    
    Args:
        base_resume_path: Path to base resume file
        sources: Job sources to search (None = all sources)
        min_match_score: Minimum match score to apply (0.0-1.0)
        max_applications: Maximum number of applications to submit
        headless: Whether to run browser in headless mode
        auto_submit: Whether to automatically submit applications
        
    Returns:
        Results dict with all application outcomes
    """
    logger.info("="*80)
    logger.info("STARTING FULLY AUTOMATED JOB HUNT")
    logger.info("="*80)
    
    # Step 1: Parse resume
    resume_path = Path(base_resume_path) if base_resume_path else BASE_RESUME_PATH
    logger.info(f"\n[1/5] Parsing resume from: {resume_path}")
    resume_summary = extract_resume_summary(resume_path)
    logger.info(f"✓ Resume parsed - Skills: {', '.join(resume_summary['skills'][:5])}")
    
    # Step 2: Discover jobs from web
    logger.info(f"\n[2/5] Discovering jobs from {len(sources or DEFAULT_SOURCE_CONNECTORS)} sources...")
    discovered_jobs = discover_jobs_for_resume(resume_summary, sources=sources)
    logger.info(f"✓ Found {len(discovered_jobs)} valid job listings")
    
    if not discovered_jobs:
        return {
            "status": "no_jobs_found",
            "message": "No valid job listings were discovered from the configured sources",
            "resume_summary": resume_summary,
            "sources_checked": sources or list(DEFAULT_SOURCE_CONNECTORS.keys()),
            "jobs_evaluated": 0,
            "applications_submitted": 0,
        }
    
    # Step 3: Match and filter jobs
    logger.info(f"\n[3/5] Matching jobs against resume (min score: {min_match_score})...")
    matched_jobs = []
    for job in discovered_jobs:
        score = _match_score(resume_summary, job)
        if score >= min_match_score:
            matched_jobs.append({"job": job, "match_score": score})
    
    # Sort by match score
    matched_jobs.sort(key=lambda x: x["match_score"], reverse=True)
    matched_jobs = matched_jobs[:max_applications]
    logger.info(f"✓ {len(matched_jobs)} jobs matched (showing top {max_applications})")
    
    if not matched_jobs:
        return {
            "status": "no_matches",
            "message": f"Found {len(discovered_jobs)} jobs but none matched your criteria",
            "resume_summary": resume_summary,
            "sources_checked": sources or list(DEFAULT_SOURCE_CONNECTORS.keys()),
            "jobs_evaluated": len(discovered_jobs),
            "applications_submitted": 0,
        }
    
    # Step 4: Tailor resumes
    logger.info(f"\n[4/5] Tailoring resumes for {len(matched_jobs)} jobs...")
    jobs_with_resumes = []
    for item in matched_jobs:
        job = item["job"]
        try:
            tailored = tailor_resume_for_job(resume_summary, job)
            jobs_with_resumes.append({
                "job": job,
                "match_score": item["match_score"],
                "resume_path": tailored["file_path"],
                "tailored_resume": tailored,
            })
            logger.info(f"  ✓ Tailored resume for: {job['title']} at {job['company']}")
        except Exception as e:
            logger.error(f"  ✗ Failed to tailor resume for {job['title']}: {e}")
    
    logger.info(f"✓ Tailored {len(jobs_with_resumes)} resumes")
    
    # Step 5: Apply to jobs automatically
    applications_results = []
    if auto_submit and jobs_with_resumes:
        logger.info(f"\n[5/5] Applying to {len(jobs_with_resumes)} jobs automatically...")
        logger.info(f"Browser mode: {'headless' if headless else 'visible'}")
        
        try:
            applier = AutoJobApplier(headless=headless)
            applications_results = await applier.apply_to_jobs_batch(jobs_with_resumes)
            
            # Summary
            successful = sum(1 for r in applications_results if r["status"] == "submitted")
            partial = sum(1 for r in applications_results if r["status"] == "partially_completed")
            failed = len(applications_results) - successful - partial
            
            logger.info(f"\n{'='*80}")
            logger.info("APPLICATION SUMMARY")
            logger.info(f"{'='*80}")
            logger.info(f"✓ Successfully submitted: {successful}")
            logger.info(f"⚠ Partially completed: {partial}")
            logger.info(f"✗ Failed: {failed}")
            logger.info(f"{'='*80}\n")
        except Exception as e:
            logger.error(f"Error during browser automation: {e}", exc_info=True)
            # Return error but don't fail completely
            applications_results = [
                {
                    "status": "error",
                    "job_title": item["job"]["title"],
                    "company": item["job"]["company"],
                    "error": str(e),
                    "note": "Browser automation failed - see logs for details"
                }
                for item in jobs_with_resumes
            ]
    else:
        logger.info(f"\n[5/5] Auto-submit disabled - applications prepared for manual review")
        applications_results = [
            {
                "status": "ready_for_review",
                "job_title": item["job"]["title"],
                "company": item["job"]["company"],
                "url": item["job"]["url"],
                "match_score": item["match_score"],
                "resume_path": item["resume_path"],
            }
            for item in jobs_with_resumes
        ]
    
    return {
        "status": "completed",
        "message": f"Processed {len(discovered_jobs)} jobs, applied to {len(applications_results)}",
        "resume_summary": resume_summary,
        "sources_checked": sources or list(DEFAULT_SOURCE_CONNECTORS.keys()),
        "jobs_evaluated": len(discovered_jobs),
        "jobs_matched": len(matched_jobs),
        "applications_submitted": len(applications_results),
        "applications": applications_results,
        "jobs_with_resumes": jobs_with_resumes,
    }
