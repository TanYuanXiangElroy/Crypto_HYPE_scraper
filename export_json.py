import json
from database import get_all_data_of_DEX
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def calculate_arbitrage_opportunities(prices_data):
    """
    Finds arbitrage opportunities from the given price data.
    Prices data should be a list of dictionaries.
    """
    # Just use the latest entry for each DEX to calculate current opportunities
    latest_prices = {}
    for entry in prices_data:
        dex = entry['dex_name']
        if dex not in latest_prices:
            latest_prices[dex] = entry

    opportunities = []
    dex_names = list(latest_prices.keys())

    for i in range(len(dex_names)):
        for j in range(len(dex_names)):
            if i == j:
                continue

            buy_dex = dex_names[i]
            sell_dex = dex_names[j]

            buy_data = latest_prices[buy_dex]
            sell_data = latest_prices[sell_dex]

            if buy_data['buy_price'] is None or sell_data['sell_price'] is None:
                continue

            # Assume 1 unit of token. Total cost to buy on buy_dex and transfer it
            total_buy_cost = buy_data['buy_price'] + (buy_data['transfer_fee'] or 0)
            # Total revenue from selling on sell_dex
            total_sell_revenue = sell_data['sell_price']

            profit = total_sell_revenue - total_buy_cost

            if profit > 0:
                opportunities.append({
                    "buy_exchange": buy_dex,
                    "sell_exchange": sell_dex,
                    "profit": profit,
                    "buy_price": buy_data['buy_price'],
                    "sell_price": sell_data['sell_price'],
                    "transfer_fee": buy_data['transfer_fee'],
                    "token_pair": buy_data['token_pair']
                })

    return opportunities, list(latest_prices.values())

def main():
    all_data = get_all_data_of_DEX(limit=100) # Get a chunk of recent data
    if all_data is None:
        logging.error("Failed to fetch data from database.")
        return

    opportunities, latest = calculate_arbitrage_opportunities(all_data)

    export_data = {
        "latest_prices": latest,
        "arbitrage_opportunities": opportunities
    }

    with open("data.json", "w") as f:
        json.dump(export_data, f, indent=4, default=str)

    logging.info("Successfully exported data to data.json")

if __name__ == "__main__":
    main()
