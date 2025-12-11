# scrapers/upheaval_v3_rpc.py

from web3 import Web3
import logging
import config
from .exceptions import ScrapingError

def scrape(**kwargs):
    """
    Scrapes the HYPE/USDC price from a Uniswap V3-style pool on Hyperliquid.
    
    Raises:
        ScrapingError: For any issues during the scraping process.
    """
    logging.info("Starting RPC scrape for Upheaval (V3-style) HYPE/USDC")

    # We use a standard, minimal V3 ABI since the contract is not verified
    pool_abi = """
    [{"inputs":[],"name":"slot0","outputs":[{"internalType":"uint160","name":"sqrtPriceX96","type":"uint160"},{"internalType":"int24","name":"tick","type":"int24"},{"internalType":"uint16","name":"observationIndex","type":"uint16"},{"internalType":"uint16","name":"observationCardinality","type":"uint16"},{"internalType":"uint16","name":"observationCardinalityNext","type":"uint16"},{"internalType":"uint8","name":"feeProtocol","type":"uint8"},{"internalType":"bool","name":"unlocked","type":"bool"}],"stateMutability":"view","type":"function"}]
    """

    try:
        # --- Connect and Set Up ---
        web3 = Web3(Web3.HTTPProvider(config.HYPERLIQUID_RPC_URL))
        if not web3.is_connected():
            raise ScrapingError(f"Could not connect to the Hyperliquid RPC endpoint at {config.HYPERLIQUID_RPC_URL}")
        
        checksum_address = web3.to_checksum_address(config.UPHEAVAL_V3_POOL_ADDRESS)
        contract = web3.eth.contract(address=checksum_address, abi=pool_abi)

        # --- Get Data from the Blockchain ---
        slot0 = contract.functions.slot0().call()
        sqrt_price_x96 = slot0[0]

        if sqrt_price_x96 == 0:
            raise ScrapingError("slot0 returned a sqrtPriceX96 of 0, cannot calculate price.")

        # --- Process the Data (V3 Price Calculation) ---
        price_ratio = (sqrt_price_x96 / (2**96)) ** 2
        
        decimal_adjustment = 10**(config.HYPE_DECIMALS - config.USDC_DECIMALS)
        price = price_ratio / decimal_adjustment
        
        logging.info(f"Successfully scraped Upheaval (V3) Price via RPC: {price:.6f}")
        
        # Note: This is a raw price from the pool. Fee calculation for V3 is complex
        # and depends on the swap direction and tick spacing. For now, we assume no fee.
        return {
            'spot_price': price,
            'pool_name': "HYPE / USDC (Upheaval V3)",
            'fee_percentage': 0.0,
            'buy_price': price,
            'sell_price': price
        }

    except Exception as e:
        raise ScrapingError(f"An unexpected error occurred in Upheaval (V3) scraper: {e}") from e
