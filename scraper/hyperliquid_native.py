# scrapers/hyperliquid_native.py

import requests

def scrape(target_token_symbol="HYPE"):
    """
    Scrapes the official Hyperliquid Spot Price using the 'tokenDetails' endpoint.
    """
    print(f"-> Starting Native API scrape for Hyperliquid ({target_token_symbol})...")

    url = "https://api.hyperliquid.xyz/info"
    headers = {"Content-Type": "application/json"}
    
    # The HYPE Token Contract Address on HyperEVM
    # Found via Explorer/Docs
    hype_token_id = "0x0d01dc56dcaaca66ad901c959b4011ec"

    payload = {
        "type": "tokenDetails",
        "tokenId": hype_token_id
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        # The API returns 'midPx' (Mid Price) and 'markPx' (Mark Price)
        # We'll use midPx as it usually represents the current spot price best
        if 'midPx' not in data:
            print(f"   Error: Price data (midPx) not found in response for {target_token_symbol}")
            return None

        spot_price = float(data['midPx'])
        
        # Hyperliquid Spot fees are generally 0 for this type of data check
        fee_percentage = 0.0

        print(f"   Successfully scraped Hyperliquid Native Price: ${spot_price:.4f}")
        
        return {
            'spot_price': spot_price,
            'pool_name': f"{target_token_symbol} / USDC (Native)",
            'fee_percentage': fee_percentage,
            'buy_price': spot_price, 
            'sell_price': spot_price
        }

    except Exception as e:
        print(f"   An unexpected error occurred in Hyperliquid Native scraper: {e}")
        return None