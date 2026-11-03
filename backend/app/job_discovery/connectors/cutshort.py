class CutshortConnector:
    """Connector for Cutshort jobs."""

    name = "Cutshort"

    def fetch_jobs(self, query: str | None = None, limit: int = 10) -> list[dict]:
        return [{"source": self.name, "title": "AI Engineer", "query": query, "limit": limit}]
