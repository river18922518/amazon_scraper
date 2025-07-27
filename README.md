# Amazon Product Scraper

A robust Python scraper that extracts product listings from Amazon search results across multiple pages.

## Features

- 🔍 Custom product searches
- 📑 Multi-page scraping (with "all pages" option)
- 🖥️ Headless browser mode (default) or visible mode
- ⏱️ Automatic pagination handling
- 📁 HTML output with preserved product structure
- 📝 Detailed logging with timestamps
- 🔄 Smart retry mechanism for reliability

## Quick Start

1. Install requirements:
    pip install selenium

2. Download ChromeDriver:
    https://googlechromelabs.github.io/chrome-for-testing

3. Run the scraper:
    please refer to the usage guide at the bottom of the "amazon_scraper.py".

## Output Files

File_Type Format Example_Name
Products  HTML   amazon_wireless_earbuds_products.html
Log       Text   amazon_scraper_20250728_0145.log

## Troubleshooting

Common Issues:
    ChromeDriver version mismatch - ensure it matches your Chrome version

## Disclaimer

This script is for educational purposes only. Please respect Amazon's Terms of Service and robots.txt. Use responsibly with reasonable request rates.

## License

MIT © 2025 river18922518
