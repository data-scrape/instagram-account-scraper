"""
Instagram Account Scraper - Command Line Interface.

Provides a full-featured CLI for scraping Instagram data from the terminal.

Usage:
    ig-scraper profile <username> [options]
    ig-scraper posts <username> [--limit 10] [options]
    ig-scraper reels <username> [--limit 5] [options]
    ig-scraper hashtag <tag> [--limit 20] [options]
    ig-scraper batch <file> [--limit 5] [options]
    ig-scraper emails <username> [options]
    ig-scraper all <username> [options]

Options:
    --login USERNAME PASSWORD    Login credentials
    --session FILE               Session file path
    --proxy URL                  Proxy server URL
    --output FILE                Output file path
    --format json|csv|excel      Output format (default: json)
    --delay SECONDS              Rate limit delay (default: 2.0)
    --quiet                      Suppress progress output
"""

import argparse
import json
import sys
import os
import logging

from ig_scraper import __version__
from ig_scraper.scraper import InstagramScraper
from ig_scraper.models import DataExporter
from ig_scraper.exceptions import (
    InstagramScraperError,
    LoginRequiredError,
    ProfileNotFoundError,
    PrivateProfileError,
)
from ig_scraper.utils import setup_logging


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="ig-scraper",
        description=(
            "Instagram Account Scraper - Scrape public Instagram profiles, "
            "posts, reels, stories, hashtags, and follower data."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  ig-scraper profile nasa\n"
            "  ig-scraper posts nasa --limit 10 --output nasa_posts.json\n"
            '  ig-scraper profile nasa --format csv --output nasa.csv\n'
            '  ig-scraper batch users.txt --limit 5 --output results.json\n'
            '  ig-scraper --login user pass emails somebusiness\n'
            '  ig-scraper hashtag travel --limit 20\n'
        ),
    )

    parser.add_argument(
        "--version", action="version", version=f"ig-scraper {__version__}"
    )

    subparsers = parser.add_subparsers(dest="command", help="Scraping command")

    # Profile command
    p_profile = subparsers.add_parser("profile", help="Scrape profile information")
    _add_common_options(p_profile)
    p_profile.add_argument("username", help="Instagram username")
    p_profile.add_argument("--fields", help="Comma-separated fields to show")

    # Posts command
    p_posts = subparsers.add_parser("posts", help="Scrape recent posts")
    _add_common_options(p_posts)
    p_posts.add_argument("username", help="Instagram username")
    p_posts.add_argument("--limit", type=int, default=12, help="Max posts (default: 12)")
    p_posts.add_argument("--reels", action="store_true", help="Only get reels")
    p_posts.add_argument("--no-reels", action="store_true", help="Exclude reels")

    # Reels command
    p_reels = subparsers.add_parser("reels", help="Scrape recent reels")
    _add_common_options(p_reels)
    p_reels.add_argument("username", help="Instagram username")
    p_reels.add_argument("--limit", type=int, default=12, help="Max reels (default: 12)")

    # Stories command
    p_stories = subparsers.add_parser("stories", help="Scrape active stories")
    _add_common_options(p_stories)
    p_stories.add_argument("usernames", nargs="+", help="Instagram usernames")

    # Hashtag command
    p_hashtag = subparsers.add_parser("hashtag", help="Scrape posts by hashtag")
    _add_common_options(p_hashtag)
    p_hashtag.add_argument("hashtag", help="Hashtag (without #)")
    p_hashtag.add_argument("--limit", type=int, default=20, help="Max posts (default: 20)")

    # Followers command
    p_followers = subparsers.add_parser("followers", help="Get followers list")
    _add_common_options(p_followers)
    p_followers.add_argument("username", help="Instagram username")
    p_followers.add_argument("--limit", type=int, default=100, help="Max followers")

    # Following command
    p_following = subparsers.add_parser("following", help="Get following list")
    _add_common_options(p_following)
    p_following.add_argument("username", help="Instagram username")
    p_following.add_argument("--limit", type=int, default=100, help="Max following")

    # Emails command
    p_emails = subparsers.add_parser("emails", help="Extract emails from profile")
    _add_common_options(p_emails)
    p_emails.add_argument("username", help="Instagram username")
    p_emails.add_argument("--posts", type=int, default=50, help="Posts to scan")

    # Batch command
    p_batch = subparsers.add_parser("batch", help="Batch scrape multiple accounts")
    _add_common_options(p_batch)
    p_batch.add_argument("file", help="Text file with usernames (one per line)")
    p_batch.add_argument("--limit", type=int, default=5, help="Posts per account")

    # All command
    p_all = subparsers.add_parser("all", help="Scrape all available data for account")
    _add_common_options(p_all)
    p_all.add_argument("username", help="Instagram username")
    p_all.add_argument("--posts", type=int, default=12, help="Max posts")



