"""
Email extraction example for Instagram Account Scraper.

Demonstrates how to extract email addresses from Instagram profiles
(bios and post captions) for lead generation.
"""

from ig_scraper import InstagramScraper

scraper = InstagramScraper()

# Extract emails from a single account
print("=== Email Extraction ===")
emails = scraper.extract_emails("some_business_account", posts_limit=50)

print(f"Found {len(emails)} unique emails:")
for email in emails:
    print(f"  - {email}")

# Batch email extraction
print("\n=== Batch Email Extraction ===")
business_accounts = [
    "business1",
    "business2",
    "business3",
]

all_emails = set()

for username in business_accounts:
    try:
        emails = scraper.extract_emails(username, posts_limit=30)
        all_emails.update(emails)
        print(f"  @{username}: {len(emails)} emails found")
    except Exception as e:
        print(f"  @{username}: failed - {e}")

print(f"\nTotal unique emails: {len(all_emails)}")
for email in sorted(all_emails):
    print(f"  - {email}")
