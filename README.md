# Web Scraper HYPE

This project is a learning exercise in web scraping, designed to extract data from various websites.

## Project Structure

- `main.py`: The main entry point for running the web scraping operations.
- `api.py`: Contains API-related functionalities, likely for exposing scraped data.
- `database_setup.py`: Handles the setup and initialization of the project's database.
- `prices.db`: The SQLite database file where scraped data is stored.
- `scraper/`: This directory contains individual scraper modules for different websites.
    - `based_one.py`: Scraper for 'Based One' platform.
    - `geckoterminal.py`: Scraper for 'GeckoTerminal'.
    - `hyperliquid.py`: Scraper for 'Hyperliquid'.
    - `lighter.py`: Scraper for 'Lighter' platform.
    - `prjx.py`: Scraper for 'PRJX' platform.

## Getting Started

### Prerequisites

- Python 3.x
- `pip` (Python package installer)

### Installation

1.  **Clone the repository (if applicable):**
    ```bash
    git clone <repository-url>
    cd webscraper_HYPE
    ```

2.  *

    pip install -r requirements.txt # You might need to create this file first
    ```
    *(Note: If `requirements.txt` does not exist, you will need to create it by running `pip freeze > requirements.txt` after installing your dependencies.)*

### Running the Scraper

To run the main scraper, execute:

```bash
python main.py
```

## Learning Web Scraping

This project serves as a practical environment to learn and experiment with web scraping techniques using Python. Each scraper module in the `scraper/` directory demonstrates how to interact with different websites and extract specific information.
