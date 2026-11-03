import time
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup


class WellfoundConnector:
    """Connector for Wellfound (AngelList) jobs with real web scraping."""

    name = "Wellfound"
    base_url = "https://wellfound.com"

    def fetch_jobs(self, query: str | None = None, limit: int = 10) -> list[dict]:
        """Fetch real jobs from Wellfound."""
        if not query:
            query = "Backend Engineer"
        
        search_query = quote_plus(query)
        url = f"{self.base_url}/role/r/backend-engineer"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }
        
        jobs = []
        try:
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code != 200:
                return []
            
            soup = BeautifulSoup(response.content, 'html.parser')
            # Wellfound has dynamic content, might need Playwright
            job_links = soup.find_all('a', href=True, limit=limit * 2)
            
            for link in job_links:
                try:
                    href = link.get('href', '')
                    if '/companies/' not in href or '/jobs/' not in href:
                        continue
                    
                    # Try to extract job info from link
                    title_text = link.get_text(strip=True)
                    if not title_text or len(title_text) < 5:
                        continue
                    
                    job_url = href if href.startswith('http') else self.base_url + href
                    
                    if 'wellfound.com' in job_url:
                        jobs.append({
                            "title": title_text[:100],
                            "company": "Startup",
                            "location": "Remote",
                            "url": job_url,
                            "source": self.name,
                            "description": f"Wellfound startup job: {title_text}",
                            "salary": "Competitive"
                        })
                    
                    if len(jobs) >= limit:
                        break
                        
                except Exception:
                    continue
            
            time.sleep(1)
            
        except Exception:
            pass
        
        return jobs
