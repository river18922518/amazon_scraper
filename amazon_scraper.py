from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
from bs4 import BeautifulSoup
import csv
import os

def scrape_amazon_multipage(search_term="laptop", pages_to_scrape=10, background=True, convert_to_csv=True):
    """
    Scrape Amazon search results for multiple pages
    
    Parameters:
    - search_term: What to search for on Amazon (default: "laptop")
    - pages_to_scrape: Number of pages to scrape (default: 10) or "all" for all pages
    - background: Run browser in headless mode if True (default: True)
    - convert_to_csv: Automatically convert HTML to CSV when True (default: True)
    """
    # Create output directory if it doesn't exist
    output_dir = "amazon_scraper_output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Set up logging with path in output directory
    log_filename = os.path.join(output_dir, f"amazon_scraper_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    
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
        log_message(f"🔍🔍 Searching for: {search_term}")
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
        log_message(f"ℹℹ️ Found {total_pages} pages of results")
        
        # Adjust pages_to_scrape if "all" was specified or if requested pages exceed available pages
        if pages_to_scrape == "all":
            pages_to_scrape = total_pages
        else:
            pages_to_scrape = min(pages_to_scrape, total_pages)
        
        # Create filename based on search term with path in output directory
        filename = os.path.join(output_dir, f"amazon_{search_term.replace(' ', '_')}_products.html")
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"<html><body><h1>Amazon results for: {search_term}</h1>\n")
            f.write(f"<p>Scraped {pages_to_scrape} out of {total_pages} available pages</p>\n")
            
            page = 1
            keep_scraping = True
            
            while keep_scraping and page <= pages_to_scrape:
                log_message(f"🔄🔄 Processing page {page} of {pages_to_scrape}...")
                
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
                            log_message("ℹℹ️ Reached the last page of results")
                        else:
                            next_button.click()
                            # Wait for page to load
                            time.sleep(2)  # Adding small delay to prevent rapid clicking
                            page += 1
                    except:
                        keep_scraping = False
                        log_message("ℹℹ️ Could not find or click next page button")
                else:
                    keep_scraping = False
            
            f.write("</body></html>")
            log_message(f"✅ Saved products from {page} pages to {filename}")
            
            # Automatically convert to CSV if requested
            if convert_to_csv:
                log_message("⚙️ Starting automatic HTML to CSV conversion")
                html_to_csv(filename)
                log_message("✅ CSV conversion completed")
            
    except Exception as e:
        log_message(f"❌❌ Error: {str(e)}")
    finally:
        driver.quit()
        log_message("🛑🛑🛑 Scraping session ended")

def html_to_csv(html_file=None, csv_file=None):
    """
    Convert scraped Amazon HTML file to CSV with product details
    
    Parameters:
    - html_file: Path to the HTML file (optional, will use latest in output dir if None)
    - csv_file: Optional output CSV filename (default: same as HTML file but with .csv extension)
    """
    output_dir = "amazon_scraper_output"
    
    # If no HTML file specified, find the most recent one in output directory
    if html_file is None:
        try:
            # Get all HTML files in output directory
            html_files = [f for f in os.listdir(output_dir) if f.endswith('.html')]
            if not html_files:
                raise FileNotFoundError("No HTML files found in output directory")
            
            # Sort by modification time (newest first)
            html_files.sort(key=lambda x: os.path.getmtime(os.path.join(output_dir, x)), reverse=True)
            html_file = os.path.join(output_dir, html_files[0])
            print(f"Using most recent HTML file: {html_file}")
        except Exception as e:
            print(f"Error finding HTML file: {e}")
            return
    
    if not os.path.exists(html_file):
        raise FileNotFoundError(f"HTML file not found: {html_file}")
    
    # Determine output directory (same as HTML file's directory)
    file_dir = os.path.dirname(html_file)
    
    if csv_file is None:
        base_name = os.path.splitext(os.path.basename(html_file))[0]
        csv_file = os.path.join(file_dir, f"{base_name}.csv")
    
    # Read the HTML file
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    products = soup.find_all(lambda tag: tag.has_attr('data-component-type') and tag['data-component-type'] == 's-search-result')
    
    if not products:
        print("No products found in the HTML file")
        return
    
    # Prepare CSV file
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'product_name',
            'price',
            'original_price',
            'rating',
            'review_count',
            'is_sponsored',
            'product_url',
            'asin'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for product in products:
            try:
                # Extract product name - updated to handle current Amazon HTML structure
                name_tag = product.find('h2', {'class': 'a-size-medium'})
                if name_tag:
                    # First try to get the aria-label which contains the full product name
                    if name_tag.has_attr('aria-label'):
                        product_name = name_tag['aria-label']
                    else:
                        # Fallback to the span content if aria-label isn't available
                        span = name_tag.find('span')
                        product_name = span.get_text(strip=True) if span else name_tag.get_text(strip=True)
                else:
                    product_name = None
                
                # Extract price
                price_tag = product.find('span', {'class': 'a-price-whole'})
                price = price_tag.get_text(strip=True) if price_tag else None
                if price:
                    price = f"${price}"
                
                # Extract original price (if discounted)
                original_price_tag = product.find('span', {'class': 'a-price a-text-price'})
                original_price = original_price_tag.find('span', {'class': 'a-offscreen'}).get_text(strip=True) if original_price_tag else None
                
                # Extract rating
                rating_tag = product.find('span', {'class': 'a-icon-alt'})
                rating = rating_tag.get_text(strip=True).split()[0] if rating_tag else None
                
                # Extract review count
                review_count_tag = product.find('span', {'class': 'a-size-base'})
                review_count = review_count_tag.get_text(strip=True) if review_count_tag else None
                
                # Check if sponsored
                sponsored_tag = product.find('span', {'class': 'a-color-secondary'})
                is_sponsored = "Sponsored" in sponsored_tag.get_text(strip=True) if sponsored_tag else False
                
                # Extract product URL and ASIN
                link_tag = product.find('a', {'class': 'a-link-normal'})
                product_url = f"https://www.amazon.com{link_tag['href']}" if link_tag else None
                asin = link_tag['href'].split('/dp/')[1].split('/')[0] if link_tag and '/dp/' in link_tag['href'] else None
                
                # Write to CSV
                writer.writerow({
                    'product_name': product_name,
                    'price': price,
                    'original_price': original_price,
                    'rating': rating,
                    'review_count': review_count,
                    'is_sponsored': is_sponsored,
                    'product_url': product_url,
                    'asin': asin
                })
                
            except Exception as e:
                print(f"Error processing product: {e}")
                continue
    
    print(f"Successfully converted {html_file} to {csv_file} with {len(products)} products")

# Example usages:
# scrape_amazon_multipage("wireless headphones", 2)  # Will automatically create CSV
# html_to_csv()  # Will use the most recent HTML file in output directory
# html_to_csv("amazon_scraper_output/amazon_laptop_products.html")  # Specific file
