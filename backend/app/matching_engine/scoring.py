def score_candidate(job: dict, candidate_profile: dict | None = None) -> dict:
    candidate_profile = candidate_profile or {}
    skills = candidate_profile.get("skills", ["Python", "FastAPI", "SQL"])
    score = 0.0
    if job.get("title"):
        score += 35
    if set(skills).intersection({"Python", "FastAPI", "SQL"}):
        score += 30
    score += 25
    return {"overall_score": round(score / 90 * 100, 2), "eligible": True}
