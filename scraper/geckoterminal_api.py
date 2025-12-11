# scrapers/geckoterminal_api.py

import requests
import logging
import config
from .exceptions import ScrapingError

def scrape_gecko_terminal_pool(network: str, pool_address: str, target_token_address: str):
    """
    Scrapes token price data from the GeckoTerminal API for a specific pool,
    targeting a specific token's price in USD.

    Args:
        network (str): The blockchain network ID (e.g., 'eth', 'hyperevm').
        pool_address (str): The address of the liquidity pool.
        target_token_address (str): The address of the token whose price is desired.

    Returns:
        dict: A dictionary containing the scraped price data.
    
    Raises:
        ScrapingError: If there is a network issue, a problem with the API response,
                       or if the target token is not found in the pool.
    """
    logging.info(f"Starting API scrape for GeckoTerminal (Network: {network}, Pool: {pool_address})")

    url = f"{config.GECKO_TERMINAL_API_BASE_URL}/networks/{network}/pools/{pool_address}"
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
        
        base_token_address = base_token_id.split('_')[-1]
        quote_token_address = quote_token_id.split('_')[-1]

        # 3. Get the prices
        base_token_price_usd = attributes.get('base_token_price_usd')
        quote_token_price_usd = attributes.get('quote_token_price_usd')
        
        # 4. Determine which price to return
        spot_price = None
        
        if target_token_address.lower() == base_token_address.lower():
            spot_price = float(base_token_price_usd)
        elif target_token_address.lower() == quote_token_address.lower():
            spot_price = float(quote_token_price_usd)
        else:
            raise ScrapingError(f"Target token '{target_token_address}' not found in pool '{pool_address}'.")

        pool_name = attributes.get('name', 'Unknown Pair')

        fee_percentage_str = attributes.get('pool_fee_percentage')
        fee_percentage = 0.0
        
        if fee_percentage_str:
            try:
                fee_percentage = float(fee_percentage_str)
            except (ValueError, TypeError):
                logging.warning(f"Could not parse fee_percentage: '{fee_percentage_str}' for pool {pool_address}")
        
        fee_multiplier = fee_percentage / 100
        
        effective_buy_price = spot_price / (1 - fee_multiplier) if fee_multiplier < 1 else spot_price
        effective_sell_price = spot_price * (1 - fee_multiplier)

        logging.info(f"Successfully scraped Price for {pool_name}: Spot=${spot_price:.6f}")

        return {
            'spot_price': spot_price,
            'pool_name': pool_name,
            'fee_percentage': fee_percentage,
            'buy_price': effective_buy_price,
            'sell_price': effective_sell_price
        }

    except requests.exceptions.HTTPError as http_err:
        raise ScrapingError(f"GeckoTerminal API request failed: {http_err}. Response: {http_err.response.text}") from http_err
    except (KeyError, IndexError, TypeError) as e:
        raise ScrapingError(f"Failed to parse GeckoTerminal API response for pool {pool_address}: {e}") from e
    except Exception as e:
        raise ScrapingError(f"An unexpected error occurred in GeckoTerminal scraper for pool {pool_address}: {e}") from e
