# Instagram Account Scraper - Installation Guide

## System Requirements

- Python 3.9 or higher
- pip (Python package manager)
- Internet connection

## Installation Methods

### Method 1: pip (Recommended)

```bash
pip install instagram-account-scraper
```

### Method 2: From Source

```bash
git clone https://github.com/xiaozhucchongya-byte/instagram-account-scraper.git
cd instagram-account-scraper
pip install -e .
```

### Method 3: With Optional Dependencies

```bash
# Excel export support
pip install instagram-account-scraper[excel]

# Development tools
pip install instagram-account-scraper[dev]

# Everything
pip install instagram-account-scraper[all]
```

## Verification

```bash
ig-scraper --version
```

## Platform-Specific Notes

### Windows

```bash
# Using pip
pip install instagram-account-scraper

# If you get permission errors, use --user
pip install --user instagram-account-scraper
```

### macOS

```bash
# Using Homebrew Python
brew install python
pip install instagram-account-scraper

# Using pyenv
pyenv install 3.11
pyenv global 3.11
pip install instagram-account-scraper
```

### Linux

```bash
# Ubuntu/Debian
sudo apt install python3 python3-pip
pip install instagram-account-scraper

# Arch Linux
sudo pacman -S python python-pip
pip install instagram-account-scraper
```

### Docker

```bash
docker run --rm -v $(pwd):/data python:3.11-slim bash -c "
  pip install instagram-account-scraper &&
  ig-scraper profile nasa --output /data/nasa.json
"
```

## Troubleshooting

### "instaloader not found"

```bash
pip install instaloader>=4.14
```

### "openpyxl not found" (Excel export)

```bash
pip install openpyxl
```

### Login fails with 2FA

Instagram accounts with two-factor authentication may not work with programmatic login. Use a dedicated account without 2FA.

### Session expired

Delete the session file and re-login:

```bash
rm ~/.ig_scraper_session
ig-scraper --login user pass profile someuser
```
