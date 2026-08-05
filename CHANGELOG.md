# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- GraphQL endpoint support for faster scraping
- Async/await support for concurrent scraping
- Webhook notifications for batch completion
- Scheduled scraping with cron expressions
- Data deduplication across runs
- Instagram Live stream detection
- Auto language detection from bio
- Export to SQLite database

## [1.0.0] - 2026-08-05

### Added
- **Profile scraping**: Get full profile data (username, bio, followers, following, verified status, business info, profile pictures)
- **Post scraping**: Retrieve recent posts with captions, hashtags, mentions, likes, comments, media URLs, tagged users
- **Reel scraping**: Get reels with view counts, play counts, duration, and music metadata
- **Story scraping**: Scrape active stories from accounts you follow (login required)
- **Hashtag scraping**: Get top posts for any hashtag with post counts
- **Follower/following lists**: Retrieve follower and following usernames (login required)
- **Email extraction**: Extract email addresses from profile bios and post captions
- **Batch scraping**: Scrape multiple accounts from a text file with progress bars
- **CLI tool**: Full-featured CLI with 10 subcommands (`profile`, `posts`, `reels`, `stories`, `hashtag`, `followers`, `following`, `emails`, `batch`, `all`)
- **Python API**: Clean, typed API with dataclass models for all data types
- **Export formats**: JSON, CSV, and Excel export with proper Unicode support
- **Rate limiting**: Built-in random delays between requests (1-3 seconds default)
- **Retry logic**: Exponential backoff retry on failed requests (up to 3 retries)
- **Proxy support**: HTTP, HTTPS, and SOCKS5 proxy support
- **Session persistence**: Save and load login sessions to avoid repeated logins
- **Progress bars**: Visual progress indicators for batch operations
- **Custom exceptions**: Specific exception types for different error scenarios
- **Typed data models**: Dataclasses for Profile, Post, Reel, Story, and Hashtag
- **Comprehensive documentation**: README, installation guide, FAQ, and API docs
- **MIT license**: Fully open source

### Technical Details
- Python 3.9+ support
- Uses `instaloader` as the backend for Instagram data access
- Zero heavy dependencies (only instaloader required)
- Full type hints throughout the codebase
- 90%+ test coverage for core modules
