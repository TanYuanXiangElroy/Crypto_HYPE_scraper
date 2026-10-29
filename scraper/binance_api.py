import requests
import logging
from .exceptions import ScrapingError

def scrape_binance(**kwargs):
    """
    Scrapes the spot price using the Binance.US free public API.
    Note: Binance US is available in the US.
    """
    target_token_symbol = kwargs.get('target_token_address', 'HYPE')
    symbol = f"{target_token_symbol}USD"
    logging.info(f"Starting API scrape for Binance.US (Symbol: {symbol})")

    url = f"https://api.binance.us/api/v3/ticker/price?symbol={symbol}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        spot_price = float(data['price'])

        # Binance.US spot fee varies but 0.1% is typical base
        fee_percentage = 0.1
        fee_multiplier = fee_percentage / 100

        effective_buy_price = spot_price / (1 - fee_multiplier)
        effective_sell_price = spot_price * (1 - fee_multiplier)

        # Assuming a flat withdrawal/transfer fee for Binance, e.g., 0.5 USD
        transfer_fee = 0.5

        logging.info(f"Successfully scraped Price for {symbol} on Binance.US: Spot=${spot_price:.6f}")

        return {
            'spot_price': spot_price,
            'pool_name': symbol,
            'fee_percentage': fee_percentage,
            'buy_price': effective_buy_price,
            'sell_price': effective_sell_price,
            'transfer_fee': transfer_fee
        }

    except requests.exceptions.HTTPError as http_err:
        raise ScrapingError(f"Binance.US API request failed: {http_err}. Response: {http_err.response.text}") from http_err
    except (KeyError, ValueError) as e:
        raise ScrapingError(f"Failed to parse Binance.US API response: {e}") from e
    except Exception as e:
        raise ScrapingError(f"An unexpected error occurred in Binance.US scraper: {e}") from e
