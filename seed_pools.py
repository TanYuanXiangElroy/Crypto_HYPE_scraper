# seed_pools.py
import logging
from database import add_pool, delete_all_pool

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- List of pools to initially monitor ---
pools_to_scrape = [
    {
        "dex_name": "Hyperliquid DEX", 
        "scraper_function": "hyperliquid_native",
        "network": "hyperliquid",
        "pool_address": "0x13ba5fea7078ab3798fbce53b4d0721c", # This is a sample, might not be the actual HYPE pool
        "target_token_address": "0x0d01dc56dcaaca66ad901c959b4011ec", # Using this field for the token symbol for this specific scraper
    },
    {
        "dex_name": "Upheaval",
        "scraper_function": "geckoterminal",
        "network": "hyperevm",
        "pool_address": "0x2621bdceb7584241dd8ed3d7ee46938b34060e77",
        "target_token_address": "0x5555555555555555555555555555555555555555", # WHYPE
    },
    {
        "dex_name": "Project X",
        "scraper_function": "geckoterminal",
        "network": "hyperevm",
        "pool_address": "0x6c9a33e3b592c0d65b3ba59355d5be0d38259285",
        "target_token_address": "0x5555555555555555555555555555555555555555", # WHYPE
    },
    {
        "dex_name": "HyperSwap V3",
        "scraper_function": "geckoterminal",
        "network": "hyperevm",
        "pool_address": "0xe712d505572b3f84c1b4deb99e1beab9dd0e23c9",
        "target_token_address": "0x5555555555555555555555555555555555555555", # WHYPE
    },
    {
    "dex_name": "KittenSwap Algebra", 
    "scraper_function": "geckoterminal",
    "network": "hyperevm", 
    "pool_address": "0x12df9913e9e08453440e3c4b1ae73819160b513e",
    "target_token_address": "0x5555555555555555555555555555555555555555", # WHYPE
    },
    {
        "dex_name": "ultrasolid-v3", 
        "scraper_function": "geckoterminal",
        "network": "hyperevm", 
        "pool_address": "0x3e69297ae794011970256623b4ab68324983b9ed",
        "target_token_address": "0x5555555555555555555555555555555555555555", # WHYPE
    },

]

def seed_pools():
    """
    Wipes and seeds the monitored_pools table with predefined pools
    by using the centralized database functions.
    """
    logging.info("--- Starting to seed database ---")

    # 1. Clear existing pools to ensure a clean slate
    logging.info("Deleting all existing pools...")
    delete_all_pool()

    # 2. Add each new pool from the list
    logging.info(f"Adding {len(pools_to_scrape)} new pools...")
    for pool in pools_to_scrape:
        add_pool(pool)
    
    logging.info("--- Database seeding complete ---")

if __name__ == "__main__":
    seed_pools()
    
