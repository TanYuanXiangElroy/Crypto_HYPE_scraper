# config.py

import os

# This gets the directory where the config.py script itself is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, 'prices.db') # Joins the directory path and the filename

# --- Server Configuration ---
API_PORT = 5000

# --- Scraper Endpoints ---
GECKO_TERMINAL_API_BASE_URL = "https://api.geckoterminal.com/api/v2"
HYPERLIQUID_API_URL = "https://api.hyperliquid.xyz/info"
HYPERLIQUID_RPC_URL = "https://api.hyperliquid.xyz/evm"

# --- Contract & Token Configuration ---
HYPE_TOKEN_ID = "0x0d01dc56dcaaca66ad901c959b4011ec"
UPHEAVAL_V3_POOL_ADDRESS = "0x2621bdceb7584241dd8ed3d7ee46938b34060e77"
HYPE_DECIMALS = 18
USDC_DECIMALS = 6