# Web Scraper for HYPE Token Price

This project is a Python-based application designed to scrape the price of the HYPE token from various decentralized exchanges (DEXs). The collected data is stored in a local SQLite database and can be served via a simple Flask API.

This project serves as a practical environment to learn and experiment with web scraping techniques, project structure, and basic API development.

## Features

- **Modular Scraper Design:** Each DEX has its own dedicated scraper module, making it easy to add, remove, or debug individual scrapers.
- **Persistent Storage:** Scraped data is saved to a local SQLite database, including a timestamp, the DEX name, and the price.
- **Data API:** A simple Flask API is included to serve all collected data in a clean JSON format.
- **Robust Scraping:** Utilizes the Selenium library to handle dynamic, JavaScript-heavy websites, including pop-up handling.

## Project Structure

-   `main.py`: The main entry point for running a one-time scraping job of all configured DEXs.
-   `api.py`: A Flask web server that provides a `/data` endpoint to view the contents of the database.
-   `database_setup.py`: A one-time script to create and initialize the SQLite database.
-   `scrapers/`: This directory contains the individual scraper modules.
    -   `__init__.py`: Makes the directory a Python package and exports the scraper functions.
    -   `hyperliquid.py`: Scraper for Hyperliquid.
    -   `lighter.py`: Scraper for Lighter.
    -   `prjx.py`: Scraper for PRJX.
    -   *...and so on for each new DEX.*
-   `requirements.txt`: A list of all required Python packages for the project.
-   `.gitignore`: Specifies files and directories to be ignored by Git (e.g., the database, virtual environment).

## Local Setup Guide

Follow these steps to set up and run the project on a local machine (tested on WSL Ubuntu).

### Prerequisites

-   Python 3.8+
-   `pip` (Python package installer)
-   `git`
-   Google Chrome browser

### Installation Steps

1.  **Clone the Repository:**
    Open your terminal and clone the project from GitHub.
    ```bash
    git clone https://github.com/TanYuanXiangElroy/Crypto_HYPE_scraper.git
    cd Crypto_HYPE_scraper
    ```

2.  **Create a Virtual Environment:**
    It's a best practice to isolate project dependencies.
    ```bash
    # Create the virtual environment folder named 'venv'
    python3 -m venv venv
    # Activate the environment
    source venv/bin/activate
    ```
    *(Your terminal prompt should now be prefixed with `(venv)`)*

3.  **Install Dependencies:**

    Now, install all the packages from this file:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Install Google Chrome & ChromeDriver (for Selenium):**
    Selenium requires two components: the Google Chrome browser and a matching ChromeDriver.
    For local development, the modern Selenium library can handle this for you. You only need to install the browser.
    code
    ```Bash
    # Download and install the latest stable version of Chrome
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
    sudo dpkg -i google-chrome-stable_current_amd64.deb
    sudo apt-get install -f # Fixes any missing dependencies
    ```
    When you run your Python script, Selenium Manager will automatically download the correct ChromeDriver the first time it's needed.

    This method is highly recommended for servers and production environments as it gives you full control and works in firewalled environments.

    Step A: Install Google Chrome
    
    ```Bash
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
    sudo dpkg -i google-chrome-stable_current_amd64.deb
    sudo apt-get install -f
    ```

    Step B: Find Your Chrome Version
    
    ```Bash
    google-chrome --version
    # Example output: "Google Chrome 124.0.6367.118"
    ```
    Step C: Download the Matching ChromeDriver

    - Go to the Chrome for Testing availability dashboard: https://googlechromelabs.github.io/chrome-for-testing/
    - Find the "Stable" version that matches your installed browser.
    - Under that version, find the chromedriver row and the linux64 column.
    - Right-click on the URL and "Copy Link Address"
    
    Step D: Install ChromeDriver
    ```Bash
    # Paste the URL you copied in the quotes below
    wget -O chromedriver.zip "YOUR_PASTED_CHROMEDRIVER_URL_HERE"

    # Unzip and move the driver to a system-wide location
    unzip chromedriver.zip
    sudo mv chromedriver-linux64/chromedriver /usr/local/bin/
    ```

5.  **Initialize the Database:**
    Run the setup script once to create the `prices.db` file and the necessary table.
    ```bash
    python database_setup.py
    ```

### Usage

You can now run the scraper and the API.

1.  **Run the Scraper Manually:**
    To execute a single run of all scrapers, which will collect the latest prices and save them to the database:
    ```bash
    python main.py
    ```

2.  **Run the API Server:**
    To view the data you have collected, start the Flask API server.
    ```bash
    python api.py
    ```
    The server will start on `http://127.0.0.1:5000`. You can now access the data:
    -   **In a browser:** Navigate to `http://localhost:5000/data`
    -   **In a new terminal:** Use `curl http://127.0.0.1:5000/data`

## How to Add a New Scraper

This project is designed to be easily extensible. Follow these steps to add a scraper for a new DEX.

1.  **Create a New Scraper File:**
    -   Create a new file in the `scrapers/` directory (e.g., `scrapers/new_dex.py`).

2.  **Write the `scrape()` Function:**
    -   Inside your new file, create a function named exactly `scrape()`.
    -   This function should contain all the Selenium logic to navigate to the site, handle pop-ups, and extract the price.
    -   It should return a dictionary on success (e.g., `{'main_price': 42.0}`) or `None` on failure.

3.  **Register the New Scraper:**
    -   Open the `scrapers/__init__.py` file.
    -   Add a new line to import and rename your new function:
        ```python
        from .new_dex import scrape as scrape_new_dex
        ```

4.  **Integrate into `main.py`:**
    -   Open `main.py`.
    -   Add `scrape_new_dex` to the import list at the top.
    -   Add a new block inside the `main()` function to call your scraper and store its data.