# scrapers/upheaval_v3_rpc.py

from web3 import Web3

def scrape():
    """Scrapes the HYPE/USDC price from a Uniswap V3-style pool on Hyperliquid."""
    print("-> Starting RPC scrape for Upheaval (V3-style) HYPE/USDC...")

    # --- Configuration ---
    rpc_url = "https://api.hyperliquid.xyz/evm"
    # The V3 pool address you found on GeckoTerminal
    pool_address = "0x2621bdceb7584241dd8ed3d7ee46938b34060e77"
    
    # We use a standard, minimal V3 ABI since the contract is not verified
    pool_abi = """
    [{"inputs":[],"name":"slot0","outputs":[{"internalType":"uint160","name":"sqrtPriceX96","type":"uint160"},{"internalType":"int24","name":"tick","type":"int24"},{"internalType":"uint16","name":"observationIndex","type":"uint16"},{"internalType":"uint16","name":"observationCardinality","type":"uint16"},{"internalType":"uint16","name":"observationCardinalityNext","type":"uint16"},{"internalType":"uint8","name":"feeProtocol","type":"uint8"},{"internalType":"bool","name":"unlocked","type":"bool"}],"stateMutability":"view","type":"function"}]
    """
    # You MUST verify the decimals for WHYPE and USDC on the Hyperliquid chain
    hype_decimals = 18
    usdc_decimals = 6

    try:
        # --- Connect and Set Up ---
        web3 = Web3(Web3.HTTPProvider(rpc_url))
        if not web3.is_connected():
            print("   Error: Could not connect to the Hyperliquid RPC endpoint.")
            return None
        
        checksum_address = web3.to_checksum_address(pool_address)
        contract = web3.eth.contract(address=checksum_address, abi=pool_abi)

        # --- Get Data from the Blockchain ---
        # Call the 'slot0' function on the V3 pool contract
        slot0 = contract.functions.slot0().call()
        sqrt_price_x96 = slot0[0]

        # --- Process the Data (V3 Price Calculation) ---
        # The formula to convert sqrtPriceX96 to a normal price is:
        # price = (sqrtPriceX96 / 2**96)**2
        # We also need to adjust for the token decimals.
        
        price_ratio = (sqrt_price_x96 / (2**96)) ** 2
        
        # The final price adjustment depends on which token is token0 vs token1.
        # For a USDC/WHYPE pool, this formula gives the price of WHYPE in USDC.
        decimal_adjustment = 10**(hype_decimals - usdc_decimals)
        price = price_ratio / decimal_adjustment
        
        print(f"   Successfully scraped Upheaval (V3) Price via RPC: {price:.6f}")
        return {'main_price': price}

    except Exception as e:
        print(f"   An unexpected error occurred in Upheaval (V3) scraper: {e}")
        return None