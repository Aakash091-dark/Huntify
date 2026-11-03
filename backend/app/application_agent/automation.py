from __future__ import annotations

from typing import Any

from playwright.sync_api import sync_playwright


class BrowserApplicationAgent:
    def __init__(self, headless: bool = True):
        self.headless = headless

    def apply_to_job(self, job: dict[str, Any], resume_path: str):
        url = job.get("url") or "https://example.com/apply"
        if url.startswith("https://example.com") or url.startswith("http://example.com"):
            url = "about:blank"
        form_data = {
            "first_name": "Aakash",
            "last_name": "Sehrawat",
            "email": "aakashhssehrawat@gmail.com",
            "phone": "+91 9217030815",
            "resume": resume_path,
        }

        try:
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(headless=self.headless)
                page = browser.new_page()
                page.goto(url, wait_until="domcontentloaded", timeout=10000)

                for selector, value in [
                    ("input[name='first_name']", form_data["first_name"]),
                    ("input[name='lastName']", form_data["last_name"]),
                    ("input[name='email']", form_data["email"]),
                    ("input[name='phone']", form_data["phone"]),
                ]:
                    try:
                        locator = page.locator(selector)
                        if locator.count() > 0:
                            locator.first.fill(value, timeout=2000)
                    except Exception:
                        continue

                for selector in [
                    "input[type='file']",
                    "textarea",
                    "button[type='submit']",
                ]:
                    try:
                        locator = page.locator(selector).first
                        if locator.count() == 0:
                            continue
                        if selector == "input[type='file']":
                            locator.set_input_files(resume_path, timeout=2000)
                        elif selector == "button[type='submit']":
                            locator.click(timeout=5000)
                        else:
                            locator.fill(form_data["email"], timeout=2000)
                    except Exception:
                        continue

                browser.close()
                status = "browser_submission_attempted"
                note = "Browser automation attempted; manual review is still required on protected/anti-bot flows."
        except Exception as exc:
            status = "browser_not_available"
            note = f"Browser automation could not run because the Playwright browser runtime is unavailable: {exc}"

        return {
            "status": status,
            "job_title": job.get("title", "Open Role"),
            "company": job.get("company", "Target Company"),
            "url": url,
            "resume_path": resume_path,
            "note": note,
        }
