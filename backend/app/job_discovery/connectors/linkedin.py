import time
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup


class LinkedInConnector:
    """Connector for LinkedIn jobs with real web scraping."""

    name = "LinkedIn"
    base_url = "https://www.linkedin.com/jobs/search"

    def fetch_jobs(self, query: str | None = None, limit: int = 10) -> list[dict]:
        """Fetch real jobs from LinkedIn job search."""
        if not query:
            query = "Python Backend Engineer"
        
        search_query = quote_plus(query)
        url = f"{self.base_url}?keywords={search_query}&location=India&f_TPR=r86400"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        }
        
        jobs = []
        try:
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code != 200:
                return []
            
            soup = BeautifulSoup(response.content, 'html.parser')
            job_cards = soup.find_all('div', class_='base-card', limit=limit)
            
            for card in job_cards:
                try:
                    title_elem = card.find('h3', class_='base-search-card__title')
                    company_elem = card.find('h4', class_='base-search-card__subtitle')
                    location_elem = card.find('span', class_='job-search-card__location')
                    link_elem = card.find('a', class_='base-card__full-link')
                    
                    if not title_elem or not company_elem or not link_elem:
                        continue
                    
                    title = title_elem.get_text(strip=True)
                    company = company_elem.get_text(strip=True)
                    location = location_elem.get_text(strip=True) if location_elem else "Remote"
                    job_url = link_elem.get('href', '')
                    
                    # Clean up URL (remove tracking params)
                    if '?' in job_url:
                        job_url = job_url.split('?')[0]
                    
                    if job_url and 'linkedin.com/jobs/view/' in job_url:
                        jobs.append({
                            "title": title,
                            "company": company,
                            "location": location,
                            "url": job_url,
                            "source": self.name,
                            "description": f"LinkedIn job posting for {title} at {company}",
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
