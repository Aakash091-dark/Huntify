from typing import Any

from fastapi import APIRouter

router = APIRouter(prefix="/matching", tags=["matching"])


@router.get("/score")
async def score_candidate() -> dict[str, Any]:
    return {
        "status": "ok",
        "score_breakdown": {
            "technical_skills": 35,
            "experience": 25,
            "role_relevance": 20,
            "education": 10,
            "location_and_compensation": 10,
        },
        "overall_score": 91,
        "eligible": True,
        "reasons": [
            "Strong Python and backend experience",
            "Skill overlap includes FastAPI and SQLAlchemy",
            "Location preference is compatible with the role",
        ],
    }
