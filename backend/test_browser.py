#!/usr/bin/env python3
"""Simple test to verify browser automation works."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from playwright.sync_api import sync_playwright
import time

print("Testing Playwright browser automation...")
print("="*60)

try:
    with sync_playwright() as p:
        print("✓ Playwright imported successfully")
        
        print("Launching browser...")
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        print("✓ Browser launched")
        
        context = browser.new_context()
        page = context.new_page()
        print("✓ Page created")
        
        print("\nNavigating to Google...")
        page.goto("https://www.google.com", timeout=30000)
        print("✓ Page loaded")
        
        print("\nBrowser will close in 5 seconds...")
        time.sleep(5)
        
        browser.close()
        print("✓ Browser closed")
        
    print("\n" + "="*60)
    print("✅ SUCCESS! Browser automation is working!")
    print("="*60)
    print("\nYou can now use the auto-apply feature.")
    
except Exception as e:
    print("\n" + "="*60)
    print("❌ ERROR! Browser automation failed:")
    print(f"{e}")
    print("="*60)
    print("\nTry running: playwright install chromium")
    sys.exit(1)
