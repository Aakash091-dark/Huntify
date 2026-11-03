from abc import ABC, abstractmethod


class BaseConnector(ABC):
    """Base interface for each job source connector."""

    name: str = "base"

    @abstractmethod
    def fetch_jobs(self, query: str | None = None, limit: int = 10) -> list[dict]:
        """Return a list of normalized job dictionaries."""
        raise NotImplementedError
