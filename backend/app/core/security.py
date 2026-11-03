"""Security helpers for the application."""


def sanitize_job_url(url: str) -> str:
    return url.strip() if url else ""
