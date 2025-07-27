from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime

def scrape_amazon_multipage(search_term="laptop", pages_to_scrape=10, background=True):
    """
    Scrape Amazon search results for multiple pages
    
    Parameters:
    - search_term: What to search for on Amazon (default: "laptop")
    - pages_to_scrape: Number of pages to scrape (default: 10) or "all" for all pages
    - background: Run browser in headless mode if True (default: True)
    """
    # Set up logging
    log_filename = f"amazon_scraper_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    def log_message(message):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(log_filename, "a", encoding="utf-8") as log_file:
            log_file.write(f"[{timestamp}] {message}\n")
    
    # Set up Chrome options
    chrome_options = Options()
    if background:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.amazon.com")
    
    max_retries = 3
    retry_count = 0
    search_bar = None
    
    try:
        # Try to find search bar with retries
        while retry_count < max_retries:
            try:
                search_bar = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
                )
                break  # Found search bar, exit retry loop
            except:
                retry_count += 1
                if retry_count < max_retries:
                    log_message(f"⚠️ Search bar not found, reloading page (attempt {retry_count}/{max_retries})")
                    driver.refresh()
                else:
                    raise Exception("Search bar not found after multiple attempts")
        
        # Search for the specified term
        log_message(f"🔍 Searching for: {search_term}")
        search_bar.send_keys(search_term + Keys.RETURN)
        
        # Wait for results to load
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-component-type='s-search-result']"))
        )
        
        # Function to get total number of pages
        def get_total_pages():
            try:
                pagination = driver.find_elements(By.CSS_SELECTOR, ".s-pagination-item")
                if pagination:
                    last_page = int(pagination[-2].text)  # Second last element is usually the last page number
                    return last_page
                return 1  # If no pagination found, assume only 1 page
            except:
                return 1
        
        # Get total pages available
        total_pages = get_total_pages()
        log_message(f"ℹ️ Found {total_pages} pages of results")
        
        # Adjust pages_to_scrape if "all" was specified or if requested pages exceed available pages
        if pages_to_scrape == "all":
            pages_to_scrape = total_pages
        else:
            pages_to_scrape = min(pages_to_scrape, total_pages)
        
        # Create filename based on search term
        filename = f"amazon_{search_term.replace(' ', '_')}_products.html"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"<html><body><h1>Amazon results for: {search_term}</h1>\n")
            f.write(f"<p>Scraped {pages_to_scrape} out of {total_pages} available pages</p>\n")
            
            page = 1
            keep_scraping = True
            
            while keep_scraping and page <= pages_to_scrape:
                log_message(f"🔄 Processing page {page} of {pages_to_scrape}...")
                
                # Wait for results and scrape
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-component-type='s-search-result']"))
                )
                products = driver.find_elements(By.CSS_SELECTOR, "[role='listitem'], [data-component-type='s-search-result']")
                
                # Save HTML
                for product in products:
                    f.write(product.get_attribute("outerHTML") + "\n\n")
                
                # Check if we should continue scraping
                if page < pages_to_scrape:
                    try:
                        next_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, ".s-pagination-next"))
                        )
                        if "s-pagination-disabled" in next_button.get_attribute("class"):
                            keep_scraping = False
                            log_message("ℹ️ Reached the last page of results")
                        else:
                            next_button.click()
                            # Wait for page to load
                            time.sleep(2)  # Adding small delay to prevent rapid clicking
                            page += 1
                    except:
                        keep_scraping = False
                        log_message("ℹ️ Could not find or click next page button")
                else:
                    keep_scraping = False
            
            f.write("</body></html>")
            log_message(f"✅ Saved products from {page} pages to {filename}")
            
    except Exception as e:
        log_message(f"❌ Error: {str(e)}")
    finally:
        driver.quit()
        log_message("🛑 Scraping session ended")

# Example usages:
# scrape_amazon_multipage()  # Default: search "laptop", 10 pages, background
# scrape_amazon_multipage("wireless headphones", 5)  # Search headphones, 5 pages
# scrape_amazon_multipage("python programming book", "all", False)  # Search books, all pages, visible browser
