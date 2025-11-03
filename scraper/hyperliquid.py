from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def scrape():
    """ Scrapes HYPE price from Hyperliquid by reading the page title."""
    print("Scraping Hyperliquid...")
    url = "https://app.hyperliquid.xyz/trade/HYPE"
    
    # IMPORTANT: Configure Selenium for a server environment
    # aka # Configure Selenium options for headless mode (runs without opening a browser window GUI)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36')

    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get(url)

        # Wait for the title to contain the token name "HYPE" to ensure it's loaded
        WebDriverWait(driver, 15).until(EC.title_contains("HYPE"))
        
        # Get the full title of the page
        page_title = driver.title
        
        # The title looks like: "0.1064 | HYPE | Hyperliquid"
        # We split the string by the "|" character and take the first part
        price_text = page_title.split('|')[0].strip()
        
        price = float(price_text)
        return {'price': price}
            
    except TimeoutException:
        print("   Error scraping hyperliquid.xyz: Timed out waiting for the title to load.")
        driver.save_screenshot('debug_screenshot_HL.png')
        print("   Screenshot saved as debug_screenshot.png for inspection.")
        return None
    except Exception as e:
        print(f"   An unexpected error occurred in scrape_hyperliquid: {e}")
        # This could happen if the title format changes, so we log it.
        print(f"   Could not parse the title: '{driver.title}'")
        return None
    finally:
        print("   Closing webdriver.")
        driver.quit()

