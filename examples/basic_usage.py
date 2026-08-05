"""
Basic usage example for Instagram Account Scraper.

This example shows how to scrape a public Instagram profile
and print the results.
"""

from ig_scraper import InstagramScraper

# Initialize scraper (no login needed for public data)
scraper = InstagramScraper()

# Scrape a profile
profile = scraper.get_profile("nasa")

print("=" * 50)
print(f"Username:     @{profile.username}")
print(f"Full Name:    {profile.full_name}")
print(f"Bio:          {profile.biography}")
print(f"Followers:    {profile.followers:,}")
print(f"Following:    {profile.following:,}")
print(f"Posts:        {profile.posts_count:,}")
print(f"Verified:     {'Yes' if profile.is_verified else 'No'}")
print(f"Business:     {'Yes' if profile.is_business else 'No'}")
if profile.business_category:
    print(f"Category:     {profile.business_category}")
print(f"Profile Pic:  {profile.profile_pic_url}")
print("=" * 50)

# Export to JSON
json_data = profile.to_json()
print("\nJSON output (first 500 chars):")
print(json_data[:500])

# Save to file
with open("nasa_profile.json", "w", encoding="utf-8") as f:
    f.write(json_data)
print("\nSaved to nasa_profile.json")
