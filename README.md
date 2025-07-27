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

## Requirements
- Python 3.8+
- Chrome (for Selenium)

## Quick Start

1. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```

2. ChromeDriver Setup  
   1. Download the correct version for your Chrome browser from [here](https://chromedriver.chromium.org/downloads).  
   2. Either:  
      - Place `chromedriver` in your project folder, **or**  
      - Add it to your system `PATH`.  
   3. Verify compatibility:  
      ```bash
      chromedriver --version
      ```

3. Run the scraper:
    ```python
   from amazon_scraper import scrape_amazon_multipage
   # Scrape 3 pages of wireless earbuds (headless mode + auto CSV)
   scrape_amazon_multipage("wireless earbuds", pages_to_scrape=3)
    ```

## Usages

```markdown
| Variable        | Type | Description                                                                     |
|-----------------|------|---------------------------------------------------------------------------------|
| pages_to_scrape | int  | The number of pages to scrape. Set to "all" for no limit.                       |
| background      | bool | If True, runs the browser in headless (background) mode. Default: True.         |
| convert_to_csv  | bool | If True, automatically converts scraped HTML data to a CSV file. Default: True. |
```

## Output Files

```markdown
| File_Type | Format | Example_Name                          | Generated When?               |
|-----------|--------|---------------------------------------|-------------------------------|
| Products  | HTML   | amazon_wireless_earbuds_products.html | Always                        |
| CSV       | CSV    | amazon_wireless_earbuds_products.csv  | convert_to_csv=True (default) |
| Log       | Text   | amazon_scraper_20250728_0145.log      | Always                        |
```

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
