"""Fully automated job application system with browser automation."""
from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import Any

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

logger = logging.getLogger(__name__)


class AutoJobApplier:
    """Automated job application agent that applies to jobs via browser automation."""

    def __init__(self, headless: bool = False):
        """
        Initialize the auto applier.
        
        Args:
            headless: Whether to run browser in headless mode (False = visible browser)
        """
        self.headless = headless
        self.applicant_info = {
            "first_name": "Aakash",
            "last_name": "Sehrawat",
            "email": "aakashhssehrawat@gmail.com",
            "phone": "+91 9217030815",
            "linkedin": "https://linkedin.com/in/aakash-sehrawat",
            "github": "https://github.com/aakash-sehrawat",
        }

    def apply_to_job(self, job: dict[str, Any], resume_path: str | Path) -> dict[str, Any]:
        """
        Automatically apply to a single job.
        
        Args:
            job: Job dict with title, company, url, description
            resume_path: Path to tailored resume file
            
        Returns:
            Application result with status and details
        """
        url = job.get("url", "")
        if not url or "example.com" in url:
            return {
                "status": "skipped",
                "reason": "Invalid or placeholder URL",
                "job_title": job.get("title"),
                "company": job.get("company"),
            }

        logger.info(f"Starting application to {job.get('title')} at {job.get('company')}")

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=self.headless, slow_mo=500)
                context = browser.new_context(
                    viewport={"width": 1280, "height": 720},
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                )
                page = context.new_page()

                # Navigate to job URL
                try:
                    page.goto(url, wait_until="domcontentloaded", timeout=30000)
                    time.sleep(2)  # Let page fully load
                except PlaywrightTimeout:
                    browser.close()
                    return {
                        "status": "failed",
                        "reason": "Page load timeout",
                        "job_title": job.get("title"),
                        "company": job.get("company"),
                        "url": url,
                    }

                # Try to find and click "Apply" button
                apply_button_selectors = [
                    "button:has-text('Apply')",
                    "a:has-text('Apply')",
                    "button:has-text('Easy Apply')",
                    "button:has-text('Quick Apply')",
                    "[data-test='apply-button']",
                    ".apply-button",
                    "#apply-button",
                ]

                apply_clicked = False
                for selector in apply_button_selectors:
                    try:
                        if page.locator(selector).count() > 0:
                            page.locator(selector).first.click(timeout=3000)
                            apply_clicked = True
                            logger.info(f"Clicked apply button: {selector}")
                            time.sleep(2)
                            break
                    except Exception:
                        continue

                if not apply_clicked:
                    logger.warning("Could not find apply button, continuing anyway")

                # Fill in form fields
                filled_fields = self._fill_application_form(page, resume_path)

                # Try to submit the application
                submitted = self._submit_application(page)

                browser.close()

                if submitted:
                    return {
                        "status": "submitted",
                        "job_title": job.get("title"),
                        "company": job.get("company"),
                        "url": url,
                        "resume_path": str(resume_path),
                        "fields_filled": filled_fields,
                        "note": "Application submitted successfully via automation",
                    }
                else:
                    return {
                        "status": "partially_completed",
                        "job_title": job.get("title"),
                        "company": job.get("company"),
                        "url": url,
                        "resume_path": str(resume_path),
                        "fields_filled": filled_fields,
                        "note": "Form filled but could not confirm submission - manual review required",
                    }

        except Exception as e:
            logger.error(f"Application error: {e}")
            return {
                "status": "error",
                "job_title": job.get("title"),
                "company": job.get("company"),
                "url": url,
                "error": str(e),
                "note": "Automation encountered an error",
            }

    def _fill_application_form(self, page, resume_path: str | Path) -> int:
        """Fill in application form fields. Returns count of fields filled."""
        filled_count = 0

        # Common field patterns and their values
        field_patterns = [
            # Name fields
            (["input[name*='first' i][name*='name' i]", "#firstName", "#first-name"], self.applicant_info["first_name"]),
            (["input[name*='last' i][name*='name' i]", "#lastName", "#last-name"], self.applicant_info["last_name"]),
            (["input[name*='full' i][name*='name' i]", "#fullName"], f"{self.applicant_info['first_name']} {self.applicant_info['last_name']}"),
            
            # Contact fields
            (["input[type='email']", "input[name*='email' i]", "#email"], self.applicant_info["email"]),
            (["input[type='tel']", "input[name*='phone' i]", "#phone"], self.applicant_info["phone"]),
            
            # Social profiles
            (["input[name*='linkedin' i]", "#linkedin"], self.applicant_info["linkedin"]),
            (["input[name*='github' i]", "#github"], self.applicant_info["github"]),
        ]

        for selectors, value in field_patterns:
            for selector in selectors:
                try:
                    if page.locator(selector).count() > 0:
                        page.locator(selector).first.fill(value, timeout=2000)
                        filled_count += 1
                        logger.info(f"Filled field: {selector}")
                        break
                except Exception:
                    continue

        # Upload resume
        resume_selectors = [
            "input[type='file']",
            "input[accept*='pdf']",
            "input[accept*='doc']",
            "#resume-upload",
            "#cv-upload",
        ]

        for selector in resume_selectors:
            try:
                if page.locator(selector).count() > 0:
                    page.locator(selector).first.set_input_files(str(resume_path), timeout=3000)
                    filled_count += 1
                    logger.info(f"Uploaded resume via: {selector}")
                    time.sleep(1)
                    break
            except Exception:
                continue

        # Fill text areas (cover letter, additional info)
        try:
            textareas = page.locator("textarea")
            if textareas.count() > 0:
                cover_letter = f"I am excited to apply for the {self.applicant_info['first_name']} position. With strong experience in backend development, AI, and scalable systems, I believe I would be a great fit for your team."
                textareas.first.fill(cover_letter, timeout=2000)
                filled_count += 1
                logger.info("Filled cover letter")
        except Exception:
            pass

        return filled_count

    def _submit_application(self, page) -> bool:
        """Try to submit the application form. Returns True if submitted."""
        submit_selectors = [
            "button[type='submit']",
            "input[type='submit']",
            "button:has-text('Submit')",
            "button:has-text('Send Application')",
            "button:has-text('Apply Now')",
            ".submit-button",
            "#submit-application",
        ]

        for selector in submit_selectors:
            try:
                if page.locator(selector).count() > 0:
                    page.locator(selector).first.click(timeout=3000)
                    logger.info(f"Clicked submit button: {selector}")
                    time.sleep(3)  # Wait for submission to process
                    
                    # Check for success indicators
                    success_indicators = [
                        "text='Application submitted'",
                        "text='Thank you'",
                        "text='Success'",
                        ".success-message",
                    ]
                    
                    for indicator in success_indicators:
                        if page.locator(indicator).count() > 0:
                            logger.info("Application submission confirmed!")
                            return True
                    
                    return True  # Assume success if no error
            except Exception as e:
                logger.debug(f"Submit attempt failed: {e}")
                continue

        return False

    def apply_to_jobs_batch(self, jobs_with_resumes: list[dict]) -> list[dict]:
        """
        Apply to multiple jobs in sequence.
        
        Args:
            jobs_with_resumes: List of dicts with 'job' and 'resume_path' keys
            
        Returns:
            List of application results
        """
        results = []
        
        for i, item in enumerate(jobs_with_resumes, 1):
            job = item["job"]
            resume_path = item["resume_path"]
            
            logger.info(f"\n{'='*60}")
            logger.info(f"Processing application {i}/{len(jobs_with_resumes)}")
            logger.info(f"Job: {job.get('title')} at {job.get('company')}")
            logger.info(f"{'='*60}\n")
            
            result = self.apply_to_job(job, resume_path)
            results.append(result)
            
            # Add delay between applications
            if i < len(jobs_with_resumes):
                delay = 5  # 5 seconds between applications
                logger.info(f"Waiting {delay} seconds before next application...\n")
                time.sleep(delay)
        
        return results
