from typing import Any

from fastapi import APIRouter, File, UploadFile

from app.resume_engine.parser import BASE_RESUME_PATH, extract_resume_summary

router = APIRouter(prefix="/resume", tags=["resume"])


@router.get("/summary")
async def get_resume_summary() -> dict[str, Any]:
    summary = extract_resume_summary(BASE_RESUME_PATH)
    return {"status": "ok", "summary": summary}


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)) -> dict[str, Any]:
    temp_path = BASE_RESUME_PATH
    if file.filename and file.filename.lower().endswith(".docx"):
        temp_path = BASE_RESUME_PATH.with_suffix(".docx")
    summary = extract_resume_summary(temp_path)
    return {
        "status": "uploaded",
        "file_name": file.filename,
        "content_type": file.content_type,
        "message": "Resume upload endpoint is ready for integration with PDF/DOCX parsing.",
        "summary": summary,
    }
