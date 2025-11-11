# scrapers/coingecko_api.py

import requests

def scrape_gecko_terminal_pool(network: str, pool_address: str, target_token_address: str):
    """
    Scrapes token price data from the GeckoTerminal API for a specific pool,
    targeting a specific token's price in USD.

    Args:
        network (str): The blockchain network ID (e.g., 'eth', 'hyperevm').
        pool_address (str): The address of the liquidity pool.
        target_token_address (str): The symbol of the token whose price is desired compared to the other (e.g., 'WHYPE', 'USDC').

    Returns:
        dict: A dictionary containing the scraped price, or None if scraping fails.
              Example: {'main_price': 123.45}
    """
    print(f"-> Starting API scrape for GeckoTerminal (Network: {network}, Pool: {pool_address}, Target: {target_token_address})...")

    url = f"https://api.geckoterminal.com/api/v2/networks/{network}/pools/{pool_address}"
    headers = {"accept": "application/json"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        # 1. Get the relationships and attributes
        relationships = data['data']['relationships']
        attributes = data['data']['attributes']

        # 2. Extract the IDs, which contain the addresses
        base_token_id = relationships['base_token']['data']['id']
        quote_token_id = relationships['quote_token']['data']['id']
        
        # The address is the part of the ID after the underscore
        base_token_address = base_token_id.split('_')[-1]
        quote_token_address = quote_token_id.split('_')[-1]

        # 3. Get the prices
        base_token_price_usd = attributes.get('base_token_price_usd')
        quote_token_price_usd = attributes.get('quote_token_price_usd')
        
        # 4. Determine which price to return by comparing addresses (case-insensitive)
        price = None
        
        if target_token_address.lower() == base_token_address.lower():
            price = float(base_token_price_usd)
        elif target_token_address.lower() == quote_token_address.lower():
            price = float(quote_token_price_usd)
        else:
            print(f"   Error: Target token address '{target_token_address}' not found in pool.")
            return None

        pool_name = attributes.get('name', 'Unknown Pair')
        print(f"   Successfully scraped Price for {pool_name}: {price:.6f}")

        return {
            'main_price': price,
            'pool_name': pool_name
            }

    except requests.exceptions.HTTPError as http_err:
        print(f"   HTTP error occurred: {http_err} - Check the network ID or Pool Address.")
        print(f"   Response Body: {response.text}")
        return None
    except Exception as e:
        print(f"   An unexpected error occurred in GeckoTerminal API scraper: {e}")
        return None