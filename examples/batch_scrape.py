"""
Batch scraping example for Instagram Account Scraper.

This example demonstrates how to scrape multiple Instagram accounts
and export the combined results.
"""

import json
from ig_scraper import InstagramScraper

# List of accounts to scrape
accounts = [
    "nasa",
    "natgeo",
    "natgeotravel",
    "discovery",
    "bbc",
]

# Initialize scraper with a longer delay for batch operations
scraper = InstagramScraper(rate_limit_delay=3.0)

# Scrape all accounts
results = scraper.batch_scrape(accounts, posts_limit=5)

# Print summary
print("\n" + "=" * 60)
print("BATCH SCRAPING RESULTS")
print("=" * 60)

for result in results:
    username = result["username"]
    if result.get("error"):
        print(f"  @{username}: ERROR - {result['error']}")
        continue

    profile = result.get("profile")
    if profile:
        print(
            f"  @{username}: {profile.followers:,} followers, "
            f"{profile.posts_count:,} posts, "
            f"{len(result.get('posts', []))} posts scraped, "
            f"{len(result.get('emails', []))} emails found"
        )
    else:
        print(f"  @{username}: profile not available")

print("=" * 60)

# Export all results to a single JSON file
export_data = []
for result in results:
    if result.get("profile"):
        export_data.append({
            "username": result["username"],
            "profile": result["profile"].to_dict(),
            "posts": [p.to_dict() for p in result.get("posts", [])],
            "reels": [r.to_dict() for r in result.get("reels", [])],
            "emails": result.get("emails", []),
        })

with open("batch_results.json", "w", encoding="utf-8") as f:
    json.dump(export_data, f, indent=2, ensure_ascii=False)

print(f"\nResults saved to batch_results.json ({len(export_data)} accounts)")
