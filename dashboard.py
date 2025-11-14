# dashboard.py

import requests
import time
from rich.console import Console
from rich.table import Table
from rich.live import Live

# The URL of running API server
API_URL = "http://127.0.0.1:5000/data"

def generate_table() -> Table:
    """Fetches data from the API and generates a Rich table."""
    
    table = Table(title="HYPE Live Price Dashboard")
    table.add_column("Timestamp", style="cyan", no_wrap=True)
    table.add_column("DEX Name", style="magenta")
    table.add_column("Token Pair", style="yellow")
    table.add_column("Spot Price", justify="right", style="green")
    table.add_column("Fee %", justify="right", style="blue")
    table.add_column("Effective Buy Price", justify="right", style="bold green")
    table.add_column("Effective sell Price", justify="right", style="bold red")

    
    try:
        # Make a request to your API to get the latest 20 entries
        response = requests.get(f"{API_URL}?limit=30")
        response.raise_for_status() # Raise an exception for bad status codes
        data = response.json()
        
        if not data:
            table.add_row("No data found in the database yet...")
            return table

        for entry in data:
            # Safely get data and provide defaults
            timestamp = entry.get('timestamp', 'N/A')
            dex = entry.get('dex_name', 'N/A')
            pair = entry.get('token_pair', 'N/A')
            spot = entry.get('spot_price')
            fee = entry.get('fee_percentage')
            buy_price = entry.get('buy_price')
            sell_price = entry.get('sell_price')

            # Format the numbers for display
            spot_str = f"${spot:.4f}" if spot is not None else "N/A"
            fee_str = f"{fee:.3f}%" if fee is not None else "N/A"
            buy_price_str = f"${buy_price:.4f}" if buy_price is not None else "N/A"
            sell_price_str = f"${sell_price:.4f}" if sell_price is not None else "N/A"
            
            table.add_row(timestamp, dex, pair, spot_str, fee_str, buy_price_str, sell_price_str)
            
    except requests.exceptions.ConnectionError:
        table.add_row("[bold red]Error: Could not connect to the API server.[/bold red]")
        table.add_row("Is 'python api.py' running in another terminal?")
    except Exception as e:
        table.add_row(f"[bold red]An unexpected error occurred: {e}[/bold red]")

    return table

if __name__ == "__main__":
    # Use Rich's "Live" feature to create a display that updates automatically
    with Live(generate_table(), screen=True, refresh_per_second=4) as live:
        while True:
            # This loop will re-generate and update the table every 15 seconds
            time.sleep(15)
            live.update(generate_table())