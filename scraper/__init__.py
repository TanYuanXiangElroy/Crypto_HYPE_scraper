#scraper/__init__.py

""""
#scraper for selenium driverr wrapper
from .hyperliquid import scrape as scrape_hyperliquid
from .based_one import scrape as scrape_based_one
from .prjx import scrape as scrape_prjx
from .lighter import scrape as scrape_lighter
from .geckoterminal import scrape as scrape_geckoterminal
"""

# Add a new line here every time you add a new DEX file
# from .thruster_finance import scrape as scrape_thruster_finance

from .upheaval_v3_rpc import scrape as scrape_upheaval_v3_rpc

from .hyperliquid_native import scrape as scrape_hyperliquid_native


# Import the geckoterminal_api scraper
from .geckoterminal_api import scrape_gecko_terminal_pool