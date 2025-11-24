#run once and then exit

# main.py (The Worker)
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

def store_price_data(dex_name, token_pair, data):
    """Inserts a new price record into the SQLite database using an absolute path."""
    # Connect to the database using the absolute DB_PATH
    conn = sqlite3.connect(DB_PATH) 
    cursor = conn.cursor()
    
    timestamp = datetime.now()
    
    
    try:
        cursor.execute('''
        INSERT INTO hype_prices (timestamp, dex_name, token_pair, spot_price, fee_percentage, buy_price, sell_price)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            timestamp, 
            dex_name, 
            token_pair, 
            data.get('spot_price'),
            data.get('fee_percentage'),
            data.get('buy_price'),
            data.get('sell_price')
        ))
        
        conn.commit()
        logging.info(f"-> Successfully stored: {dex_name} | {token_pair} | Spot Price=${data.get('spot_price'):.4f}")
    except Exception as e:
        logging.error(f"-> Error storing data: {e}")
    finally:
        conn.close()

def getting_pools_to_scrape():
    """Fetches the list of pools to scrape from the monitored_pools table."""
    conn = sqlite3.connect(DB_PATH)
    # This allows us to access columns by name (row['dex_name'])
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM monitored_pools")
        rows = cursor.fetchall()
        # Convert database rows to a list of dictionaries just like your old hardcoded list
        pools = [dict(row) for row in rows]
        return pools
    except Exception as e:
        logging.error(f"Error fetching pools config: {e}")
        return []
    finally:
        conn.close()

def main():
    """Main function to run the scraping job."""
    logging.info(f"--- Running scrape job at {datetime.now()} ---")

    pools_to_scrape = getting_pools_to_scrape()
    
    if not pools_to_scrape:
        logging.warning("No pools found in database to scrape.")
        return

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
            
            if price_data:
                token_pair_name = price_data.get('pool_name', 'Unknown Pair')
                
                store_price_data(
                    dex_name=pool['dex_name'],
                    token_pair=token_pair_name,
                    data=price_data
                )
            else:
                print(f"-> Skipping database insert for {pool['dex_name']} due to scraping failure.")
        except Exception as e:
            print(f"An error occurred during {pool['dex_name']} scrape: {e}")

    logging.info("--- Job finished ---")

# Main execution block
if __name__ == "__main__":
    main()