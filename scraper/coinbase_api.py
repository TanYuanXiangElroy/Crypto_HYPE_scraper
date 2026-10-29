import requests
import logging
from .exceptions import ScrapingError

def scrape_coinbase(**kwargs):
    """
    Scrapes the spot price using the Coinbase free public API.
    """
    target_token_symbol = kwargs.get('target_token_address', 'HYPE')
    symbol = f"{target_token_symbol}-USD"
    logging.info(f"Starting API scrape for Coinbase (Symbol: {symbol})")

    url = f"https://api.coinbase.com/v2/prices/{symbol}/spot"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        spot_price = float(data['data']['amount'])

        # Coinbase fee varies but let's assume 0.5% average
        fee_percentage = 0.5
        fee_multiplier = fee_percentage / 100

        effective_buy_price = spot_price / (1 - fee_multiplier)
        effective_sell_price = spot_price * (1 - fee_multiplier)

        # Assuming a flat withdrawal fee for Coinbase, e.g., 1.0 USD
        transfer_fee = 1.0

        logging.info(f"Successfully scraped Price for {symbol} on Coinbase: Spot=${spot_price:.6f}")

        return {
            'spot_price': spot_price,
            'pool_name': symbol,
            'fee_percentage': fee_percentage,
            'buy_price': effective_buy_price,
            'sell_price': effective_sell_price,
            'transfer_fee': transfer_fee
        }

    except requests.exceptions.HTTPError as http_err:
        raise ScrapingError(f"Coinbase API request failed: {http_err}. Response: {http_err.response.text}") from http_err
    except (KeyError, ValueError) as e:
        raise ScrapingError(f"Failed to parse Coinbase API response: {e}") from e
    except Exception as e:
        raise ScrapingError(f"An unexpected error occurred in Coinbase scraper: {e}") from e
