#run once and then exit

# scraper.py (The Worker)
import os
import sqlite3
import logging
from datetime import datetime

from scraper import scrape_gecko_terminal_pool
from scraper.exceptions import ScrapingError

# This gets the directory where the main.py script itself is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, 'prices.db') # Joins the directory path and the filename

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def store_price_data(dex_name, token_pair, price):
    """Inserts a new price record into the SQLite database using an absolute path."""
    # Connect to the database using the absolute DB_PATH
    conn = sqlite3.connect(DB_PATH) 
    cursor = conn.cursor()
    
    timestamp = datetime.now()
    
    try:
        cursor.execute('''
        INSERT INTO hype_prices (timestamp, dex_name, token_pair, price)
        VALUES (?, ?, ?, ?)
        ''', (timestamp, dex_name, token_pair, price))
        
        conn.commit()
        logging.info(f"-> Successfully stored: {dex_name} | {token_pair} | ${price}")
    except Exception as e:
        logging.error(f"-> Error storing data: {e}")
    finally:
        conn.close()

def main():
    """Main function to run the scraping job."""
    logging.info(f"--- Running scrape job at {datetime.now()} ---")

    # --- List of pools to scrape from GeckoTerminal ---
    """
    HYPE: 0x0d01dc56dcaaca66ad901c959b4011ec
    WHYPE: 0x5555555555555555555555555555555555555555
    USDC: 0xb88339cb7199b77e23db6e890353e22632ba630f
    """
    pools_to_scrape = [
        {
        "dex_name": "Hyperliquid DEX", 
        "scraper_function": "geckoterminal",
        "network": "hyperliquid", 
        "pool_address": "0x13ba5fea7078ab3798fbce53b4d0721c",
        "target_token_address": "0x0d01dc56dcaaca66ad901c959b4011ec",
    },
    {
        "dex_name": "Upheaval", 
        "scraper_function": "geckoterminal",
        "network": "hyperevm", 
        "pool_address": "0x2621bdceb7584241dd8ed3d7ee46938b34060e77",
        "target_token_address": "0x5555555555555555555555555555555555555555",
    },
    {
        "dex_name": "Project X", 
        "scraper_function": "geckoterminal",
        "network": "hyperevm", 
        "pool_address": "0x6c9a33e3b592c0d65b3ba59355d5be0d38259285",
        "target_token_address": "0x5555555555555555555555555555555555555555",
    },
    {
        "dex_name": "HyperSwap V3", 
        "scraper_function": "geckoterminal",
        "network": "hyperevm", 
        "pool_address": "0xe712d505572b3f84c1b4deb99e1beab9dd0e23c9",
        "target_token_address": "0x5555555555555555555555555555555555555555",
    },
    {
        "dex_name": "KittenSwap Algebra", 
        "scraper_function": "geckoterminal",
        "network": "hyperevm", 
        "pool_address": "0x12df9913e9e08453440e3c4b1ae73819160b513e",
        "target_token_address": "0x5555555555555555555555555555555555555555",
    },
    {
        "dex_name": "ultrasolid-v3", 
        "scraper_function": "geckoterminal",
        "network": "hyperevm", 
        "pool_address": "0x3e69297ae794011970256623b4ab68324983b9ed",
        "target_token_address": "0x5555555555555555555555555555555555555555",
    },
    {
        "dex_name": "ramses-v3-hyperevm", 
        "scraper_function": "geckoterminal",
        "network": "hyperevm", 
        "pool_address": "0xebe8bbbf8e9582ef7c8f7705f4458e6ee34850ae",
        "target_token_address": "0x5555555555555555555555555555555555555555",
    }
]

    # --- Loop through the pools and scrape data ---
    for pool in pools_to_scrape:
        print(f"\n--- Scraping {pool['dex_name']} ---")
        try:
            if pool['scraper_function'] == 'geckoterminal':
                price_data = scrape_gecko_terminal_pool(
                network=pool['network'],
                pool_address=pool['pool_address'],
                target_token_address=pool['target_token_address'] 
        )
            
            if scraped_data and 'main_price' in scraped_data:

                token_pair_name = scraped_data.get('pool_name', 'Unknown Pair')

                store_price_data(
                    dex_name=pool['dex_name'],
                    token_pair=token_pair_name, 
                    price=scraped_data['main_price']
                )
            else:
                print(f"-> Skipping database insert for {pool['dex_name']} due to scraping failure.")
        except Exception as e:
            print(f"An error occurred during {pool['dex_name']} scrape: {e}")

    logging.info("--- Job finished ---")

# Main execution block
if __name__ == "__main__":
    main()