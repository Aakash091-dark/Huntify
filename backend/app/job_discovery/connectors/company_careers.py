class CompanyCareersConnector:
    """Connector for company career pages."""

    name = "CompanyCareers"

    def fetch_jobs(self, query: str | None = None, limit: int = 10) -> list[dict]:
        return [{"source": self.name, "title": "Product Engineer", "query": query, "limit": limit}]
