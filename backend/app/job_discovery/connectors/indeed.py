import time
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup


class IndeedConnector:
    """Connector for Indeed jobs with real web scraping."""

    name = "Indeed"
    base_url = "https://in.indeed.com"

    def fetch_jobs(self, query: str | None = None, limit: int = 10) -> list[dict]:
        """Fetch real jobs from Indeed India."""
        if not query:
            query = "Python Backend Developer"
        
        search_query = quote_plus(query)
        url = f"{self.base_url}/jobs?q={search_query}&l=India"
        
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
            
            # Indeed uses different class names, trying multiple patterns
            job_cards = soup.find_all('div', class_='job_seen_beacon') or soup.find_all('a', class_='tapItem')
            
            for card in job_cards[:limit * 2]:
                try:
                    # Try to find title
                    title_elem = card.find('h2', class_='jobTitle') or card.find('span', title=True)
                    company_elem = card.find('span', class_='companyName')
                    location_elem = card.find('div', class_='companyLocation')
                    
                    if not title_elem or not company_elem:
                        continue
                    
                    # Extract title text
                    title = title_elem.get_text(strip=True) if hasattr(title_elem, 'get_text') else str(title_elem.get('title', ''))
                    company = company_elem.get_text(strip=True)
                    location = location_elem.get_text(strip=True) if location_elem else "Multiple locations"
                    
                    # Find job link
                    job_link = card.find('a', class_='jcs-JobTitle') or card.find('a', href=True)
                    if not job_link:
                        continue
                    
                    job_url = job_link.get('href', '')
                    if job_url and not job_url.startswith('http'):
                        job_url = self.base_url + job_url
                    
                    if job_url and 'indeed.com' in job_url and title and company:
                        jobs.append({
                            "title": title,
                            "company": company,
                            "location": location,
                            "url": job_url,
                            "source": self.name,
                            "description": f"Indeed job posting for {title} at {company}",
                            "salary": "Not disclosed"
                        })
                    
                    if len(jobs) >= limit:
                        break
                        
                except Exception:
                    continue
            
            time.sleep(1)  # Rate limiting
            
        except Exception:
            pass
        
        return jobs
