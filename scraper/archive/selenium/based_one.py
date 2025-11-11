import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from scraper.driver import get_webdriver
from config import SCRAPER_CONFIG
from scraper.exceptions import ScrapingError

def scrape():
    """Scrapes HYPE price from Based.one using Selenium in headless mode."""
    logging.info("Scraping Based.one...")
    config = SCRAPER_CONFIG['based_one']
    driver = get_webdriver()
    try:
        logging.info(f"   Getting URL: {config['url']}")
        driver.get(config['url'])
        
        wait = WebDriverWait(driver, 20)
        price_element = wait.until(EC.presence_of_element_located((By.XPATH , config['selector'])))
        
        price_text = price_element.get_attribute('value') or price_element.text
        
        price = float(price_text.replace('$', '').strip())
        return {'price': price}
        
    except TimeoutException:
        logging.error("Error scraping Based.one: Timed out waiting for price element.")
        driver.save_screenshot('debug_screenshot_based.png')
        logging.info("   Screenshot saved as debug_screenshot_based.png for inspection.")
        raise ScrapingError("Timed out waiting for price element on Based.one")
    except Exception as e:
        logging.error(f"Error scraping Based.one: {e}")
        raise ScrapingError(f"An unexpected error occurred on Based.one: {e}")
    finally:
        driver.quit()
