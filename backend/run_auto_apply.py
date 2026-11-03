#!/usr/bin/env python3
"""Command-line interface for automated job applications."""
import argparse
import logging
import sys
from pathlib import Path

# Add parent dir to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from app.autonomous.auto_agent import run_fully_automated_hunt

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('huntify_automation.log')
    ]
)

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Huntify - Automated Job Application System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with default settings (visible browser, all sources)
  python run_auto_apply.py
  
  # Apply to 5 jobs with minimum 70% match score
  python run_auto_apply.py --max-jobs 5 --min-score 0.70
  
  # Run in headless mode (no visible browser)
  python run_auto_apply.py --headless
  
  # Use specific job sources only
  python run_auto_apply.py --sources "LinkedIn,Naukri,Indeed"
  
  # Prepare applications without auto-submitting
  python run_auto_apply.py --no-auto-submit
        """
    )
    
    parser.add_argument(
        '--max-jobs',
        type=int,
        default=10,
        help='Maximum number of jobs to apply to (default: 10)'
    )
    
    parser.add_argument(
        '--min-score',
        type=float,
        default=0.60,
        help='Minimum match score to apply (0.0-1.0, default: 0.60)'
    )
    
    parser.add_argument(
        '--headless',
        action='store_true',
        help='Run browser in headless mode (no visible window)'
    )
    
    parser.add_argument(
        '--no-auto-submit',
        action='store_true',
        help='Prepare applications but do not auto-submit'
    )
    
    parser.add_argument(
        '--sources',
        type=str,
        default=None,
        help='Comma-separated list of job sources (e.g., "LinkedIn,Naukri,Indeed")'
    )
    
    parser.add_argument(
        '--resume',
        type=str,
        default=None,
        help='Path to your resume file (default: storage/master_resume/base_resume.txt)'
    )
    
    args = parser.parse_args()
    
    # Parse sources
    sources = None
    if args.sources:
        sources = [s.strip() for s in args.sources.split(',')]
    
    # Display configuration
    logger.info("="*80)
    logger.info("HUNTIFY - AUTOMATED JOB APPLICATION SYSTEM")
    logger.info("="*80)
    logger.info(f"Configuration:")
    logger.info(f"  Max Jobs: {args.max_jobs}")
    logger.info(f"  Min Match Score: {args.min_score}")
    logger.info(f"  Browser Mode: {'Headless' if args.headless else 'Visible'}")
    logger.info(f"  Auto Submit: {not args.no_auto_submit}")
    logger.info(f"  Sources: {sources if sources else 'All available'}")
    logger.info(f"  Resume: {args.resume if args.resume else 'Default'}")
    logger.info("="*80 + "\n")
    
    # Confirm before starting
    if not args.no_auto_submit:
        response = input("⚠️  Auto-submit is ENABLED. Applications will be submitted automatically. Continue? (yes/no): ")
        if response.lower() not in ['yes', 'y']:
            logger.info("Aborted by user")
            return
    
    try:
        # Run automated job hunt
        result = run_fully_automated_hunt(
            base_resume_path=args.resume,
            sources=sources,
            min_match_score=args.min_score,
            max_applications=args.max_jobs,
            headless=args.headless,
            auto_submit=not args.no_auto_submit,
        )
        
        # Display results
        logger.info("\n" + "="*80)
        logger.info("FINAL RESULTS")
        logger.info("="*80)
        logger.info(f"Status: {result['status']}")
        logger.info(f"Jobs Evaluated: {result['jobs_evaluated']}")
        logger.info(f"Jobs Matched: {result.get('jobs_matched', 0)}")
        logger.info(f"Applications: {result['applications_submitted']}")
        
        if result.get('applications'):
            logger.info("\nApplication Details:")
            for i, app in enumerate(result['applications'], 1):
                status_emoji = {
                    'submitted': '✓',
                    'partially_completed': '⚠',
                    'failed': '✗',
                    'ready_for_review': '📋',
                }.get(app['status'], '?')
                
                logger.info(f"\n  {i}. {status_emoji} {app['job_title']} at {app['company']}")
                logger.info(f"     Status: {app['status']}")
                if 'url' in app:
                    logger.info(f"     URL: {app['url']}")
                if 'note' in app:
                    logger.info(f"     Note: {app['note']}")
        
        logger.info("\n" + "="*80)
        logger.info(f"Log file saved to: huntify_automation.log")
        logger.info("="*80 + "\n")
        
    except KeyboardInterrupt:
        logger.info("\n\nProcess interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"\nError during automation: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
