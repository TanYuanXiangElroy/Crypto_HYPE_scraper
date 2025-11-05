# config.py

# Configuration for each scraper
SCRAPER_CONFIG = {
    'hyperliquid': {
        'url': "https://app.hyperliquid.xyz/trade/HYPE",
        'selector': None  # Uses title
    },
    'based_one': {
        'url': "https://app.based.one/HYPE/USDC",
        'selector': "//span[contains(text(), 'Mark')]/following-sibling::span"
    },
    'prjx': {
        'url': "https://www.prjx.com/swap?fromToken=0xb88339CB7199b77E23DB6E890353E22632Ba630f&fromChain=999&toToken=0x0000000000000000000000000000000000000000&toChain=999",
        'selector': "//p[contains(text(), 'HYPE')]/following-sibling::p"
    },
    'lighter': {
        'url': "https://app.lighter.xyz/trade/HYPE/",
        'selector': None  # Uses title
    },
    'geckoterminal': {
        'url': "https://www.geckoterminal.com/unichain/pools/0xc4f393785b36430779a93eedd52dd20857a46142bbe48c88d4c655303a53279c",
        'selector': "//span[@id='pool-price-display']/span"
    }
}
