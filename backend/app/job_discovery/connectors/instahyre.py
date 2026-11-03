import time
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup


class InstahyreConnector:
    """Connector for Instahyre jobs with real web scraping."""

    name = "Instahyre"
    base_url = "https://www.instahyre.com"

    def fetch_jobs(self, query: str | None = None, limit: int = 10) -> list[dict]:
        """Fetch real jobs from Instahyre."""
        if not query:
            query = "Python Backend Developer"
        
        # Instahyre job search
        search_query = quote_plus(query)
        url = f"{self.base_url}/search-jobs/?q={search_query}"
        
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
            job_cards = soup.find_all('div', class_='opportunity-card', limit=limit)
            
            for card in job_cards:
                try:
                    title_elem = card.find('p', class_='opportunity-title')
                    company_elem = card.find('p', class_='company-name')
                    location_elem = card.find('span', class_='location')
                    link_elem = card.find('a', href=True)
                    
                    if not title_elem or not company_elem or not link_elem:
                        continue
                    
                    title = title_elem.get_text(strip=True)
                    company = company_elem.get_text(strip=True)
                    location = location_elem.get_text(strip=True) if location_elem else "Multiple locations"
                    job_url = link_elem.get('href', '')
                    
                    if job_url and not job_url.startswith('http'):
                        job_url = self.base_url + job_url
                    
                    if job_url and 'instahyre.com' in job_url:
                        jobs.append({
                            "title": title,
                            "company": company,
                            "location": location,
                            "url": job_url,
                            "source": self.name,
                            "description": f"Instahyre job posting for {title} at {company}",
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
