from __future__ import annotations

from app.job_discovery.connectors.company_careers import CompanyCareersConnector
from app.job_discovery.connectors.cutshort import CutshortConnector
from app.job_discovery.connectors.foundit import FounditConnector
from app.job_discovery.connectors.indeed import IndeedConnector
from app.job_discovery.connectors.instahyre import InstahyreConnector
from app.job_discovery.connectors.linkedin import LinkedInConnector
from app.job_discovery.connectors.naukri import NaukriConnector
from app.job_discovery.connectors.wellfound import WellfoundConnector

DEFAULT_SOURCE_CONNECTORS = {
    "LinkedIn": LinkedInConnector,
    "Naukri": NaukriConnector,
    "Indeed": IndeedConnector,
    "CompanyCareers": CompanyCareersConnector,
    "Wellfound": WellfoundConnector,
    "Foundit": FounditConnector,
    "Cutshort": CutshortConnector,
    "Instahyre": InstahyreConnector,
}


def discover_jobs_for_resume(resume_summary: dict, sources: list[str] | None = None) -> list[dict]:
    selected_sources = sources or list(DEFAULT_SOURCE_CONNECTORS.keys())
    query_keywords = resume_summary.get("skills", [])
    query = " ".join(query_keywords[:5])

    jobs: list[dict] = []
    for source_name in selected_sources:
        connector_cls = DEFAULT_SOURCE_CONNECTORS.get(source_name)
        if connector_cls is None:
            continue
        connector = connector_cls()
        fetched = connector.fetch_jobs(query=query, limit=5)
        for index, job in enumerate(fetched):
            url = job.get("url")
            title = job.get("title")
            company = job.get("company")
            if not url or not title or not company or "example.com" in url:
                continue

            normalized = {
                "id": f"{source_name.lower()}-{index + 1}",
                "source": source_name,
                "title": title,
                "company": company,
                "location": job.get("location") or "Remote",
                "salary": job.get("salary") or "Not disclosed",
                "url": url,
                "description": job.get("description") or "",
            }
            jobs.append(normalized)
    return jobs
