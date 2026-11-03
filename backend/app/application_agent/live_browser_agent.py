"""Live browser agent that opens job boards and applies in real-time."""
import logging
import time
from typing import Any

from playwright.sync_api import sync_playwright, Page, TimeoutError as PlaywrightTimeout

logger = logging.getLogger(__name__)


class LiveBrowserAgent:
    """Agent that opens job boards in browser and applies to jobs in real-time."""
    
    def __init__(self, headless: bool = False):
        self.headless = headless
        self.applicant_info = {
            "first_name": "Aakash",
            "last_name": "Sehrawat",
            "email": "aakashhssehrawat@gmail.com",
            "phone": "+91 9217030815",
            "linkedin": "https://linkedin.com/in/aakash-sehrawat",
            "github": "https://github.com/aakash-sehrawat",
        }
    
    def search_and_apply_naukri(self, search_query: str, max_applications: int = 10) -> dict[str, Any]:
        """Open Naukri.com, search jobs, and apply in real-time."""
        logger.info(f"Opening Naukri.com to search: {search_query}")
        
        results = {
            "source": "Naukri",
            "search_query": search_query,
            "jobs_found": 0,
            "applications_attempted": 0,
            "applications_successful": 0,
            "details": []
        }
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=self.headless, slow_mo=1000)
                context = browser.new_context(viewport={"width": 1280, "height": 900})
                page = context.new_page()
                
                # Go to Naukri homepage
                logger.info("Navigating to Naukri.com...")
                page.goto("https://www.naukri.com", timeout=30000)
                time.sleep(3)
                
                # Search for jobs
                logger.info(f"Searching for: {search_query}")
                try:
                    # Find search box and enter query
                    search_box = page.locator("input[placeholder*='Skills' i], input[class*='suggestor-input']").first
                    search_box.fill(search_query, timeout=5000)
                    time.sleep(1)
                    
                    # Click search button
                    search_btn = page.locator("button:has-text('Search'), button[class*='search']").first
                    search_btn.click(timeout=5000)
                    time.sleep(5)
                    
                    logger.info("Search results loaded")
                    results["jobs_found"] = "multiple"
                    
                    # Find job cards
                    job_cards = page.locator("article.jobTuple, div[class*='job'], div[class*='srp-tuple']")
                    job_count = job_cards.count()
                    logger.info(f"Found {job_count} job listings")
                    
                    applications_attempted = 0
                    
                    # Loop through jobs and apply
                    for i in range(min(job_count, max_applications)):
                        if applications_attempted >= max_applications:
                            break
                        
                        try:
                            logger.info(f"\n{'='*60}")
                            logger.info(f"Processing job {i+1}/{min(job_count, max_applications)}")
                            logger.info(f"{'='*60}")
                            
                            # Get job card
                            job_card = job_cards.nth(i)
                            
                            # Extract job title
                            try:
                                title_elem = job_card.locator("a.title, a[class*='title']").first
                                job_title = title_elem.text_content(timeout=2000) or "Unknown Position"
                            except:
                                job_title = "Unknown Position"
                            
                            # Extract company
                            try:
                                company_elem = job_card.locator("a.subTitle, a[class*='company']").first
                                company = company_elem.text_content(timeout=2000) or "Unknown Company"
                            except:
                                company = "Unknown Company"
                            
                            logger.info(f"Job: {job_title} at {company}")
                            
                            # Click on job to open details
                            job_card.click(timeout=5000)
                            time.sleep(3)
                            
                            # Look for Apply button in the detail panel
                            apply_result = self._try_apply_on_page(page, job_title, company)
                            
                            results["details"].append({
                                "job_title": job_title,
                                "company": company,
                                "status": apply_result["status"],
                                "note": apply_result.get("note", "")
                            })
                            
                            if apply_result["status"] == "applied":
                                results["applications_successful"] += 1
                            
                            applications_attempted += 1
                            results["applications_attempted"] = applications_attempted
                            
                            # Wait before next application
                            time.sleep(3)
                            
                        except Exception as job_error:
                            logger.error(f"Error processing job {i+1}: {job_error}")
                            continue
                    
                except Exception as search_error:
                    logger.error(f"Error during search: {search_error}")
                    results["error"] = str(search_error)
                
                # Keep browser open for a moment to see results
                logger.info("\nKeeping browser open for 10 seconds...")
                time.sleep(10)
                
                browser.close()
                
        except Exception as e:
            logger.error(f"Browser automation error: {e}")
            results["error"] = str(e)
        
        return results
    
    def _try_apply_on_page(self, page: Page, job_title: str, company: str) -> dict[str, str]:
        """Try to apply to the job on current page."""
        result = {"status": "not_applied", "note": ""}
        
        # Look for apply button
        apply_button_selectors = [
            "button:has-text('Apply')",
            "a:has-text('Apply')",
            "button[id*='apply']",
            "a[id*='apply']",
            "div.apply-button",
        ]
        
        for selector in apply_button_selectors:
            try:
                if page.locator(selector).count() > 0:
                    logger.info(f"Found apply button: {selector}")
                    page.locator(selector).first.click(timeout=3000)
                    time.sleep(2)
                    
                    # Try to fill application form
                    filled = self._fill_quick_apply_form(page)
                    
                    if filled:
                        # Try to submit
                        submitted = self._try_submit_form(page)
                        if submitted:
                            result["status"] = "applied"
                            result["note"] = "Application submitted successfully"
                            logger.info(f"✓ Applied to {job_title} at {company}")
                        else:
                            result["status"] = "form_filled"
                            result["note"] = "Form filled but couldn't confirm submission"
                            logger.warning(f"⚠ Filled form for {job_title} but couldn't submit")
                    else:
                        result["status"] = "clicked_apply"
                        result["note"] = "Clicked apply but couldn't fill form"
                        logger.warning(f"⚠ Clicked apply for {job_title} but couldn't fill form")
                    
                    return result
            except Exception as e:
                logger.debug(f"Apply button selector failed: {selector} - {e}")
                continue
        
        result["note"] = "No apply button found"
        logger.info(f"○ No apply button found for {job_title}")
        return result
    
    def _fill_quick_apply_form(self, page: Page) -> bool:
        """Fill quick apply form if present."""
        filled = False
        
        # Name fields
        name_fields = [
            ("input[name*='name' i]", f"{self.applicant_info['first_name']} {self.applicant_info['last_name']}"),
            ("input[placeholder*='name' i]", f"{self.applicant_info['first_name']} {self.applicant_info['last_name']}"),
        ]
        
        for selector, value in name_fields:
            try:
                if page.locator(selector).count() > 0:
                    page.locator(selector).first.fill(value, timeout=2000)
                    filled = True
                    logger.info("  ✓ Filled name")
                    break
            except:
                continue
        
        # Email
        email_selectors = ["input[type='email']", "input[name*='email' i]"]
        for selector in email_selectors:
            try:
                if page.locator(selector).count() > 0:
                    page.locator(selector).first.fill(self.applicant_info['email'], timeout=2000)
                    filled = True
                    logger.info("  ✓ Filled email")
                    break
            except:
                continue
        
        # Phone
        phone_selectors = ["input[type='tel']", "input[name*='phone' i]", "input[name*='mobile' i]"]
        for selector in phone_selectors:
            try:
                if page.locator(selector).count() > 0:
                    page.locator(selector).first.fill(self.applicant_info['phone'], timeout=2000)
                    filled = True
                    logger.info("  ✓ Filled phone")
                    break
            except:
                continue
        
        return filled
    
    def _try_submit_form(self, page: Page) -> bool:
        """Try to submit the application form."""
        submit_selectors = [
            "button[type='submit']",
            "button:has-text('Submit')",
            "button:has-text('Apply')",
            "input[type='submit']",
        ]
        
        for selector in submit_selectors:
            try:
                if page.locator(selector).count() > 0:
                    page.locator(selector).first.click(timeout=3000)
                    logger.info("  ✓ Clicked submit")
                    time.sleep(2)
                    return True
            except:
                continue
        
        return False
    
    def search_and_apply_indeed(self, search_query: str, max_applications: int = 10) -> dict[str, Any]:
        """Open Indeed, search jobs, and apply in real-time."""
        logger.info(f"Opening Indeed to search: {search_query}")
        
        results = {
            "source": "Indeed",
            "search_query": search_query,
            "jobs_found": 0,
            "applications_attempted": 0,
            "applications_successful": 0,
            "details": []
        }
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=self.headless, slow_mo=1000)
                context = browser.new_context(viewport={"width": 1280, "height": 900})
                page = context.new_page()
                
                # Go to Indeed India
                logger.info("Navigating to Indeed...")
                page.goto("https://in.indeed.com", timeout=30000)
                time.sleep(3)
                
                # Search for jobs
                logger.info(f"Searching for: {search_query}")
                try:
                    # Find and fill search box
                    search_box = page.locator("input[name='q'], input[id='text-input-what']").first
                    search_box.fill(search_query, timeout=5000)
                    time.sleep(1)
                    
                    # Click search
                    search_btn = page.locator("button[type='submit'], button:has-text('Search')").first
                    search_btn.click(timeout=5000)
                    time.sleep(5)
                    
                    logger.info("Search results loaded")
                    
                    # Find job cards
                    job_cards = page.locator("div.job_seen_beacon, div[class*='job']")
                    job_count = job_cards.count()
                    logger.info(f"Found {job_count} job listings")
                    results["jobs_found"] = job_count
                    
                    # Process jobs similar to Naukri
                    for i in range(min(job_count, max_applications)):
                        try:
                            job_card = job_cards.nth(i)
                            job_card.click(timeout=5000)
                            time.sleep(3)
                            
                            apply_result = self._try_apply_on_page(page, f"Job {i+1}", "Company")
                            results["details"].append(apply_result)
                            
                            if apply_result["status"] == "applied":
                                results["applications_successful"] += 1
                            
                            results["applications_attempted"] += 1
                            time.sleep(3)
                            
                        except Exception as job_error:
                            logger.error(f"Error processing job {i+1}: {job_error}")
                            continue
                
                except Exception as search_error:
                    logger.error(f"Error during search: {search_error}")
                    results["error"] = str(search_error)
                
                logger.info("\nKeeping browser open for 10 seconds...")
                time.sleep(10)
                browser.close()
                
        except Exception as e:
            logger.error(f"Browser automation error: {e}")
            results["error"] = str(e)
        
        return results
    
    def run_live_application_session(self, search_query: str, sources: list[str], max_per_source: int = 5) -> dict:
        """Run live browser session applying to multiple job boards."""
        logger.info("="*80)
        logger.info("STARTING LIVE BROWSER APPLICATION SESSION")
        logger.info("="*80)
        logger.info(f"Search Query: {search_query}")
        logger.info(f"Sources: {', '.join(sources)}")
        logger.info(f"Max per source: {max_per_source}")
        logger.info("="*80)
        
        all_results = []
        
        for source in sources:
            logger.info(f"\n{'='*80}")
            logger.info(f"Processing source: {source}")
            logger.info(f"{'='*80}\n")
            
            if source.lower() == "naukri":
                result = self.search_and_apply_naukri(search_query, max_per_source)
                all_results.append(result)
            elif source.lower() == "indeed":
                result = self.search_and_apply_indeed(search_query, max_per_source)
                all_results.append(result)
            else:
                logger.warning(f"Source {source} not yet implemented for live browser")
        
        # Summary
        total_attempted = sum(r.get("applications_attempted", 0) for r in all_results)
        total_successful = sum(r.get("applications_successful", 0) for r in all_results)
        
        logger.info(f"\n{'='*80}")
        logger.info("SESSION COMPLETE")
        logger.info(f"{'='*80}")
        logger.info(f"Total applications attempted: {total_attempted}")
        logger.info(f"Total applications successful: {total_successful}")
        logger.info(f"{'='*80}\n")
        
        return {
            "status": "completed",
            "search_query": search_query,
            "sources_processed": sources,
            "total_attempted": total_attempted,
            "total_successful": total_successful,
            "details_by_source": all_results
        }
