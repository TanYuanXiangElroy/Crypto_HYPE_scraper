# scrapers/hyperliquid_native.py

import requests
import logging
import config
from .exceptions import ScrapingError

def scrape(target_token_symbol="HYPE", **kwargs):
    """
    Scrapes the official Hyperliquid Spot Price using the 'tokenDetails' endpoint.
    
    Raises:
        ScrapingError: For any issues during the scraping process.
    """
    logging.info(f"Starting Native API scrape for Hyperliquid ({target_token_symbol})")

    headers = {"Content-Type": "application/json"}
    
    payload = {
        "type": "tokenDetails",
        "tokenId": config.HYPE_TOKEN_ID
    }

    try:
        response = requests.post(config.HYPERLIQUID_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        # The API returns 'midPx' (Mid Price) and 'markPx' (Mark Price)
        # We'll use midPx as it usually represents the current spot price best
        if 'midPx' not in data:
            raise ScrapingError(f"Price data ('midPx') not found in Hyperliquid response for {target_token_symbol}")

        spot_price = float(data['midPx'])
        
        # Hyperliquid Spot fees are generally 0 for this type of data check
        fee_percentage = 0.0

        logging.info(f"Successfully scraped Hyperliquid Native Price: ${spot_price:.4f}")
        
        return {
            'spot_price': spot_price,
            'pool_name': f"{target_token_symbol} / USDC (Native)",
            'fee_percentage': fee_percentage,
            'buy_price': spot_price, 
            'sell_price': spot_price
        }

    except requests.exceptions.HTTPError as http_err:
        response_text = http_err.response.text if http_err.response is not None else "No response body available."
        raise ScrapingError(f"Hyperliquid API request failed: {http_err}. Response: {response_text}") from http_err
    except (KeyError, ValueError) as e:
        raise ScrapingError(f"Failed to parse Hyperliquid API response: {e}") from e
    except Exception as e:
        raise ScrapingError(f"An unexpected error occurred in Hyperliquid Native scraper: {e}") from e