# scrapers/lighter.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import time


def scrape():
    """Scrapes the main displayed price (Last Traded Price) from Lighter."""
    print("Scraping Lighter...")
    url = "https://app.lighter.xyz/trade/HYPE/" 
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36')
    
    driver = webdriver.Chrome(options=options)
    

    try:
        print(f"   Getting URL: {url}")
        driver.get(url)

        # --- NEW: POP-UP HANDLING BLOCK ---
        try:
            # Wait a few seconds for the pop-up's close button to be clickable
            close_button_xpath = "//button[@data-testid='notification-close-button']"
            print("   Checking for announcement pop-up...")
            close_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, close_button_xpath))
            )
            print("   Pop-up found. Clicking close button...")
            close_button.click()
            # Wait a second for the closing animation to finish
            time.sleep(1) 
        except TimeoutException:
            # If the pop-up doesn't appear after 10 seconds, just continue
            print("   No pop-up found, continuing...")
            pass
    # --- END OF POP-UP HANDLING ---

        #print("   Waiting for title to contain HYPE market data...")
        WebDriverWait(driver, 20).until(EC.title_contains("HYPE"))
        
        page_title = driver.title
        #print(f"   Page Title found: '{page_title}'")
        
        # The title format is: "$40.6773 • HYPE • Lighter"
        # We split by the bullet point character '•' and take the first part
        price_text = page_title.split('•')[0]
        
        price = float(price_text.replace('$', '').strip())
        #print(f"   Successfully scraped Lighter Main Price: {price}")

        return { 'price': price }
        
    except TimeoutException:
        print("   Error scraping Lighter: Timed out waiting for main price element.")
        driver.save_screenshot('debug_screenshot_lighter.png')
        print("   Screenshot saved as debug_screenshot_lighter.png for inspection.")
        return None
    except Exception as e:
        print(f"   An unexpected error occurred in scrape_lighter: {e}")
        return None
    finally:
        print("   Closing webdriver.")
        driver.quit()