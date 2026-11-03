from dataclasses import dataclass


@dataclass
class JobValidationResult:
    valid: bool
    errors: list[str]
    warnings: list[str]


def validate_job(job: dict) -> JobValidationResult:
    errors: list[str] = []
    warnings: list[str] = []

    if not job.get("title"):
        errors.append("Job title is required.")
    if not job.get("company"):
        warnings.append("Company name is missing.")
    if not job.get("description"):
        errors.append("Description is required.")

    return JobValidationResult(valid=not errors, errors=errors, warnings=warnings)
