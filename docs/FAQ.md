# Instagram Account Scraper - FAQ

## General Questions

### What is Instagram Account Scraper?

Instagram Account Scraper is a Python tool that scrapes public Instagram account data including profiles, posts, reels, stories, hashtags, followers, and email addresses. It provides both a Python library and a CLI tool.

### Is it free?

Yes. The tool is open source and released under the MIT license.

### Do I need an Instagram account to use it?

No. You can scrape public profiles, posts, reels, and hashtags without logging in. Login is only required for stories, follower lists, and private profiles you follow.

### What data can I scrape?

| Data Type | Without Login | With Login |
|-----------|:---:|:---:|
| Profile info | Yes | Yes |
| Recent posts | Yes | Yes |
| Reels | Yes | Yes |
| Hashtag posts | Yes | Yes |
| Email extraction | Yes | Yes |
| Stories | No | Yes |
| Follower list | No | Yes |
| Following list | No | Yes |
| Private profiles | No | Yes (if following) |

### How is this different from other Instagram scrapers?

- **Typed data models** - All data returned as typed Python dataclasses
- **Multiple export formats** - JSON, CSV, Excel out of the box
- **Email extraction** - Built-in email extraction from bios and captions
- **Rate limiting** - Built-in delays and retry logic to prevent bans
- **Proxy support** - First-class proxy and proxy rotation support
- **Batch operations** - Scrape multiple accounts with progress bars
- **CLI + API** - Use from the command line or import as a Python library

## Technical Questions

### What Python versions are supported?

Python 3.9 and above. The tool uses modern Python features like type hints and dataclasses.

### What dependencies does it use?

- **instaloader** - Instagram data access backend
- **openpyxl** (optional) - Excel export
- No other heavy dependencies

### How does rate limiting work?

The scraper adds random delays (1-3 seconds by default) between requests. It also retries failed requests with exponential backoff (up to 3 retries).

### Can I use multiple proxies?

Yes. You can create separate scraper instances with different proxies:

```python
proxies = ["http://proxy1:8080", "http://proxy2:8080"]

for username in usernames:
    proxy = proxies[usernames.index(username) % len(proxies)]
    scraper = InstagramScraper(proxy=proxy)
    profile = scraper.get_profile(username)
```

### How do I save my login session?

Sessions are automatically saved to `~/.ig_scraper_session`. On subsequent runs, the scraper loads the saved session instead of requiring login.

### Can I scrape Instagram Stories?

Yes. Stories require login. Use:

```python
scraper = InstagramScraper(username="user", password="pass")
stories = scraper.get_stories(["friend1", "friend2"])
```

### How accurate is the email extraction?

The tool uses regex pattern matching to find email addresses in bios and post captions. It may find false positives or miss some emails. Always verify extracted emails before use.

## Legal & Ethical Questions

### Is scraping Instagram legal?

Web scraping publicly available data is generally legal in most jurisdictions, but Instagram's Terms of Service prohibit automated access. You are responsible for complying with:

- Instagram's Terms of Service
- GDPR (if processing data of EU residents)
- CCPA (if processing data of California residents)
- Local data protection laws

### Will my Instagram account get banned?

There is always a risk. To minimize it:

1. Use a dedicated Instagram account (not your personal one)
2. Use session persistence
3. Add delays between requests (3-5 seconds)
4. Use proxies for large-scale scraping
5. Don't scrape more than a few hundred profiles per day

### Can I scrape private profiles?

Only if you are logged in and follow the private account. The tool does not bypass Instagram's privacy settings.

### Is the scraped data GDPR compliant?

You are responsible for ensuring GDPR compliance. This includes:

1. Having a legal basis for processing personal data
2. Providing privacy notices to data subjects
3. Honoring data subject rights (access, deletion, etc.)
4. Implementing appropriate security measures

The tool itself does not provide GDPR compliance features.
