"""
Utility functions for Instagram Scraper.

Provides helper functions for rate limiting, retry logic, proxy management,
logging, and data formatting.
"""

import time
import random
import logging
import functools
from typing import Callable, Optional

logger = logging.getLogger("ig_scraper")


def setup_logging(level: str = "INFO", filename: Optional[str] = None):
    """Configure logging for the scraper.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR).
        filename: Optional file to write logs to.
    """
    levels = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
    }
    log_level = levels.get(level.upper(), logging.INFO)

    handlers = [logging.StreamHandler()]
    if filename:
        handlers.append(logging.FileHandler(filename, encoding="utf-8"))

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=handlers,
    )


def rate_limit(min_delay: float = 1.0, max_delay: float = 3.0):
    """Decorator that adds random delay between function calls.

    Args:
        min_delay: Minimum delay in seconds.
        max_delay: Maximum delay in seconds.
    """

    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            delay = random.uniform(min_delay, max_delay)
            logger.debug(f"Rate limiting: sleeping {delay:.2f}s")
            time.sleep(delay)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def retry(max_retries: int = 3, backoff_factor: float = 2.0):
    """Decorator that retries a function on failure with exponential backoff.

    Args:
        max_retries: Maximum number of retry attempts.
        backoff_factor: Multiplier for exponential backoff.
    """

    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries:
                        wait = backoff_factor ** attempt
                        logger.warning(
                            f"Attempt {attempt + 1}/{max_retries + 1} failed: {e}. "
                            f"Retrying in {wait:.1f}s..."
                        )
                        time.sleep(wait)
                    else:
                        logger.error(f"All {max_retries + 1} attempts failed.")
            raise last_exception

        return wrapper

    return decorator


def format_number(n: int) -> str:
    """Format large numbers for display (e.g., 1.2M, 3.5K).

    Args:
        n: Number to format.

    Returns:
        Formatted string.
    """
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    elif n >= 1_000:
        return f"{n / 1_000:.1f}K"
    else:
        return str(n)


def parse_hashtags(caption: str) -> list:
    """Extract hashtags from a caption string.

    Args:
        caption: Instagram post caption text.

    Returns:
        List of hashtags (without the # symbol).
    """
    if not caption:
        return []
    import re
    return re.findall(r"#(\w+)", caption)


def parse_mentions(caption: str) -> list:
    """Extract @mentions from a caption string.

    Args:
        caption: Instagram post caption text.

    Returns:
        List of mentioned usernames (without the @ symbol).
    """
    if not caption:
        return []
    import re
    return re.findall(r"@(\w+)", caption)


def sanitize_filename(filename: str) -> str:
    """Sanitize a string for use as a filename.

    Args:
        filename: Raw filename string.

    Returns:
        Sanitized filename safe for filesystem.
    """
    import re
    # Remove or replace unsafe characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    sanitized = sanitized.strip().rstrip('.')
    return sanitized[:200] if len(sanitized) > 200 else sanitized


class ProgressBar:
    """Simple text-based progress bar for batch operations."""

    def __init__(self, total: int, description: str = "Scraping"):
        self.total = total
        self.current = 0
        self.description = description
        self.bar_length = 40

    def update(self, n: int = 1):
        self.current += n
        self._render()

    def _render(self):
        filled = int(self.bar_length * self.current / self.total) if self.total > 0 else 0
        bar = "=" * filled + "-" * (self.bar_length - filled)
        percent = f"{100 * self.current / self.total:.1f}%" if self.total > 0 else "0%"
        print(
            f"\r{self.description}: [{bar}] {percent} ({self.current}/{self.total})",
            end="", flush=True,
        )
        if self.current >= self.total:
            print()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        if self.current < self.total:
            print()
