# Instagram Account Scraper

<div align="center">

[![GitHub stars](https://img.shields.io/github/stars/data-scrape/instagram-account-scraper?style=social)](https://github.com/data-scrape/instagram-account-scraper)
[![GitHub forks](https://img.shields.io/github/forks/data-scrape/instagram-account-scraper?style=social)](https://github.com/data-scrape/instagram-account-scraper/fork)
[![GitHub issues](https://img.shields.io/github/issues/data-scrape/instagram-account-scraper)](https://github.com/data-scrape/instagram-account-scraper/issues)
[![GitHub license](https://img.shields.io/github/license/data-scrape/instagram-account-scraper)](https://github.com/data-scrape/instagram-account-scraper/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)](https://www.python.org/)

</div>


> Instagram account scraper - profiles, posts, reels, stories, emails


<!-- SEO keywords: instagram account scraper, Instagram Account Scraper, instagram account scraper python, instagram account scraper github, best instagram account scraper -->


<div align="center">

## 💎 Sponsored by CoreClaw

[![CoreClaw](https://img.shields.io/badge/CoreClaw-Data_Scraping_Platform-7B2FF7?style=for-the-badge&labelColor=5B21B6)](https://www.coreclaw.com/?utm_source=github&utm_medium=cpc&utm_campaign=L7&utm_term=&utm_id=L7)

**The All-in-One Web Scraping & Data Platform** — Scrape Google Maps, Instagram, Amazon, LinkedIn, TikTok, YouTube, and 50+ platforms via ready-to-use REST APIs.

✅ No browser automation · ✅ No proxy management · ✅ Free credits for new users

⬇️ [Get Started with CoreClaw Free](https://www.coreclaw.com/?utm_source=github&utm_medium=cpc&utm_campaign=L7&utm_term=&utm_id=L7)

</div>

---

> A powerful Python tool to scrape Instagram profiles, posts, reels, stories, hashtags, followers, and emails. Export to JSON, CSV, or Excel. Built for data analysts, marketers, and researchers.

<p align="center">  
  <a href="https://github.com/data-scrape/instagram-account-scraper/releases"><img src="https://img.shields.io/github/v/release/data-scrape/instagram-account-scraper?label=version" alt="Version"></a>  
  <a href="https://github.com/data-scrape/instagram-account-scraper/actions"><img src="https://img.shields.io/github/actions/workflow/status/data-scrape/instagram-account-scraper/ci.yml?branch=main\&label=CI" alt="CI"></a>  
  <a href="https://github.com/data-scrape/instagram-account-scraper/stargazers"><img src="https://img.shields.io/github/stars/data-scrape/instagram-account-scraper?style=social" alt="GitHub stars"></a>  
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue" alt="Python 3.9+">  
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License: MIT">  
  <img src="https://img.shields.io/badge/instaloader-4.14%2B-blue" alt="instaloader 4.14+">  
  <a href="https://pypi.org/project/instagram-account-scraper/"><img src="https://img.shields.io/pypi/dm/instagram-account-scraper" alt="PyPI downloads"></a>  
</p>

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [CLI Usage](#cli-usage)
- [Python API](#python-api)
- [Data Models](#data-models)
- [Export Formats](#export-formats)
- [Use Cases](#use-cases)
- [Configuration](#configuration)
- [Rate Limiting & Best Practices](#rate-limiting--best-practices)
- [Proxy Support](#proxy-support)
- [FAQ](#frequently-asked-questions)
- [Contributing](#contributing)
- [Changelog](#changelog)
- [License](#license)
- [Disclaimer](#disclaimer)

---

## Overview

**Instagram Account Scraper** is a Python library and CLI tool that lets you scrape public Instagram account data programmatically. It retrieves profile information, recent posts, reels, stories, hashtags, follower lists, and even extracts email addresses from bios and captions.

Whether you're doing competitor analysis, lead generation, social media research, or building a marketing pipeline, this tool provides a clean, typed API and a full-featured command line interface.

### Why This Scraper?

| Feature                          | This Tool | Manual Instagram Browsing |  Other Scrapers  |
| -------------------------------- | :-------: | :-----------------------: | :--------------: |
| Batch scrape multiple accounts   |    Yes    |             No            |      Limited     |
| Export to JSON / CSV / Excel     |    Yes    |             No            |      Partial     |
| Extract emails from bios & posts |    Yes    |             No            |       Rare       |
| Scrape reels and stories         |    Yes    |             No            |      Limited     |
| Rate limiting & retry logic      |    Yes    |            N/A            |      Partial     |
| Proxy support                    |    Yes    |            N/A            |       Some       |
| Typed data models                |    Yes    |            N/A            |        No        |
| CLI + Python API                 |    Yes    |            N/A            | One or the other |
| Open source (MIT)                |    Yes    |            N/A            |       Rare       |

---

## Features

### Profile Scraping

- Username, full name, bio, external URL
- Follower count, following count, post count
- Verified badge, business account, business category
- Profile picture URL (standard + HD)
- Private/public status

### Post & Reel Scraping

- Recent posts (photos, carousels, videos)
- Post captions, hashtags, mentions
- Like count, comment count, view count
- Post timestamps and locations
- Media URLs (images and videos)
- Tagged users
- Reel-specific data (play count, duration, music info)

### Story Scraping (Login Required)

- Active stories from any account you follow
- Story media URLs and types
- Story timestamps and durations

### Hashtag Scraping

- Top posts for any hashtag
- Post count for the hashtag
- Recent posts with full metadata

### Follower & Following Lists (Login Required)

- Get follower usernames
- Get following usernames
- Batch processing with progress bars

### Email Extraction

- Scrape emails from profile bios
- Scrape emails from post captions
- Unique email deduplication

### Data Export

- JSON (with proper Unicode support)
- CSV (Excel-compatible)
- Excel (via openpyxl)
- Custom field selection

### Developer Features

- Typed dataclasses for all data models
- Built-in rate limiting with random delays
- Automatic retry with exponential backoff
- Proxy support
- Session persistence for login
- Progress bars for batch operations
- Comprehensive error handling with custom exceptions
- Full type hints (Python 3.9+)

---

## Installation

### Option 1: pip install (Recommended)

```bash
pip install instagram-account-scraper
```

### Option 2: Install from source

```bash
git clone https://github.com/data-scrape/instagram-account-scraper.git
cd instagram-account-scraper
pip install -e .
```

### Option 3: Install with optional dependencies

```bash
# For Excel export
pip install instagram-account-scraper[excel]

# For development
pip install instagram-account-scraper[dev]

# Install everything
pip install instagram-account-scraper[all]
```

### Prerequisites

- **Python 3.9 or higher**
- **instaloader** (installed automatically as a dependency)
- **openpyxl** (optional, for Excel export)

Verify your installation:

```bash
ig-scraper --version
```

---

## Quick Start

### Scrape a Profile (No Login Required)

```bash
# Get profile info as JSON
ig-scraper profile nasa

# Save to file
ig-scraper profile nasa --output nasa_profile.json

# Export as CSV
ig-scraper profile nasa --format csv --output nasa.csv
```

### Scrape Recent Posts

```bash
# Get 10 recent posts
ig-scraper posts nasa --limit 10 --output nasa_posts.json

# Get only reels
ig-scraper posts nasa --reels --limit 5
```

### Batch Scrape Multiple Accounts

Create a text file `accounts.txt`:

```
nasa
natgeo
natgeotravel
discovery
```

```bash
ig-scraper batch accounts.txt --limit 5 --output results.json
```

### Scrape with Login (For Private Data)

```bash
ig-scraper --login youruser yourpass posts private_account --limit 20
```

### Extract Emails from a Business Account

```bash
ig-scraper emails somebusiness --posts 50 --output emails.json
```

---

## CLI Usage

### Full Command Reference

| Command                                       | Description                       | Login Required |
| --------------------------------------------- | --------------------------------- | :------------: |
| `ig-scraper profile <username>`               | Get profile information           |       No       |
| `ig-scraper posts <username> [--limit N]`     | Get recent posts                  |       No       |
| `ig-scraper reels <username> [--limit N]`     | Get recent reels                  |       No       |
| `ig-scraper stories <user1> <user2> ...`      | Get active stories                |       Yes      |
| `ig-scraper hashtag <tag> [--limit N]`        | Get posts by hashtag              |       No       |
| `ig-scraper followers <username> [--limit N]` | Get follower list                 |       Yes      |
| `ig-scraper following <username> [--limit N]` | Get following list                |       Yes      |
| `ig-scraper emails <username> [--posts N]`    | Extract email addresses           |       No       |
| `ig-scraper batch <file> [--limit N]`         | Batch scrape from file            |       No       |
| `ig-scraper all <username> [--posts N]`       | Scrape everything for one account |       No       |

### Global Options

| Option                      | Description              | Default                 |
| --------------------------- | ------------------------ | ----------------------- |
| `--login USERNAME PASSWORD` | Instagram credentials    | None                    |
| `--session FILE`            | Session file path        | `~/.ig_scraper_session` |
| `--proxy URL`               | Proxy server             | None                    |
| `--output FILE`             | Output file path         | stdout                  |
| `--format json\|csv\|excel` | Output format            | json                    |
| `--delay SECONDS`           | Rate limit delay         | 2.0                     |
| `--quiet`                   | Suppress progress output | False                   |
| `--debug`                   | Enable debug logging     | False                   |

### CLI Examples

```bash
# Scrape profile and save as Excel
ig-scraper profile natgeo --format excel --output natgeo.xlsx

# Scrape 50 posts with 5-second delay
ig-scraper posts nasa --limit 50 --delay 5.0 --output nasa_posts.json

# Use proxy for scraping
ig-scraper --proxy http://user:pass@proxy:8080 profile nasa

# Batch scrape with quiet mode
ig-scraper batch accounts.txt --limit 10 --quiet --output results.json

# Scrape hashtag posts
ig-scraper hashtag travel --limit 30 --output travel_hashtag.json

# Get followers (requires login)
ig-scraper --login user pass followers nasa --limit 500
```

---

## Python API

### Basic Profile Scraping

```python
from ig_scraper import InstagramScraper

# Initialize without login (public data only)
scraper = InstagramScraper()

# Scrape a profile
profile = scraper.get_profile("nasa")

print(f"Name: {profile.full_name}")
print(f"Followers: {profile.followers:,}")
print(f"Following: {profile.following:,}")
print(f"Posts: {profile.posts_count:,}")
print(f"Bio: {profile.biography}")
print(f"Verified: {profile.is_verified}")
print(f"Business: {profile.is_business}")
```

### Scraping Posts

```python
from ig_scraper import InstagramScraper

scraper = InstagramScraper()

# Get 10 most recent posts
posts = scraper.get_posts("nasa", limit=10)

for post in posts:
    print(f"Post {post.shortcode}")
    print(f"  Likes: {post.like_count:,}")
    print(f"  Comments: {post.comment_count:,}")
    print(f"  Type: {post.post_type}")
    print(f"  Hashtags: {', '.join(post.hashtags)}")
    print(f"  URL: {post.post_url}")
    print()
```

### Scraping Reels

```python
scraper = InstagramScraper()

# Get 10 most recent reels
reels = scraper.get_reels("nasa", limit=10)

for reel in reels:
    print(f"Reel {reel.shortcode}")
    print(f"  Views: {reel.view_count:,}")
    print(f"  Likes: {reel.like_count:,}")
    print(f"  Duration: {reel.duration:.1f}s")
    if reel.music_title:
        print(f"  Music: {reel.music_title} - {reel.music_artist}")
    print()
```

### Batch Scraping

```python
scraper = InstagramScraper()

usernames = ["nasa", "natgeo", "natgeotravel", "discovery"]
results = scraper.batch_scrape(usernames, posts_limit=5)

for result in results:
    if result.get("profile"):
        p = result["profile"]
        print(f"@{p.username}: {p.followers:,} followers, {p.posts_count:,} posts")
```

### Email Extraction

```python
scraper = InstagramScraper()
emails = scraper.extract_emails("somebusiness", posts_limit=50)

print(f"Found {len(emails)} emails:")
for email in emails:
    print(f"  {email}")
```

### Hashtag Scraping

```python
scraper = InstagramScraper()
hashtag = scraper.get_hashtag_posts("travel", limit=20)

print(f"#{hashtag.hashtag}: {hashtag.post_count:,} total posts")
for post in hashtag.top_posts:
    print(f"  @{post.owner}: {post.like_count:,} likes")
```

### With Login (Private Data, Stories, Followers)

```python
scraper = InstagramScraper(
    username="your_username",
    password="your_password",
)

# Now you can access private profiles you follow
posts = scraper.get_posts("private_account", limit=20)

# Get active stories
stories = scraper.get_stories(["friend1", "friend2"])
for username, user_stories in stories.items():
    print(f"@{username}: {len(user_stories)} active stories")

# Get followers
followers = scraper.get_followers("your_account", limit=500)
print(f"Found {len(followers)} followers")
```

### Export to Multiple Formats

```python
from ig_scraper import InstagramScraper

scraper = InstagramScraper()
profile = scraper.get_profile("nasa")

# JSON
json_data = profile.to_json()
print(json_data)

# Save to JSON file
scraper.export_profile(profile, format="json", output="nasa.json")

# CSV
scraper.export_profile(profile, format="csv", output="nasa.csv")

# Excel (requires openpyxl)
scraper.export_profile(profile, format="excel", output="nasa.xlsx")
```

---

## Data Models

### Profile

| Field                | Type | Description             |
| -------------------- | ---- | ----------------------- |
| `username`           | str  | Instagram username      |
| `user_id`            | str  | Instagram user ID       |
| `full_name`          | str  | Display name            |
| `biography`          | str  | Bio text                |
| `external_url`       | str  | External link in bio    |
| `followers`          | int  | Follower count          |
| `following`          | int  | Following count         |
| `posts_count`        | int  | Total post count        |
| `is_private`         | bool | Private account         |
| `is_verified`        | bool | Verified badge          |
| `is_business`        | bool | Business account        |
| `business_category`  | str  | Business category       |
| `profile_pic_url`    | str  | Profile picture URL     |
| `profile_pic_hd_url` | str  | HD profile picture URL  |
| `cached_at`          | str  | ISO timestamp of scrape |

### Post

| Field           | Type | Description                             |
| --------------- | ---- | --------------------------------------- |
| `shortcode`     | str  | Post shortcode (e.g., `CABC123`)        |
| `owner`         | str  | Owner username                          |
| `caption`       | str  | Post caption text                       |
| `post_url`      | str  | Full post URL                           |
| `post_type`     | str  | GraphImage, GraphVideo, or GraphSidecar |
| `like_count`    | int  | Number of likes                         |
| `comment_count` | int  | Number of comments                      |
| `view_count`    | int  | Video view count                        |
| `timestamp`     | str  | ISO timestamp                           |
| `location`      | str  | Location name                           |
| `media_urls`    | list | List of media URLs                      |
| `tagged_users`  | list | Tagged usernames                        |
| `hashtags`      | list | Hashtags in caption                     |
| `mentions`      | list | @mentions in caption                    |

### Reel

| Field           | Type  | Description         |
| --------------- | ----- | ------------------- |
| `shortcode`     | str   | Reel shortcode      |
| `owner`         | str   | Owner username      |
| `caption`       | str   | Reel caption        |
| `video_url`     | str   | Video URL           |
| `thumbnail_url` | str   | Thumbnail URL       |
| `view_count`    | int   | View count          |
| `like_count`    | int   | Like count          |
| `comment_count` | int   | Comment count       |
| `play_count`    | int   | Play count          |
| `duration`      | float | Duration in seconds |
| `timestamp`     | str   | ISO timestamp       |
| `music_title`   | str   | Music track title   |
| `music_artist`  | str   | Music artist name   |

---

## Export Formats

### JSON Export

```json
{
  "username": "nasa",
  "user_id": "528817151",
  "full_name": "NASA",
  "biography": "There's space for everybody. ✨",
  "followers": 85000000,
  "following": 81,
  "posts_count": 3500,
  "is_private": false,
  "is_verified": true,
  "is_business": true,
  "cached_at": "2026-08-05T14:00:00"
}
```

### CSV Export

Automatically generates Excel-compatible CSV with proper UTF-8 encoding.

### Excel Export

Requires `openpyxl`:

```bash
pip install openpyxl
```

---

## Use Cases

### 1. Competitor Analysis

```python
scraper = InstagramScraper()

competitors = ["brand1", "brand2", "brand3"]
for username in competitors:
    profile = scraper.get_profile(username)
    print(f"@{username}: {profile.followers:,} followers, "
          f"{profile.posts_count:,} posts")
```

### 2. Lead Generation (Email Extraction)

```python
scraper = InstagramScraper()

# Extract emails from business accounts in your niche
accounts = ["business1", "business2", "business3"]
all_emails = []

for account in accounts:
    emails = scraper.extract_emails(account, posts_limit=50)
    all_emails.extend(emails)

print(f"Total unique emails: {len(set(all_emails))}")
```

### 3. Hashtag Research

```python
scraper = InstagramScraper()

hashtags = ["travel", "wanderlust", "travelgram"]
for tag in hashtags:
    data = scraper.get_hashtag_posts(tag, limit=20)
    print(f"#{tag}: {data.post_count:,} posts")
    avg_likes = sum(p.like_count for p in data.top_posts) / len(data.top_posts)
    print(f"  Avg likes: {avg_likes:.0f}")
```

### 4. Content Audit

```python
scraper = InstagramScraper()
posts = scraper.get_posts("your_brand", limit=50)

total_likes = sum(p.like_count for p in posts)
total_comments = sum(p.comment_count for p in posts)

print(f"Total likes: {total_likes:,}")
print(f"Total comments: {total_comments:,}")
print(f"Engagement rate: {(total_likes + total_comments) / 50:.1f} per post")
```

### 5. Follower Analysis (Login Required)

```python
scraper = InstagramScraper(username="user", password="pass")
followers = scraper.get_followers("your_account", limit=1000)

print(f"Retrieved {len(followers)} followers")
# Export for further analysis
import json
with open("followers.json", "w") as f:
    json.dump(followers, f, indent=2)
```

---

## Configuration

### Environment Variables

```bash
# Set default session file location
export IG_SCRAPER_SESSION=/path/to/session

# Set default proxy
export IG_SCRAPER_PROXY=http://user:pass@proxy:8080

# Set default rate limit delay
export IG_SCRAPER_DELAY=3.0
```

### Configuration File

Create `~/.ig_scraper_config.json`:

```json
{
  "rate_limit_delay": 2.5,
  "max_retries": 3,
  "session_file": "~/.ig_scraper_session",
  "proxy": null,
  "user_agent": "Mozilla/5.0 (compatible; IGScraper/1.0)"
}
```

---

## Rate Limiting & Best Practices

Instagram enforces rate limits on API access. This tool includes built-in protections:

### Built-in Protections

- **Random delay between requests** (1-3 seconds by default)
- **Exponential backoff on failures** (retry up to 3 times)
- **Session persistence** to avoid repeated logins
- **Progress bars** for batch operations

### Recommendations

1. **Use session persistence** - Login once, save the session, reuse it
2. **Add delays for large batches** - Use `--delay 5.0` or higher
3. **Use proxies for large-scale scraping** - Rotate IPs to avoid blocks
4. **Respect private accounts** - Don't attempt to bypass privacy settings
5. **Cache results** - Save scraped data to avoid re-scraping

```python
# Good: Cache results and add delays
scraper = InstagramScraper(rate_limit_delay=5.0)

usernames = ["nasa", "natgeo", "natgeotravel"]
for username in usernames:
    profile = scraper.get_profile(username)
    # Save each result immediately
    with open(f"{username}.json", "w") as f:
        f.write(profile.to_json())
```

---

## Proxy Support

Use a proxy to avoid IP-based rate limiting:

### HTTP/HTTPS Proxy

```python
scraper = InstagramScraper(
    proxy="http://user:pass@proxy.example.com:8080"
)
```

### SOCKS5 Proxy

```python
scraper = InstagramScraper(
    proxy="socks5://user:pass@proxy.example.com:1080"
)
```

### Proxy Rotation

For large-scale scraping, use a proxy rotation service:

```python
import random

proxies = [
    "http://proxy1:8080",
    "http://proxy2:8080",
    "http://proxy3:8080",
]

for username in large_username_list:
    proxy = random.choice(proxies)
    scraper = InstagramScraper(proxy=proxy)
    profile = scraper.get_profile(username)
```

---

## Frequently Asked Questions

### Is this tool legal to use?

This tool scrapes publicly available Instagram data. You are responsible for complying with Instagram's Terms of Service, applicable laws, and data protection regulations (GDPR, CCPA) in your jurisdiction. See the [Disclaimer](#disclaimer) section.

### Do I need to log in to Instagram?

No. You can scrape public profiles, posts, reels, hashtags, and emails without logging in. However, stories, follower lists, and following lists require authentication.

### Will this get my Instagram account banned?

There is always a risk when scraping Instagram. To minimize risk:

- Use session persistence instead of repeated logins
- Add delays between requests (`--delay 5.0`)
- Use proxies for large-scale scraping
- Don't scrape thousands of profiles in one session
- Use a dedicated Instagram account (not your personal one)

### What data can I scrape without logging in?

- Profile information (name, bio, follower count, etc.)
- Recent posts (photos, videos, carousels)
- Reels
- Hashtag posts
- Email addresses from bios and captions

### What data requires login?

- Stories (active stories from accounts you follow)
- Follower lists
- Following lists
- Private profiles (that you follow)

### How many profiles can I scrape per day?

This depends on your rate limiting, proxy setup, and Instagram's current rate limits. With proper delays (3-5 seconds between requests) and no proxy, expect ~100-200 profiles per day. With proxy rotation, you can scale higher.

### Can I scrape Instagram Stories?

Yes, but you must be logged in and follow the account whose stories you want to scrape.

### Does this work with Instagram's Graph API?

No. This tool uses [instaloader](https://instaloader.github.io/), which accesses Instagram's web/mobile interface, not the official Graph API. The Graph API requires an approved Facebook App and is limited to business accounts.

### Can I export data to Excel?

Yes. Install `openpyxl` and use `--format excel`:

```bash
pip install openpyxl
ig-scraper profile nasa --format excel --output nasa.xlsx
```

### How do I handle Instagram's 2FA?

If your account has two-factor authentication enabled, the scraper may not be able to log in programmatically. Use a dedicated Instagram account without 2FA, or manually create a session file.

---

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
git clone https://github.com/data-scrape/instagram-account-scraper.git
cd instagram-account-scraper
pip install -e ".[dev]"
pytest
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=ig_scraper

# Run specific test file
pytest tests/test_scraper.py
```

---

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

### v1.0.0 (2026-08-05)

- Initial release
- Profile, post, reel, story, hashtag scraping
- Follower/following list scraping
- Email extraction from bios and captions
- CLI tool with 10 subcommands
- JSON, CSV, Excel export
- Rate limiting, retry logic, proxy support
- Batch scraping with progress bars

---

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

---

## Disclaimer

This tool is for educational and research purposes only. Users are responsible for:

1. **Compliance with Instagram's Terms of Service** - Automated scraping may violate Instagram's ToS.
2. **Data protection laws** - Ensure compliance with GDPR, CCPA, and other applicable data protection regulations.
3. **Ethical use** - Do not use scraped data for harassment, spam, or illegal activities.
4. **Rate limiting** - Respect Instagram's servers and use appropriate delays.

The authors of this tool are not responsible for any consequences of its use, including account suspension, IP bans, or legal action by Instagram or third parties.

**Use at your own risk.**


<!-- CROSS_LINKS_START -->

## Related Scrapers

Explore more data extraction tools:

### Facebook Scrapers

- [facebook-group-scraper](https://github.com/data-scrape/facebook-group-scraper) — Scrape Facebook groups, members, and group posts data

### Google Scrapers

- [apify-google-maps-scraper](https://github.com/data-scrape/apify-google-maps-scraper) — Compare Apify Google Maps Scraper with modern alternatives. Features, pricing, APIs, Google Maps business data, reviews, Place IDs, and production-ready scraping solutions.
- [best-google-maps-scraper](https://github.com/data-scrape/best-google-maps-scraper) — The best Google Maps scraper for extracting business listings, reviews, phone numbers, websites, emails, and local business data via production-ready APIs.
- [best-google-search-scraper](https://github.com/data-scrape/best-google-search-scraper) — The best Google Search scraper for extracting organic results, ads, featured snippets, related searches, knowledge panels, and SERP data through ready-to-use APIs.
- [google-business-scraper](https://github.com/data-scrape/google-business-scraper) — Scrape Google Business Profiles - reviews, hours, contact info
- [google-map-scraper-api-](https://github.com/data-scrape/google-map-scraper-api-) — Production-ready Google Maps Scraper API for extracting business listings, reviews, place IDs, phone numbers, websites, emails, and locations. REST API, JSON, CSV, no proxies required.
- [google-maps-data-scraper](https://github.com/data-scrape/google-maps-data-scraper) — Extract Google Maps business data, reviews, place IDs, emails, phone numbers, websites, ratings, and locations with production-ready APIs. No proxies or browser automation.
- [google-place-id-api](https://github.com/data-scrape/google-place-id-api) — Get Google Place IDs without API key - free alternative
- [google-reviews-scraper](https://github.com/data-scrape/google-reviews-scraper) — Scrape google-reviews-scraper data
- [google-shopping-scraper](https://github.com/data-scrape/google-shopping-scraper) — Scrape Google Shopping results - prices, products, sellers
- [outscraper-google-maps-scraper](https://github.com/data-scrape/outscraper-google-maps-scraper) — Compare Outscraper Google Maps Scraper with modern alternatives. Features, pricing, APIs, reviews, and production-ready Google Maps scraping solutions.
- [scrape-google-maps](https://github.com/data-scrape/scrape-google-maps) — Learn how to scrape Google Maps business listings, reviews, emails, phone numbers, and place IDs with production-ready APIs. No proxies. No browser automation.

### Job Scrapers

- [apify-indeed-scraper](https://github.com/data-scrape/apify-indeed-scraper) — Scrape apify-indeed-scraper data
- [best-indeed-scraper](https://github.com/data-scrape/best-indeed-scraper) — The best Indeed scraper for extracting job listings, companies, salaries, search results, and public recruitment data through ready-to-use APIs.
- [glassdoor-scraper](https://github.com/data-scrape/glassdoor-scraper) — Scrape Glassdoor job listings, salaries, company reviews
- [indeed-job-scraper](https://github.com/data-scrape/indeed-job-scraper) — Free Indeed job scraper - extract job postings, salaries, company info
- [scrape-indeed-job-postings](https://github.com/data-scrape/scrape-indeed-job-postings) — Python tool to scrape Indeed job postings with full details

### LinkedIn Scrapers

- [linkedin-job-scraper](https://github.com/data-scrape/linkedin-job-scraper) — Scrape LinkedIn job postings, salaries, and application data
- [linkedin-sales-navigator-scraper](https://github.com/data-scrape/linkedin-sales-navigator-scraper) — Scrape LinkedIn Sales Navigator leads and accounts data

### Music & Audio Scrapers

- [spotify-scraper](https://github.com/data-scrape/spotify-scraper) — Scrape Spotify songs, playlists, artists, and podcasts data without API

### Other Scrapers

- [amazon-asin-scraper](https://github.com/data-scrape/amazon-asin-scraper) — Amazon ASIN scraper - lookup ASIN data and product information
- [amazon-price-scraper](https://github.com/data-scrape/amazon-price-scraper) — Amazon price scraper - track prices and extract pricing history
- [amazon-product-scraper](https://github.com/data-scrape/amazon-product-scraper) — Amazon product scraper - extract product details, images, and specs
- [amazon-review-scraper](https://github.com/data-scrape/amazon-review-scraper) — Amazon review scraper - extract product reviews and ratings in bulk
- [amazon-scraper-api](https://github.com/data-scrape/amazon-scraper-api) — Amazon scraper API - REST API for Amazon data extraction
- [apify-instagram-scraper](https://github.com/data-scrape/apify-instagram-scraper) — Compare Apify Instagram Scraper with modern alternatives. Compare APIs, features, pricing, Instagram profile scraping, Reels, comments, hashtags, and production-ready data extraction.
- [apify-reddit-scraper](https://github.com/data-scrape/apify-reddit-scraper) — Apify-style Reddit scraper alternative - free & open source
- [apify-tiktok-scraper](https://github.com/data-scrape/apify-tiktok-scraper) — Apify TikTok scraper alternative - free Python TikTok scraper
- [awesome-apify-alternatives](https://github.com/data-scrape/awesome-apify-alternatives) — A curated list of the best Apify alternatives for web scraping, browser automation, AI agents, and business data extraction.
- [awesome-lead-generation](https://github.com/data-scrape/awesome-lead-generation) — A curated list of the best local lead generation tools, Google Maps scrapers, business data APIs, SEO resources, automation tools, and communities.
- [best-amazon-scraper](https://github.com/data-scrape/best-amazon-scraper) — The best Amazon scraper for extracting products, prices, reviews, sellers, search results, categories, and public e-commerce data through ready-to-use APIs.
- [best-apify-alternative](https://github.com/data-scrape/best-apify-alternative) — The best Apify alternative for Google Maps, LinkedIn, YouTube, Instagram, Amazon, AI agents, and business data APIs.
- [best-apollo-scraper-reddit](https://github.com/data-scrape/best-apollo-scraper-reddit) — Reddit community recommended Apollo scraper alternative
- [best-ebay-scraper](https://github.com/data-scrape/best-ebay-scraper) — The best eBay scraper for extracting products, prices, sellers, reviews, sold listings, search results, and marketplace data through ready-to-use APIs.
- [best-facebook-scraper](https://github.com/data-scrape/best-facebook-scraper) — The best Facebook scraper for extracting public pages, posts, comments, groups, profiles, and business data through production-ready APIs.
- [best-instagram-scraper](https://github.com/data-scrape/best-instagram-scraper) — The best Instagram scraper for extracting profiles, posts, reels, comments, hashtags, followers, and public business data through production-ready APIs.
- [best-linkedin-scraper](https://github.com/data-scrape/best-linkedin-scraper) — The best LinkedIn scraper for extracting profiles, companies, contact information, jobs, posts, and business data through production-ready APIs.
- [best-reddit-scraper](https://github.com/data-scrape/best-reddit-scraper) — The best Reddit scraper for extracting posts, comments, subreddits, users, search results, and public community data through ready-to-use APIs.
- [best-tiktok-scraper](https://github.com/data-scrape/best-tiktok-scraper) — The best TikTok scraper for extracting profiles, videos, comments, hashtags, search results, and public creator data through ready-to-use APIs.
- [best-walmart-scraper](https://github.com/data-scrape/best-walmart-scraper) — The best Walmart scraper for extracting products, prices, reviews, sellers, inventory, search results, and marketplace data through ready-to-use APIs.
- [best-youtube-scraper](https://github.com/data-scrape/best-youtube-scraper) — The best YouTube scraper for extracting channels, videos, comments, playlists, search results, and public creator business information through ready-to-use APIs.
- [blog](https://github.com/data-scrape/blog) — CoreClaw blog - web scraping infrastructure insights. Served at data-scrape.github.io/blog/
- [discord-scraper](https://github.com/data-scrape/discord-scraper) — Scrape Discord messages, channels, members without API
- [ebay-price-scraper](https://github.com/data-scrape/ebay-price-scraper) — eBay price scraper - track prices and extract sold item history
- [ebay-web-scraper](https://github.com/data-scrape/ebay-web-scraper) — eBay web scraper - extract product listings, prices, seller data
- [facebook-marketplace-scraper](https://github.com/data-scrape/facebook-marketplace-scraper) — Facebook Marketplace scraper - extract listings, prices, seller data
- [facebook-page-scraper](https://github.com/data-scrape/facebook-page-scraper) — Facebook page scraper - extract page posts, reviews, insights
- [facebook-post-scraper](https://github.com/data-scrape/facebook-post-scraper) — Facebook post scraper - extract post data, reactions, comments
- [facebook-profile-scraper](https://github.com/data-scrape/facebook-profile-scraper) — Facebook profile scraper - extract profiles, friends, photos, posts
- [facebook-scrape-website](https://github.com/data-scrape/facebook-scrape-website) — Facebook scrape website - full Facebook data extraction toolkit
- [instagram-comment-scraper](https://github.com/data-scrape/instagram-comment-scraper) — Instagram comment scraper - extract comments from posts and reels
- [instagram-email-scraper](https://github.com/data-scrape/instagram-email-scraper) — Instagram email scraper - extract emails from Instagram bios and profiles
- [instagram-follower-scraper](https://github.com/data-scrape/instagram-follower-scraper) — Extract Instagram followers, public profiles, engagement metrics, and creator information using a production-ready Instagram Follower Scraper API. No browser automation. No proxy management.
- [instagram-profile-scraper](https://github.com/data-scrape/instagram-profile-scraper) — Extract public Instagram profile data, business accounts, bios, followers, following, posts, engagement metrics, and profile information using a production-ready Instagram Profile Scraper API.
- [instagram-scraper](https://github.com/data-scrape/instagram-scraper) — Extract Instagram profiles, posts, reels, comments, hashtags, followers, and public business data using production-ready APIs. No browser automation. No proxy management.
- [linkedin-email-scraper](https://github.com/data-scrape/linkedin-email-scraper) — LinkedIn email scraper - extract emails from LinkedIn profiles
- [linkedin-post-scraper](https://github.com/data-scrape/linkedin-post-scraper) — LinkedIn post scraper - extract posts, likes, comments, analytics
- [linkedin-profile-data-scraper](https://github.com/data-scrape/linkedin-profile-data-scraper) — LinkedIn profile data scraper - extract profiles, experience, skills, education
- [linkedin-scraper-api](https://github.com/data-scrape/linkedin-scraper-api) — LinkedIn scraper API - REST API for LinkedIn data extraction
- [pinterest-scraper](https://github.com/data-scrape/pinterest-scraper) — Scrape Pinterest pins, boards, images without API
- [scrap-gold-ebay](https://github.com/data-scrape/scrap-gold-ebay) — Scrap gold eBay - extract gold and precious metal listings from eBay
- [scrape-instagram-followers](https://github.com/data-scrape/scrape-instagram-followers) — Learn how to scrape Instagram followers, public profiles, follower counts, bios, business categories, and creator data using ready-to-use APIs.
- [scrape-instagram-photos](https://github.com/data-scrape/scrape-instagram-photos) — Scrape Instagram photos - download photos from any profile in bulk
- [scrape-youtube-comments](https://github.com/data-scrape/scrape-youtube-comments) — Scrape YouTube comments - extract comments from any video
- [scrape-youtube-search-results](https://github.com/data-scrape/scrape-youtube-search-results) — Scrape YouTube search results - extract videos, channels, playlists
- [telegram-scraper](https://github.com/data-scrape/telegram-scraper) — Scrape Telegram channels, messages, groups without API
- [threads-scraper](https://github.com/data-scrape/threads-scraper) — Scrape Meta Threads posts, profiles, replies without API
- [tiktok-comment-scraper](https://github.com/data-scrape/tiktok-comment-scraper) — TikTok comment scraper - extract comments from TikTok videos
- [tiktok-comments-scraper](https://github.com/data-scrape/tiktok-comments-scraper) — TikTok comments scraper - bulk extract comments and replies
- [tiktok-data-scraper-api](https://github.com/data-scrape/tiktok-data-scraper-api) — TikTok data scraper API - REST API for TikTok data extraction
- [tiktok-profile-scraper](https://github.com/data-scrape/tiktok-profile-scraper) — TikTok profile scraper - extract profiles, followers, video stats
- [tiktok-video-scraper](https://github.com/data-scrape/tiktok-video-scraper) — TikTok video scraper - extract video data, hashtags, trending content
- [twitch-scraper](https://github.com/data-scrape/twitch-scraper) — Scrape Twitch channels, streams, chat without API
- [x-scraper](https://github.com/data-scrape/x-scraper) — Scrape X/Twitter posts, profiles, followers without API
- [youtube-video-scraper-api](https://github.com/data-scrape/youtube-video-scraper-api) — YouTube video scraper API - REST API for video data extraction

### Proxy & API Alternatives

- [bright-data-alternative](https://github.com/data-scrape/bright-data-alternative) — Free open-source Bright Data alternative - web scraping proxy
- [oxylabs-alternative](https://github.com/data-scrape/oxylabs-alternative) — Free open-source Oxylabs alternative - residential proxy scraper
- [scraperapi-alternative](https://github.com/data-scrape/scraperapi-alternative) — Free open-source ScraperAPI alternative - rotating proxy scraper
- [scrapingbee-alternative](https://github.com/data-scrape/scrapingbee-alternative) — Free open-source ScrapingBee alternative - headless browser scraper
- [serpapi-alternative](https://github.com/data-scrape/serpapi-alternative) — Free open-source SerpAPI alternative - SERP scraping without API key
- [zenrows-alternative](https://github.com/data-scrape/zenrows-alternative) — Free open-source ZenRows alternative - anti-bot bypass scraper

### Real Estate Scrapers

- [apify-zillow-scraper](https://github.com/data-scrape/apify-zillow-scraper) — Apify-style Zillow scraper alternative - free & open source
- [best-zillow-scraper](https://github.com/data-scrape/best-zillow-scraper) — The best Zillow scraper for extracting property listings, prices, rental listings, agents, estimates, and real estate data through ready-to-use APIs.
- [easy-scrape-zillow-agents-free](https://github.com/data-scrape/easy-scrape-zillow-agents-free) — Free tool to scrape Zillow real estate agents listings
- [zillow-data-scraper](https://github.com/data-scrape/zillow-data-scraper) — Scrape Zillow property data - prices, addresses, Zestimate
- [zillow-scraper-api](https://github.com/data-scrape/zillow-scraper-api) — Zillow scraper API - structured JSON output for property data

### Reviews & Local Scrapers

- [scrape-yelp-reviews](https://github.com/data-scrape/scrape-yelp-reviews) — Free Yelp reviews scraper - extract ratings, text, dates
- [yellow-pages-scraper](https://github.com/data-scrape/yellow-pages-scraper) — Scrape yellow-pages-scraper data

### Social Media Scrapers

- [quora-scraper](https://github.com/data-scrape/quora-scraper) — Scrape Quora questions, answers, and user profiles data
- [slack-scraper](https://github.com/data-scrape/slack-scraper) — Scrape Slack channels, messages, and workspace data
- [snapchat-scraper](https://github.com/data-scrape/snapchat-scraper) — Scrape Snapchat stories, profiles, and public content data
- [whatsapp-scraper](https://github.com/data-scrape/whatsapp-scraper) — Scrape WhatsApp groups, contacts, and message data programmatically

### YouTube Scrapers

- [youtube-channel-scraper](https://github.com/data-scrape/youtube-channel-scraper) — Scrape YouTube channel data, stats, and video lists in bulk

<!-- CROSS_LINKS_END -->

<!-- STAR_SECTION_START -->
## ⭐ Support This Project

If this tool helped you, please consider:

1. **⭐ Star this repository** — [Click here to star](https://github.com/data-scrape/instagram-account-scraper)
2. **📧 Share with your network** — Help others discover this tool
3. **🐛 Report issues** — [Open an issue](https://github.com/data-scrape/instagram-account-scraper/issues) if you find a bug
4. **📚 Contribute** — PRs are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md)

<div align="center">

### 👉 Ready to scrape more platforms?

[![Star History](https://img.shields.io/github/stars/data-scrape/instagram-account-scraper?style=social)](https://github.com/data-scrape/instagram-account-scraper)

**Check out all our scrapers:**

[Instagram](https://github.com/data-scrape/instagram-scraper) ·
[Google Maps](https://github.com/data-scrape/best-google-maps-scraper) ·
[Amazon](https://github.com/data-scrape/best-amazon-scraper) ·
[TikTok](https://github.com/data-scrape/best-tiktok-scraper) ·
[YouTube](https://github.com/data-scrape/best-youtube-scraper) ·
[LinkedIn](https://github.com/data-scrape/best-linkedin-scraper) ·
[eBay](https://github.com/data-scrape/best-ebay-scraper) ·
[Reddit](https://github.com/data-scrape/best-reddit-scraper) ·
[Apify Alternative](https://github.com/data-scrape/best-apify-alternative)

</div>

<!-- STAR_SECTION_END -->

