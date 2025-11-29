# main.py (The Worker)
import logging
from datetime import datetime

from scraper import SCRAPER_DISPATCHER
from scraper.exceptions import ScrapingError
from database import store_price_data, getting_pools_to_scrape
import config


def main():
    """Main function to run the scraping job."""
    logging.info(f"--- Running scrape job at {datetime.now()} ---")

    pools_to_scrape = getting_pools_to_scrape()
    
    if not pools_to_scrape:
        logging.warning("No pools found in database to scrape.")
        return

    # --- Loop through the pools and scrape data ---
    for pool in pools_to_scrape:
        logging.info(f"\n--- Scraping {pool['dex_name']} ---")
        
        scraper_name = pool.get('scraper_function')
        scraper_to_run = SCRAPER_DISPATCHER.get(scraper_name)

        if not scraper_to_run:
            logging.error(f"Scraper '{scraper_name}' for pool '{pool['dex_name']}' not found in dispatcher. Skipping.")
            continue

        try:
            # Dynamically call the correct scraper function
            price_data = scraper_to_run(
                network=pool.get('network'),
                pool_address=pool.get('pool_address'),
                target_token_address=pool.get('target_token_address')
            )
            
            if price_data:
                token_pair_name = price_data.get('pool_name', 'Unknown Pair')
                store_price_data(
                    dex_name=pool['dex_name'],
                    token_pair=token_pair_name,
                    data=price_data
                )
            else:
                logging.warning(f"-> No data returned from {scraper_name} for {pool['dex_name']}. Skipping database insert.")
        
        except ScrapingError as e:
            logging.error(f"A known scraping error occurred during {pool['dex_name']} scrape: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred during {pool['dex_name']} scrape: {e}", exc_info=True)

    logging.info("--- Job finished ---")

# Main execution block
if __name__ == "__main__":
    # Ensure logging is configured when running this file directly
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("cron.log"), # Log to a file
            logging.StreamHandler()          # And to the console
        ]
    )
    main()
    