# COVID-19 Data Scraping Script - Installation & Setup Guide

## Overview
This Python script scrapes COVID-19 pandemic data from Wikipedia and performs data cleaning and analysis.

## Requirements Summary

### Direct Dependencies (Must Have)
1. **pandas** (v3.0.0+) - Data manipulation and analysis
2. **requests** (v2.32.0+) - HTTP library for fetching web pages
3. **beautifulsoup4** (v4.14.0+) - HTML/XML parsing library
4. **lxml** (v6.0.0+) - XML and HTML processing backend

### Optional but Recommended
- **html5lib** (v1.1+) - Better HTML5 parsing support

## Installation Instructions

### Step 1: Install Python (if not already installed)
- Python 3.8 or higher recommended
- Download from: https://www.python.org/downloads/

### Step 2: Install pip (if not already installed)
- pip is typically included with Python
- Verify installation: `pip --version`

### Step 3: Install All Requirements

#### Option A: Using requirements.txt (Recommended)
```bash
pip install -r requirements.txt
```

#### Option B: Install individually
```bash
pip install pandas>=3.0.0
pip install requests>=2.32.0
pip install beautifulsoup4>=4.14.0
pip install lxml>=6.0.0
pip install html5lib>=1.1
```

## Package Details

| Package | Version | Purpose |
|---------|---------|---------|
| pandas | 3.0.0+ | Data manipulation, DataFrame operations, data cleaning |
| requests | 2.32.0+ | Makes HTTP requests to fetch Wikipedia pages |
| beautifulsoup4 | 4.14.0+ | Parses HTML content and extracts tables |
| lxml | 6.0.0+ | Backend parser for BeautifulSoup, faster parsing |
| html5lib | 1.1+ | Alternative HTML5 parser for better compatibility |

## Verification

After installation, verify all packages are installed correctly:

```bash
pip list | grep -E "pandas|requests|beautifulsoup|lxml|html5lib"
```

Expected output:
```
beautifulsoup4      4.14.3
html5lib            1.1
lxml                6.0.2
pandas              3.0.1
requests            2.32.5
```

## How the Script Uses Each Package

1. **requests** - Fetches the Wikipedia page containing COVID-19 data
2. **BeautifulSoup (beautifulsoup4)** - Parses HTML and locates the data table
3. **lxml** - Provides efficient HTML parsing backend
4. **pandas** - Reads HTML table into DataFrame, cleans data, and performs analysis

## Running the Script

```bash
python covid_scraper.py
```

## Troubleshooting

### ImportError: No module named 'requests'
**Solution:** Run `pip install requests`

### ImportError: No module named 'bs4'
**Solution:** Run `pip install beautifulsoup4` (note: import is `bs4`, not `beautifulsoup4`)

### Connection errors when fetching Wikipedia
**Solution:** 
- Check your internet connection
- Wikipedia may be blocking automated requests - consider adding a User-Agent header

### Table parsing issues
**Solution:** 
- Install html5lib: `pip install html5lib`
- This provides better HTML5 parsing support

## Additional Notes

- The script requires internet access to fetch Wikipedia data
- Some systems may need additional dependencies (lxml may require system libraries)
- On Linux: `sudo apt-get install libxml2-dev libxslt1-dev` (if lxml installation fails)
- On macOS: Xcode Command Line Tools required for C extensions

## Version Compatibility

- **Minimum Python Version:** 3.8
- **Recommended Python Version:** 3.10 or higher
- All packages are compatible with Python 3.8+

## Updating Packages

To update all packages to their latest versions:

```bash
pip install --upgrade -r requirements.txt
```

Or individually:
```bash
pip install --upgrade pandas requests beautifulsoup4 lxml html5lib
```
