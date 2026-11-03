from __future__ import annotations

import re
from pathlib import Path

from docx import Document

ROOT_DIR = Path(__file__).resolve().parents[2]
OUTPUT_DIR = ROOT_DIR / "storage" / "tailored_resumes"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def _extract_keywords(text: str) -> list[str]:
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text.lower())
    words = [word for word in text.split() if len(word) > 3]
    counts: dict[str, int] = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    ranked = [word for word, _ in sorted(counts.items(), key=lambda item: (-item[1], item[0]))]
    priority = {"python", "fastapi", "postgresql", "redis", "llm", "ai", "rag", "kubernetes", "docker", "celery", "backend", "api", "sql", "agentic", "prompt", "vector"}
    ordered = [word for word in ranked if word in priority]
    ordered += [word for word in ranked if word not in priority]
    return ordered[:15]


def tailor_resume_for_job(resume_summary: dict, job: dict) -> dict:
    skills = resume_summary.get("skills", [])
    experience_years = resume_summary.get("experience_years", 4.5)
    job_title = job.get("title", "AI Engineer")
    company = job.get("company", "Target Company")
    job_description = job.get("description", "")
    keywords = _extract_keywords(job_description + " " + job_title)
    relevant_skills = [skill for skill in skills if isinstance(skill, str)]
    if len(relevant_skills) > 8:
        relevant_skills = relevant_skills[:8]

    matched_keywords = [kw for kw in keywords if kw.lower() in [s.lower() for s in relevant_skills]]
    if not matched_keywords:
        matched_keywords = keywords[:4]

    summary = (
        f"Python and AI developer with {experience_years:.1f} years of experience building scalable backend systems, API platforms, and LLM-powered workflows for production environments. "
        f"Expertise includes FastAPI, PostgreSQL, Redis, Celery, Docker, Kubernetes, and AI integrations such as LLM orchestration, RAG, and agentic tooling."
    )

    experience_lines = [
        "Designed and maintained multi-tenant SaaS backend services with FastAPI, PostgreSQL, Redis, and Celery.",
        "Integrated Anthropic and other AI APIs to build workflow automation, tool-using agents, and retrieval-based experiences.",
        "Deployed production-ready applications with Docker and Kubernetes, improving scalability, observability, and reliability.",
        "Partnered with product and growth teams to identify workflows that could be automated, increasing operational efficiency.",
    ]

    safe_title = re.sub(r"[^a-zA-Z0-9]+", "_", job_title).strip("_") or "tailored_resume"
    file_path = OUTPUT_DIR / f"{safe_title.lower()}_{company.lower()}.docx"
    text_path = OUTPUT_DIR / f"{safe_title.lower()}_{company.lower()}.txt"

    document = Document()
    document.add_heading(job_title, level=1)
    document.add_paragraph(summary)
    document.add_heading("Keyword Alignment", level=2)
    document.add_paragraph(", ".join(matched_keywords[:10]))
    document.add_heading("Core Skills", level=2)
    document.add_paragraph(", ".join(relevant_skills + keywords[:4]))
    document.add_heading("Relevant Experience", level=2)
    for line in experience_lines:
        document.add_paragraph(line)
    document.save(file_path)

    text_path.write_text(
        "\n\n".join([
            f"Role: {job_title}",
            f"Company: {company}",
            "Summary:",
            summary,
            "Keyword Alignment:",
            ", ".join(matched_keywords[:10]),
            "Core Skills:",
            ", ".join(relevant_skills + keywords[:4]),
            "Relevant Experience:",
            *experience_lines,
        ]),
        encoding="utf-8",
    )

    return {
        "job_title": job_title,
        "company": company,
        "summary": summary,
        "keywords": matched_keywords[:10],
        "file_path": str(file_path),
        "text_path": str(text_path),
        "status": "tailored",
    }
