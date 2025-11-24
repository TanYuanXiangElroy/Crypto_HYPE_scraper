# seed_pools.py
import sqlite3

# --- List of pools to scrape from GeckoTerminal ---
"""
HYPE: 0x0d01dc56dcaaca66ad901c959b4011ec
WHYPE: 0x5555555555555555555555555555555555555555
USDC: 0xb88339cb7199b77e23db6e890353e22632ba630f


{ #outdated example as the pool is too small so give wrong data
    "dex_name": "ramses-v3-hyperevm", 
    "scraper_function": "geckoterminal",
    "network": "hyperevm", 
    "pool_address": "0xebe8bbbf8e9582ef7c8f7705f4458e6ee34850ae",
    "target_token_address": "0x5555555555555555555555555555555555555555",
}
"""
pools_to_scrape = [
    {
    "dex_name": "Hyperliquid DEX", 
    "scraper_function": "hyperliquid_native",
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

]

def seed_pools():
    """Function to seed the monitored_pools table with predefined pools."""
    conn = sqlite3.connect('prices.db')
    cursor = conn.cursor()

    # Clear existing config to avoid duplicates (optional)
    cursor.execute('DELETE FROM monitored_pools')

    for pool in pools_to_scrape:
        cursor.execute('''
        INSERT INTO monitored_pools (dex_name, scraper_function, network, pool_address, target_token_address)
        VALUES (?, ?, ?, ?, ?)
        ''', (
            pool['dex_name'],
            pool['scraper_function'],
            pool['network'],
            pool['pool_address'],
            pool['target_token_address']
        ))

    conn.commit()
    conn.close()
    print("Monitored pools seeded successfully.")

if __name__ == "__main__":
    seed_pools()