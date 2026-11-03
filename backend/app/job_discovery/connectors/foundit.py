class FounditConnector:
    """Connector for Foundit jobs."""

    name = "Foundit"

    def fetch_jobs(self, query: str | None = None, limit: int = 10) -> list[dict]:
        return [{"source": self.name, "title": "Software Engineer", "query": query, "limit": limit}]
