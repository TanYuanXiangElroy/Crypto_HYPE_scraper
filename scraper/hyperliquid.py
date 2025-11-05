import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from scraper.driver import get_webdriver
from config import SCRAPER_CONFIG
from scraper.exceptions import ScrapingError

def scrape():
    """ Scrapes HYPE price from Hyperliquid by reading the page title."""
    logging.info("Scraping Hyperliquid...")
    config = SCRAPER_CONFIG['hyperliquid']
    driver = get_webdriver()
    try:
        driver.get(config['url'])

        WebDriverWait(driver, 15).until(EC.title_contains("HYPE"))
        
        page_title = driver.title
        
        price_text = page_title.split('|')[0].strip()
        
        price = float(price_text)
        return {'price': price}
            
    except TimeoutException:
        logging.error("   Error scraping hyperliquid.xyz: Timed out waiting for the title to load.")
        driver.save_screenshot('debug_screenshot_HL.png')
        logging.info("   Screenshot saved as debug_screenshot.png for inspection.")
        raise ScrapingError("Timed out waiting for title to load on hyperliquid.xyz")
    except Exception as e:
        logging.error(f"   An unexpected error occurred in scrape_hyperliquid: {e}")
        logging.error(f"   Could not parse the title: '{driver.title}'")
        raise ScrapingError(f"An unexpected error occurred on hyperliquid.xyz: {e}")
    finally:
        logging.info("   Closing webdriver.")
        driver.quit()
