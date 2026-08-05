"""
Export data example for Instagram Account Scraper.

Shows how to export scraped data to JSON, CSV, and Excel formats.
"""

from ig_scraper import InstagramScraper

scraper = InstagramScraper()
profile = scraper.get_profile("nasa")

# === JSON Export ===
print("=== JSON Export ===")
json_data = profile.to_json(indent=2)
print(json_data[:300] + "...")

# Save to file
with open("nasa.json", "w", encoding="utf-8") as f:
    f.write(json_data)
print("Saved to nasa.json\n")

# === CSV Export ===
print("=== CSV Export ===")
from ig_scraper.models import DataExporter

csv_data = DataExporter.to_csv([profile])
print(csv_data[:300] + "...")

# Save to file
DataExporter.to_csv([profile], output="nasa.csv")
print("Saved to nasa.csv\n")

# === Excel Export ===
print("=== Excel Export ===")
try:
    DataExporter.to_excel(profile, output="nasa.xlsx")
    print("Saved to nasa.xlsx")
except ImportError:
    print("Excel export requires openpyxl: pip install openpyxl")

# === Export Multiple Profiles ===
print("\n=== Batch CSV Export ===")
profiles = []

for username in ["nasa", "natgeo", "discovery"]:
    try:
        p = scraper.get_profile(username)
        profiles.append(p)
        print(f"  Scraped @{username}: {p.followers:,} followers")
    except Exception as e:
        print(f"  Failed @{username}: {e}")

# Export all to CSV
DataExporter.to_csv(profiles, output="all_profiles.csv")
print(f"\n{len(profiles)} profiles saved to all_profiles.csv")