def _add_common_options(parser):
    """Add output/format/quiet options to a subparser."""
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument(
        "--format", choices=["json", "csv", "excel"], default="json",
        help="Output format (default: json)",
    )
    parser.add_argument("--quiet", "-q", action="store_true", help="Suppress progress")
    return parser

    # Global options (kept for backward compatibility when used before command)
    parser.add_argument(
        "--login", nargs=2, metavar=("USERNAME", "PASSWORD"),
        help="Instagram login credentials",
    )
    parser.add_argument("--session", help="Session file path")
    parser.add_argument("--proxy", help="Proxy server URL")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument(
        "--format", choices=["json", "csv", "excel"], default="json",
        help="Output format (default: json)",
    )
    parser.add_argument("--delay", type=float, default=2.0, help="Rate limit delay")
    parser.add_argument("--quiet", "-q", action="store_true", help="Suppress progress")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")

    return parser


def main(argv=None):
    """Main CLI entry point."""
    parser = build_parser()
    args = parser.parse_args(argv)

    # Setup logging
    level = "DEBUG" if args.debug else ("ERROR" if args.quiet else "INFO")
    setup_logging(level=level)

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Initialize scraper
    try:
        username, password = args.login if args.login else (None, None)
        scraper = InstagramScraper(
            username=username,
            password=password,
            session_file=args.session,
            proxy=args.proxy,
            rate_limit_delay=args.delay,
        )
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        result = dispatch_command(scraper, args)
        output_result(result, args)
    except ProfileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)
    except PrivateProfileError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(3)
    except LoginRequiredError as e:
        print(f"Error: {e}", file=sys.stderr)
        print("Hint: Use --login USERNAME PASSWORD to authenticate", file=sys.stderr)
        sys.exit(4)
    except InstagramScraperError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(5)
    except KeyboardInterrupt:
        print("\nAborted by user.", file=sys.stderr)
        sys.exit(130)


def dispatch_command(scraper: InstagramScraper, args) -> object:
    """Dispatch the appropriate scraping command."""
    cmd = args.command

    if cmd == "profile":
        return scraper.get_profile(args.username)

    elif cmd == "posts":
        if args.reels:
            return scraper.get_reels(args.username, limit=args.limit)
        else:
            return scraper.get_posts(
                args.username, limit=args.limit, only_reels=False
            )

    elif cmd == "reels":
        return scraper.get_reels(args.username, limit=args.limit)

    elif cmd == "stories":
        return scraper.get_stories(args.usernames)

    elif cmd == "hashtag":
        return scraper.get_hashtag_posts(args.hashtag, limit=args.limit)

    elif cmd == "followers":
        return scraper.get_followers(args.username, limit=args.limit)

    elif cmd == "following":
        return scraper.get_following(args.username, limit=args.limit)

    elif cmd == "emails":
        return scraper.extract_emails(args.username, posts_limit=args.posts)

    elif cmd == "batch":
        with open(args.file, "r", encoding="utf-8") as f:
            usernames = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        return scraper.batch_scrape(usernames, posts_limit=args.limit)

    elif cmd == "all":
        return scraper.scrape_all(args.username, posts_limit=args.posts)

    else:
        raise ValueError(f"Unknown command: {cmd}")


def output_result(result, args):
    """Format and output the scraping result."""
    if hasattr(result, "to_json"):
        data = result.to_json()
    elif isinstance(result, list):
        if result and hasattr(result[0], "to_dict"):
            data = DataExporter.to_json(result)
        else:
            data = json.dumps(result, indent=2, ensure_ascii=False)
    elif isinstance(result, dict):
        # Handle dict with mixed objects
        serializable = {}
        for k, v in result.items():
            if hasattr(v, "to_dict"):
                serializable[k] = v.to_dict()
            elif isinstance(v, list) and v and hasattr(v[0], "to_dict"):
                serializable[k] = [item.to_dict() for item in v]
            else:
                serializable[k] = v
        data = json.dumps(serializable, indent=2, ensure_ascii=False, default=str)
    else:
        data = str(result)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(data)
        if not args.quiet:
            print(f"Output saved to {args.output}")
    else:
        print(data)


if __name__ == "__main__":
    main()
