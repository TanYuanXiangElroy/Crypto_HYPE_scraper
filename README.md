# Crypto HYPE Price Scraper & API

This project is a Python-based application designed to scrape token prices from various decentralized exchanges (DEXs). It features a robust, modular architecture that allows for easy extension and management. The collected data is stored in a local SQLite database and served via a Flask API.

This refactored version moves beyond simple scripts to a more structured application, separating concerns like database interaction, configuration, and scheduling into their own modules.

## Core Architecture

The project is designed with a clear separation of concerns, making it easier to maintain and extend.

-   `api.py`: The main entry point for the application. It runs a **Flask web server** that serves the collected data and provides endpoints for interacting with the application. It also initializes and starts the automated scraping scheduler.
-   `scheduler.py`: Contains the scheduling logic using `APScheduler`. It periodically runs the main scraping job defined in `main.py`.
-   `main.py`: The "worker" script. It contains the core logic for a single scraping run. It fetches the list of pools from the database, calls the appropriate scraper for each, and stores the results.
-   `database.py`: A centralized module for all **database interactions**. No other file writes SQL. This module handles getting a database connection, fetching pools to monitor, and storing price data.
-   `config.py`: A simple configuration file that defines global constants like the database file path, preventing the use of "magic strings" in other files.
-   `scraper/`: This directory contains all the individual scraper modules.
    -   `__init__.py`: Implements the **Strategy Pattern** via the `SCRAPER_DISPATCHER` dictionary. This dictionary maps a `scraper_function` name (from the database) to the actual Python scraper function to be executed.
    -   `geckoterminal_api.py`, `hyperliquid_native.py`, etc.: Individual modules, each responsible for scraping a specific type of source.
-   `seed_pools.py`: A utility script to populate the database with an initial list of pools to monitor.

## Features

-   **Modular Scraper Dispatcher:** Easily add new scrapers without changing the core loop. Just add a new function and register it in the `SCRAPER_DISPATCHER`.
-   **Centralized Database Logic:** All SQL and database connections are handled in one place (`database.py`).
-   **Automated & Manual Scraping:** A built-in scheduler (`APScheduler`) runs scraping jobs automatically, but you can also trigger a run manually.
-   **Dynamic Pool Management:** Add new pools to be scraped via a simple API endpoint, without touching the code.
-   **Data API:** A Flask API to serve all collected data and manage the scraper.

## Local Setup Guide

### Prerequisites

-   Python 3.8+
-   `pip` (Python package installer)

### Installation Steps

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/TanYuanXiangElroy/Crypto_HYPE_scraper.git
    cd Crypto_HYPE_scraper
    ```

2.  **Create and Activate a Virtual Environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Seed the Database with Initial Pools:**
    The database file (`prices.db`) will be created automatically. Run the seed script to populate it with the initial list of pools to monitor.
    ```bash
    python seed_pools.py
    ```
    You can inspect or modify `seed_pools.py` to change which pools are monitored by default.

## Usage

The primary way to run the application is by starting the API server, which includes the automated scheduler.

1.  **Run the API Server & Scheduler:**
    ```bash
    python api.py
    ```
    The server will start on `http://127.0.0.1:5000`, and the scheduler will automatically begin running the scraping job every minute. The logs for the API and scheduler are saved to `api_server.log`.

2.  **Run a Scraper Job Manually (Optional):**
    If you want to perform a single, one-off scraping run without starting the server, you can run `main.py` directly. The output is logged to `cron.log`.
    ```bash
    python main.py
    ```

3.  **View the Data:**
    -   **Terminal Dashboard:** Run `python dashboard.py` (requires the API server to be running).
    -   **Web Dashboard:** The React frontend is in the `scraper_front_end` directory. See its README for instructions.
    -   **Directly via API:** Use a browser or `curl` to access the API endpoints.

## API Endpoints

-   `GET /`: Welcome message.
-   `GET /data`: Fetches all stored price data.
    -   Query Params: `limit` (int), `dex_name` (str).
    -   Example: `http://localhost:5000/data?limit=10&dex_name=hyperliquid_native`
-   `GET /latest_data`: Fetches the single most recent price data entry.
-   `POST /run_scraper`: Manually triggers a new scraping job.
-   `POST /add_scrap_pool`: Adds a new pool to the monitoring database.
    -   **Method:** `POST`
    -   **Body:** Raw JSON payload.
    -   **Success:** `201 Created`
    -   **Error:** `400 Bad Request`, `409 Conflict` (if pool exists).
    -   **Example Payload:**
        ```json
        {
            "dex_name": "Thruster",
            "scraper_function": "geckoterminal",
            "network": "blast_mainnet",
            "pool_address": "0x1265b4354a35159a6866b8e2B491c9534f595a85",
            "target_token_address": "0x4300000000000000000000000000000000000004"
        }
        ```

## How to Extend the Scraper

### Adding a New Pool to Scrape

To add a new pool, you don't need to edit any code. Simply send a `POST` request to the `/add_scrap_pool` endpoint with the correct JSON payload (see above). The application will perform a "dry run" to validate the pool before adding it to the database.

### Adding a New Scraper Function

If you need to scrape from a new source (e.g., a new DEX with a unique API), follow these two steps:

1.  **Create the Scraper Module:**
    -   Create a new `.py` file inside the `scraper/` directory (e.g., `mynewdex_api.py`).
    -   In this file, create a function named `scrape` that accepts `network`, `pool_address`, and `target_token_address` as arguments.
    -   This function should contain the logic to fetch and process the data, returning a dictionary with the price information or `None` if it fails.

2.  **Register the Scraper in the Dispatcher:**
    -   Open `scraper/__init__.py`.
    -   Import your new `scrape` function.
    -   Add a new entry to the `SCRAPER_DISPATCHER` dictionary. The key is the string you will use in the database (e.g., `'mynewdex'`), and the value is the function object you just imported.

    ```python
    # scraper/__init__.py

    # ... other imports
    from .mynewdex_api import scrape as scrape_mynewdex

    SCRAPER_DISPATCHER = {
        'geckoterminal': scrape_gecko_terminal_pool,
        'hyperliquid_native': scrape_hyperliquid_native,
        'mynewdex': scrape_mynewdex, # Add your new scraper here
    }
    ```
Once registered, you can add pools that use `"scraper_function": "mynewdex"` via the API.
