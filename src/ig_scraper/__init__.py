"""
Instagram Account Scraper - Core scraper module.

A lightweight Python library and CLI tool for scraping public Instagram
account data: profile info, posts, reels, stories, hashtags, and followers.
"""

from ig_scraper.scraper import InstagramScraper
from ig_scraper.models import Profile, Post, Story, Reel
from ig_scraper.exceptions import (
    InstagramScraperError,
    LoginRequiredError,
    RateLimitError,
    ProfileNotFoundError,
    PrivateProfileError,
)

__version__ = "1.0.0"
__author__ = "Instagram Scraper Contributors"
__license__ = "MIT"

__all__ = [
    "InstagramScraper",
    "Profile",
    "Post",
    "Story",
    "Reel",
    "InstagramScraperError",
    "LoginRequiredError",
    "RateLimitError",
    "ProfileNotFoundError",
    "PrivateProfileError",
    "__version__",
]
