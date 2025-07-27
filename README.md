# Amazon Product Scraper

A robust Python scraper that extracts product listings from Amazon search results across multiple pages.

## ⚠️ Disclaimer  
This is an **educational project** demonstrating web scraping techniques.  
- **Do not use** to scrape Amazon at scale.  
- **Respect** [Amazon’s robots.txt](https://www.amazon.com/robots.txt) and [Terms of Service](https://www.amazon.com/gp/help/customer/display.html?nodeId=508088)

## Features

- 🔍 Custom product searches
- 📑 Multi-page scraping (with "all pages" option)
- 🖥️ Headless browser mode (default) or visible mode
- ⏱️ Automatic pagination handling
- 📁 HTML output with preserved product structure
- 📝 Detailed logging with timestamps
- 🔄 Smart retry mechanism for reliability

## Quick Start

1. Install dependencies:  
   ```bash
   pip install -r requirements.txt

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

## 🎯 What This Project Demonstrates

- Web scraping with Selenium
- Headless browser automation
- Robust error handling

## 💡 Why I Build This

Amazon’s search results are heavily dynamic, making them a good case study for learning:  
- **Technical Challenge**: Extracting data from a site that actively blocks scrapers.  
- **My Approach**: Used Selenium with headless browsing and staggered requests to reduce detection risk.  

**Outcome**: A working scraper that logs errors and preserves data structure.  

*Note: This is a demo project—scraping at scale may violate Amazon’s ToS.*  

## License

MIT © 2025 river18922518
