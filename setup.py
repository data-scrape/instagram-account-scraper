from setuptools import setup, find_packages

setup(
    name="instagram-account-scraper",
    version="1.0.0",
    description=(
        "A powerful Python tool to scrape Instagram profiles, posts, reels, "
        "stories, hashtags, followers, and emails. Export to JSON, CSV, or Excel."
    ),
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Instagram Scraper Contributors",
    license="MIT",
    python_requires=">=3.9",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "instaloader>=4.14",
    ],
    extras_require={
        "excel": ["openpyxl>=3.1.0"],
        "dev": ["pytest>=7.0", "pytest-cov>=4.0", "openpyxl>=3.1.0"],
        "all": ["instaloader>=4.14", "openpyxl>=3.1.0"],
    },
    entry_points={
        "console_scripts": [
            "ig-scraper=ig_scraper.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords=[
        "instagram", "scraper", "instagram-scraper", "instagram-api",
        "instagram-crawler", "instagram-data-extraction",
        "instagram-profile-scraper", "instagram-post-scraper",
        "instagram-reels", "instagram-stories", "instagram-hashtag",
        "instagram-followers", "social-media-scraper", "web-scraping",
    ],
)
