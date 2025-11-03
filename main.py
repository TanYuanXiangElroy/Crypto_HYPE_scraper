#run once and then exit

# scraper.py (The Worker)
import sqlite3
from datetime import datetime

from scraper import scrape_hyperliquid, scrape_based_one, scrape_prjx, scrape_lighter, scrape_geckoterminal


def store_price_data(dex_name, token_pair, price):
    """Inserts a new price record into the SQLite database."""
    conn = sqlite3.connect('prices.db')
    cursor = conn.cursor()
    
    timestamp = datetime.now()
    
    try:
        cursor.execute('''
        INSERT INTO hype_prices (timestamp, dex_name, token_pair, price)
        VALUES (?, ?, ?, ?)
        ''', (timestamp, dex_name, token_pair, price))
        
        conn.commit()
        print(f"Successfully stored: {dex_name} - {token_pair} - ${price}")
    except Exception as e:
        print(f"Error storing data: {e}")
    finally:
        conn.close()


def main():
    """Main function to run the scraping job."""
    print(f"--- Running scrape job at {datetime.now()} ---")
    
    
    """
# Scrape Hyperliquid
    hyperliquid_data = scrape_hyperliquid()
    if hyperliquid_data:
        store_price_data(dex_name='Hyperliquid', token_pair='HYPE/USDC', price=hyperliquid_data['price'])

    # Scrape Based.one ---
    based_one_data = scrape_based_one()
    if based_one_data:
        store_price_data(dex_name='Based.one',  token_pair='HYPE/USDC', price=based_one_data['price'])

    # Scrape prijx.one ---
    prjx_data = scrape_prjx()
    if prjx_data:
        store_price_data(dex_name='prjx',  token_pair='HYPE/USDC', price=prjx_data['price'])
        

# Scrape lighter ---
    lighter_data = scrape_lighter()
    if lighter_data:
        store_price_data(dex_name='lighter',  token_pair='HYPE/USDC', price=lighter_data['price'])
"""
    # Scrape geckoterminal ---
    geckoterminal_data = scrape_geckoterminal()
    if geckoterminal_data:
        store_price_data(dex_name='geckoterminal',  token_pair='HYPE/USDC', price=geckoterminal_data['price'])
    print("--- Job finished ---")

# Main execution block
if __name__ == "__main__":
    main()