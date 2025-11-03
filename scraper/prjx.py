from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def scrape():
    """
    Scrapes HYPE price from prjx using Selenium in headless mode.
    It uses dexscreener API to get the price data. but here we demonstrate
    Selenium usage for consistency with other scrapers.
    
    """
    print("Scraping prjx...")
    url = "https://www.prjx.com/swap?fromToken=0xb88339CB7199b77E23DB6E890353E22632Ba630f&fromChain=999&toToken=0x0000000000000000000000000000000000000000&toChain=999"
    
    # IMPORTANT: Configure Selenium for a server environment
    options = webdriver.ChromeOptions()
    options.add_argument('--headless') # Runs Chrome without a GUI
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36')
    
    driver = webdriver.Chrome(options=options)
    try:
        print(f"   Getting URL: {url}")
        driver.get(url)

        price_xpath_selector = "//p[contains(text(), 'HYPE')]/following-sibling::p"

        # Wait up to 20 seconds for the element with the price to appear
        wait = WebDriverWait(driver, 20)
        price_element = wait.until(EC.presence_of_element_located((By.XPATH , price_xpath_selector)))
        
        # This part depends heavily on the site. You might need to get a 'value' or 'innerText'.
        price_text = price_element.get_attribute('value') or price_element.text

        # Clean the extracted text to get a number
        price = float(price_text.replace('$', '').strip())
        return {'price': price}
        
    except TimeoutException:
        print("Error scraping prjx: Timed out waiting for price element.")
        driver.save_screenshot('debug_screenshot_prjx.png')
        print("   Screenshot saved as debug_screenshot_prjx.png for inspection.")
        return None
    except Exception as e:
        print(f"Error scraping prjx: {e}")
        return None
    finally:
        driver.quit()
