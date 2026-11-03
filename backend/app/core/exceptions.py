class JobAgentError(Exception):
    """Base application error for the platform."""


class ValidationError(JobAgentError):
    """Raised when uploaded data fails validation."""
