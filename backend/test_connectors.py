#!/usr/bin/env python3
"""Test script to verify job connectors are working."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.job_discovery.connectors.naukri import NaukriConnector
from app.job_discovery.connectors.indeed import IndeedConnector
from app.job_discovery.connectors.instahyre import InstahyreConnector
from app.job_discovery.connectors.linkedin import LinkedInConnector


def test_connector(connector_class, query="Python Developer"):
    """Test a single connector."""
    print(f"\n{'='*60}")
    print(f"Testing {connector_class.name}")
    print(f"{'='*60}")
    
    try:
        connector = connector_class()
        print(f"Searching for: {query}")
        print("Please wait...")
        
        jobs = connector.fetch_jobs(query=query, limit=5)
        
        print(f"\n✓ Found {len(jobs)} jobs\n")
        
        for i, job in enumerate(jobs, 1):
            print(f"{i}. {job.get('title', 'N/A')}")
            print(f"   Company: {job.get('company', 'N/A')}")
            print(f"   Location: {job.get('location', 'N/A')}")
            print(f"   URL: {job.get('url', 'N/A')[:80]}...")
            print()
        
        return len(jobs)
    
    except Exception as e:
        print(f"\n✗ Error: {e}\n")
        return 0


def main():
    print("="*60)
    print("Huntify - Job Connector Test")
    print("="*60)
    print("\nThis script tests if job scrapers are working correctly.\n")
    
    query = input("Enter job search query (default: Python Backend Developer): ").strip()
    if not query:
        query = "Python Backend Developer"
    
    connectors = [
        NaukriConnector,
        InstahyreConnector,
        IndeedConnector,
        LinkedInConnector,
    ]
    
    results = {}
    for connector_class in connectors:
        count = test_connector(connector_class, query)
        results[connector_class.name] = count
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    total = sum(results.values())
    print(f"Total jobs found: {total}\n")
    
    for name, count in results.items():
        status = "✓" if count > 0 else "✗"
        print(f"{status} {name}: {count} jobs")
    
    print("\n" + "="*60)
    
    if total > 0:
        print("\n✓ Connectors are working! You can now run:")
        print("  python run_auto_apply.py --max-jobs 5 --no-auto-submit\n")
    else:
        print("\n⚠ No jobs found. This could be due to:")
        print("  - Network issues")
        print("  - Website changes (scrapers need update)")
        print("  - Rate limiting\n")


if __name__ == '__main__':
    main()
