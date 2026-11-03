import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT_DIR = Path(__file__).resolve().parents[3]
BASE_RESUME_PATH = ROOT_DIR / "storage" / "master_resume" / "base_resume.txt"


def _extract_text_from_docx(path: Path) -> str:
    with zipfile.ZipFile(path) as docx_file:
        xml_data = docx_file.read("word/document.xml")
    root = ET.fromstring(xml_data)
    namespace = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    text_nodes = [node.text or "" for node in root.findall(".//w:t", namespace)]
    return "".join(text_nodes)


def _read_resume_text(file_path: str | Path) -> str:
    path = Path(file_path)
    if not path.exists():
        return ""

    if path.suffix.lower() == ".docx":
        return _extract_text_from_docx(path)

    return path.read_text(encoding="utf-8", errors="ignore")


def extract_resume_summary(file_path: str | Path | None = None) -> dict:
    path = Path(file_path) if file_path else BASE_RESUME_PATH
    text = _read_resume_text(path)
    text_clean = re.sub(r"\s+", " ", text).strip()

    skills = [
        "Python",
        "FastAPI",
        "PostgreSQL",
        "AI",
        "LLM",
        "RAG",
        "Redis",
        "Docker",
        "Kubernetes",
        "Celery",
        "JavaScript",
        "React",
    ]
    skill_matches = [skill for skill in skills if skill.lower() in text_clean.lower()]

    preferred_roles = [
        role for role in ["Backend Engineer", "AI Engineer", "Python Developer", "LLM Engineer"]
        if role.lower() in text_clean.lower()
    ]
    if not preferred_roles:
        preferred_roles = ["Backend Engineer", "AI Engineer"]

    experience_years = 4.5
    match = re.search(r"(\d+(?:\.\d+)?)\s*(?:years|yrs|year)", text_clean, re.IGNORECASE)
    if match:
        experience_years = float(match.group(1))

    return {
        "file_name": path.name,
        "parsed": bool(text_clean),
        "experience_years": experience_years,
        "skills": skill_matches or ["Python", "FastAPI", "PostgreSQL", "AI"],
        "preferred_roles": preferred_roles,
        "base_resume_path": str(path),
    }
