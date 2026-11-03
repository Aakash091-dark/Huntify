#!/usr/bin/env python3
"""Live browser application - opens job boards and applies in real-time."""
import argparse
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.application_agent.live_browser_agent import LiveBrowserAgent

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('huntify_live_browser.log')
    ]
)

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Huntify Live Browser - Apply to jobs in real-time",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Search and apply on Naukri
  python run_live_browser.py --query "Python Developer" --sources Naukri --max 5
  
  # Multiple sources
  python run_live_browser.py --query "Backend Engineer" --sources "Naukri,Indeed" --max 3
  
  # Hidden browser mode
  python run_live_browser.py --query "Python Developer" --headless
        """
    )
    
    parser.add_argument(
        '--query',
        type=str,
        default="Python Backend Developer",
        help='Job search query (default: "Python Backend Developer")'
    )
    
    parser.add_argument(
        '--sources',
        type=str,
        default="Naukri",
        help='Comma-separated job sources: Naukri,Indeed (default: Naukri)'
    )
    
    parser.add_argument(
        '--max',
        type=int,
        default=5,
        help='Maximum applications per source (default: 5)'
    )
    
    parser.add_argument(
        '--headless',
        action='store_true',
        help='Run browser in headless mode'
    )
    
    args = parser.parse_args()
    
    sources = [s.strip() for s in args.sources.split(',')]
    
    logger.info("="*80)
    logger.info("HUNTIFY LIVE BROWSER APPLICATION")
    logger.info("="*80)
    logger.info(f"Search Query: {args.query}")
    logger.info(f"Sources: {', '.join(sources)}")
    logger.info(f"Max per source: {args.max}")
    logger.info(f"Browser Mode: {'Headless' if args.headless else 'Visible'}")
    logger.info("="*80 + "\n")
    
    if not args.headless:
        response = input("⚠️  Browser will open and apply to jobs automatically. Continue? (yes/no): ")
        if response.lower() not in ['yes', 'y']:
            logger.info("Aborted by user")
            return
    
    try:
        agent = LiveBrowserAgent(headless=args.headless)
        result = agent.run_live_application_session(
            search_query=args.query,
            sources=sources,
            max_per_source=args.max
        )
        
        logger.info("\n" + "="*80)
        logger.info("FINAL RESULTS")
        logger.info("="*80)
        logger.info(f"Total Attempted: {result['total_attempted']}")
        logger.info(f"Total Successful: {result['total_successful']}")
        logger.info(f"Log saved to: huntify_live_browser.log")
        logger.info("="*80 + "\n")
        
    except KeyboardInterrupt:
        logger.info("\n\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"\nError: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
