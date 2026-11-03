#!/usr/bin/env python3
"""Simple synchronous job application - no async, works on Windows."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import logging
import time
from playwright.sync_api import sync_playwright

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Your info
APPLICANT_INFO = {
    "name": "Aakash Sehrawat",
    "email": "aakashhssehrawat@gmail.com",
    "phone": "+91 9217030815",
}

def apply_to_naukri_jobs(search_query="Python Developer", max_jobs=3):
    """Open Naukri, search, and try to apply to jobs."""
    
    logger.info("="*80)
    logger.info("HUNTIFY - LIVE BROWSER APPLICATION")
    logger.info("="*80)
    logger.info(f"Opening Naukri.com...")
    logger.info(f"Search: {search_query}")
    logger.info(f"Max jobs: {max_jobs}")
    logger.info("="*80)
    
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        
        # Go to Naukri
        logger.info("\n[1/4] Navigating to Naukri.com...")
        page.goto("https://www.naukri.com", timeout=30000)
        time.sleep(3)
        
        # Search
        logger.info(f"\n[2/4] Searching for: {search_query}")
        try:
            # Wait for page to load
            time.sleep(2)
            
            # Try different search box selectors
            search_selectors = [
                "input[placeholder*='skill' i]",
                "input[placeholder*='designation' i]",
                "input[class*='suggestor-input']",
                "input[type='text']",
            ]
            
            search_filled = False
            for selector in search_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        logger.info(f"  Found search box: {selector}")
                        page.locator(selector).first.fill(search_query)
                        search_filled = True
                        break
                except:
                    continue
            
            if not search_filled:
                logger.warning("Could not find search box - using URL search instead")
                # Use URL-based search as fallback
                search_url = f"https://www.naukri.com/{search_query.replace(' ', '-')}-jobs"
                logger.info(f"  Going to: {search_url}")
                page.goto(search_url, timeout=30000)
                time.sleep(5)
                logger.info("✓ Search page loaded")
            else:
                time.sleep(1)
                
                # Click search button
                search_btn_selectors = [
                    "button:has-text('Search')",
                    "button[type='submit']",
                    "button[class*='search']",
                ]
                
                for selector in search_btn_selectors:
                    try:
                        if page.locator(selector).count() > 0:
                            logger.info(f"  Clicking search button: {selector}")
                            page.locator(selector).first.click()
                            break
                    except:
                        continue
                
                time.sleep(5)
                logger.info("✓ Search results loaded")
        except Exception as e:
            logger.error(f"Search failed: {e}")
            browser.close()
            return
        
        # Find jobs
        logger.info(f"\n[3/4] Finding job listings...")
        
        # Try different job card selectors
        job_card_selectors = [
            "article.jobTuple",
            "div[class*='jobTuple']",
            "div[class*='job-card']",
            "article",
        ]
        
        job_cards = None
        for selector in job_card_selectors:
            cards = page.locator(selector)
            if cards.count() > 0:
                job_cards = cards
                logger.info(f"✓ Found {cards.count()} jobs using selector: {selector}")
                break
        
        if not job_cards or job_cards.count() == 0:
            logger.error("No job listings found on page")
            browser.close()
            return
        
        count = job_cards.count()
        
        # Apply to jobs
        logger.info(f"\n[4/4] Applying to jobs...")
        applied = 0
        
        for i in range(min(count, max_jobs)):
            try:
                logger.info(f"\n{'='*60}")
                logger.info(f"Job {i+1}/{min(count, max_jobs)}")
                logger.info(f"{'='*60}")
                
                # Get job info
                card = job_cards.nth(i)
                try:
                    title = card.locator("a.title").first.text_content() or "Unknown"
                    company = card.locator("a.subTitle").first.text_content() or "Unknown"
                    logger.info(f"Position: {title}")
                    logger.info(f"Company: {company}")
                except:
                    logger.info("Position: Unknown job")
                
                # Click job
                card.click()
                time.sleep(3)
                
                # Try to apply
                try:
                    apply_btn = page.locator("button:has-text('Apply')").first
                    if apply_btn.count() > 0:
                        logger.info("Found Apply button - clicking...")
                        apply_btn.click(timeout=3000)
                        time.sleep(2)
                        
                        # Fill form if present
                        try:
                            if page.locator("input[name*='name']").count() > 0:
                                page.locator("input[name*='name']").first.fill(APPLICANT_INFO["name"])
                                logger.info("  ✓ Filled name")
                            
                            if page.locator("input[type='email']").count() > 0:
                                page.locator("input[type='email']").first.fill(APPLICANT_INFO["email"])
                                logger.info("  ✓ Filled email")
                            
                            if page.locator("input[type='tel']").count() > 0:
                                page.locator("input[type='tel']").first.fill(APPLICANT_INFO["phone"])
                                logger.info("  ✓ Filled phone")
                            
                            # Submit
                            if page.locator("button[type='submit']").count() > 0:
                                page.locator("button[type='submit']").first.click()
                                logger.info("  ✓ Clicked submit")
                                applied += 1
                        except Exception as fill_error:
                            logger.warning(f"  ⚠ Form fill error: {fill_error}")
                        
                        logger.info("✓ Application attempted")
                    else:
                        logger.info("○ No apply button found")
                except Exception as apply_error:
                    logger.warning(f"✗ Apply failed: {apply_error}")
                
                time.sleep(2)
                
            except Exception as job_error:
                logger.error(f"Error processing job {i+1}: {job_error}")
                continue
        
        # Summary
        logger.info("\n" + "="*80)
        logger.info("SUMMARY")
        logger.info("="*80)
        logger.info(f"Jobs processed: {min(count, max_jobs)}")
        logger.info(f"Applications attempted: {applied}")
        logger.info("="*80)
        
        logger.info("\nBrowser will stay open for 10 seconds...")
        time.sleep(10)
        
        browser.close()
        logger.info("\n✓ Done!")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Simple Naukri job application")
    parser.add_argument("--query", default="Python Developer", help="Search query")
    parser.add_argument("--max", type=int, default=3, help="Max jobs to apply")
    
    args = parser.parse_args()
    
    try:
        apply_to_naukri_jobs(args.query, args.max)
    except KeyboardInterrupt:
        print("\n\nStopped by user")
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()
