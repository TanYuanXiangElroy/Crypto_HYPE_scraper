#run once and then exit

# scraper.py (The Worker)
import os
import sqlite3
import logging
from datetime import datetime

from scraper import scrape_hyperliquid, scrape_based_one, scrape_prjx, scrape_lighter, scrape_geckoterminal
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
    
    # Scrape Hyperliquid
    try:
        hyperliquid_data = scrape_hyperliquid()
        if hyperliquid_data:
            store_price_data(dex_name='Hyperliquid', token_pair='HYPE/USDC', price=hyperliquid_data['price'])
    except ScrapingError as e:
        logging.error(f"Failed to scrape Hyperliquid: {e}")

    # Scrape Based.one ---
    try:
        based_one_data = scrape_based_one()
        if based_one_data:
            store_price_data(dex_name='Based.one',  token_pair='HYPE/USDC', price=based_one_data['price'])
    except ScrapingError as e:
        logging.error(f"Failed to scrape Based.one: {e}")

    # Scrape prijx.one ---
    try:
        prjx_data = scrape_prjx()
        if prjx_data:
            store_price_data(dex_name='prjx',  token_pair='HYPE/USDC', price=prjx_data['price'])
    except ScrapingError as e:
        logging.error(f"Failed to scrape prjx: {e}")
        
    # Scrape lighter ---
    try:
        lighter_data = scrape_lighter()
        if lighter_data:
            store_price_data(dex_name='lighter',  token_pair='HYPE/USDC', price=lighter_data['price'])
    except ScrapingError as e:
        logging.error(f"Failed to scrape lighter: {e}")

    # Scrape geckoterminal ---
    try:
        geckoterminal_data = scrape_geckoterminal()
        if geckoterminal_data:
            store_price_data(dex_name='geckoterminal',  token_pair='HYPE/USDC', price=geckoterminal_data['price'])
    except ScrapingError as e:
        logging.error(f"Failed to scrape geckoterminal: {e}")

    logging.info("--- Job finished ---")

# Main execution block
if __name__ == "__main__":
    main()