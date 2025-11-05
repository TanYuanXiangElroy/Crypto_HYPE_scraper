import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from scraper.driver import get_webdriver
from config import SCRAPER_CONFIG
from scraper.exceptions import ScrapingError

def scrape():
    """Scrapes the main displayed price (Last Traded Price) from Lighter."""
    logging.info("Scraping Lighter...")
    config = SCRAPER_CONFIG['lighter']
    driver = get_webdriver()
    
    try:
        logging.info(f"   Getting URL: {config['url']}")
        driver.get(config['url'])

        # --- NEW: POP-UP HANDLING BLOCK ---
        try:
            # Wait a few seconds for the pop-up's close button to be clickable
            close_button_xpath = "//button[@data-testid='notification-close-button']"
            logging.info("   Checking for announcement pop-up...")
            close_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, close_button_xpath))
            )
            logging.info("   Pop-up found. Clicking close button...")
            close_button.click()
            # Wait a second for the closing animation to finish
            time.sleep(1) 
        except TimeoutException:
            # If the pop-up doesn't appear after 10 seconds, just continue
            logging.info("   No pop-up found, continuing...")
            pass
    # --- END OF POP-UP HANDLING ---

        WebDriverWait(driver, 20).until(EC.title_contains("HYPE"))
        
        page_title = driver.title
        
        price_text = page_title.split('•')[0]
        
        price = float(price_text.replace('$', '').strip())

        return { 'price': price }
        
    except TimeoutException:
        logging.error("   Error scraping Lighter: Timed out waiting for main price element.")
        driver.save_screenshot('debug_screenshot_lighter.png')
        logging.info("   Screenshot saved as debug_screenshot_lighter.png for inspection.")
        raise ScrapingError("Timed out waiting for main price element on Lighter")
    except Exception as e:
        logging.error(f"   An unexpected error occurred in scrape_lighter: {e}")
        raise ScrapingError(f"An unexpected error occurred on Lighter: {e}")
    finally:
        logging.info("   Closing webdriver.")
        driver.quit()