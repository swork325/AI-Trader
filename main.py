"""AI-Trader: An AI-powered trading agent system.

This is the main entry point for the AI-Trader application.
It initializes the environment, sets up the trading agent, and starts
the main execution loop.
"""

import os
import sys
import argparse
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("ai-trader")


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="AI-Trader: AI-powered stock trading agent",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=["backtest", "paper", "live"],
        default="paper",
        help="Trading mode: backtest (historical), paper (simulated), or live",
    )
    parser.add_argument(
        "--ticker",
        type=str,
        default=None,
        help="Stock ticker symbol(s) to trade, comma-separated (e.g. AAPL,TSLA)",
    )
    parser.add_argument(
        "--start-date",
        type=str,
        default=None,
        help="Start date for backtesting (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--end-date",
        type=str,
        default=None,
        help="End date for backtesting (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config.yaml",
        help="Path to configuration file",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        default=False,
        help="Enable verbose/debug logging",
    )
    return parser.parse_args()


def validate_environment() -> bool:
    """Validate that required environment variables are set."""
    required_vars = [
        "OPENAI_API_KEY",
    ]
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        logger.error(
            "Missing required environment variables: %s", ", ".join(missing)
        )
        logger.error("Please copy .env.example to .env and fill in the required values.")
        return False
    return True


def main() -> int:
    """Main entry point for AI-Trader."""
    args = parse_args()

    # Set log level based on verbosity flag
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Verbose logging enabled.")

    logger.info("Starting AI-Trader (mode=%s)", args.mode)

    # Validate environment before proceeding
    if not validate_environment():
        return 1

    # Parse tickers
    tickers = (
        [t.strip().upper() for t in args.ticker.split(",")]
        if args.ticker
        else []
    )

    if not tickers:
        logger.warning("No ticker symbols provided. Use --ticker to specify symbols.")

    logger.info("Tickers: %s", tickers if tickers else "(none specified)")
    logger.info("Config file: %s", args.config)

    if args.mode == "backtest":
        if not args.start_date or not args.end_date:
            logger.error("Backtest mode requires --start-date and --end-date.")
            return 1
        logger.info(
            "Backtest period: %s to %s", args.start_date, args.end_date
        )

    # TODO: Initialize agent and run trading loop
    logger.info("AI-Trader initialized successfully. Agent module coming soon.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
