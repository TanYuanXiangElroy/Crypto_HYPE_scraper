# HYPE Token Price Scraper & API

This project is a Python-based application designed to scrape the price of the HYPE token from various decentralized exchanges (DEXs) using the GeckoTerminal API. The collected data is stored in a local SQLite database and can be served via a simple Flask API.

This project serves as a practical environment to learn and experiment with API integration, project structure, and basic API development.

## Project Evolution: From Selenium to API

This project originally started as a web scraper using the **Selenium** library to extract data directly from DEX websites.

**Why the change?**
- **Instability of Web Scraping:** Scraping websites is often brittle. A small change in a website's HTML structure could break the scraper, requiring constant maintenance.
- **Efficiency:** Directly calling an API is significantly faster and more reliable than loading a full webpage in a browser.

The new version of this project now uses the **GeckoTerminal API**, which provides a clean and stable way to get token and pool data. The original Selenium-based code has been moved to the `scraper/archive/selenium` directory for learning and comparison purposes.

## Features

- **Modular Scraper Design:** The main scraping logic is built around a reusable function that can query any pool on GeckoTerminal, making it easy to add new pools.
- **Persistent Storage:** Scraped data is saved to a local SQLite database, including a timestamp, the DEX name, and the price.
- **Data API:** A simple Flask API is included to serve all collected data in a clean JSON format.
- **Reliable API Integration:** Uses the `requests` library to fetch data directly from the GeckoTerminal API.

## Project Structure

-   `main.py`: The main entry point for running a one-time scraping job of all configured DEXs.
-   `api.py`: A Flask web server that provides a `/data` endpoint to view the contents of the database.
-   `database_setup.py`: A one-time script to create and initialize the SQLite database.
-   `scraper/`: This directory contains the individual scraper modules.
    -   `__init__.py`: Makes the directory a Python package and exports the scraper functions.
    -   `coingecko_api.py`: Contains the modular function for scraping GeckoTerminal pools.
    -   `archive/`: Contains archived code from previous project versions (e.g., the old Selenium scrapers).
-   `requirements.txt`: A list of all required Python packages for the project.
-   `.gitignore`: Specifies files and directories to be ignored by Git (e.g., the database, virtual environment).

## Local Setup Guide

Follow these steps to set up and run the project on a local machine (tested on WSL Ubuntu).

### Prerequisites

-   Python 3.8+
-   `pip` (Python package installer)
-   `git`

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

4.  **Initialize the Database:**
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

## How to Add a New Pool to Scrape

This project is designed to be easily extensible. Follow these steps to add a new DEX pool to the scraping list.

1.  **Find the Pool Information:**
    -   Go to [GeckoTerminal](https://geckoterminal.com).
    -   Find the token and network you are interested in.
    -   You will need two pieces of information: the **network ID** (e.g., `hyperevm`) and the **pool address**.

2.  **Add to the List in `main.py`:**
    -   Open the `main.py` file.
    -   Locate the `pools_to_scrape` list.
    -   Add a new dictionary to the list with the information you found:
        ```python
        pools_to_scrape = [
            # ... existing pools
            {
                "dex_name": "NameOfYourDEX", 
                "network": "network_id_here", 
                "pool_address": "pool_address_here"
            }
        ]
        ```

That's it! The main loop will automatically pick up the new entry and start scraping it.

## Automation with Cron (Linux/WSL)

To run the scraper automatically at a regular interval, you can set up a cron job. The following steps will configure the scraper to run every 5 minutes and save its output to a log file for easy debugging.

### Steps to Set Up the Cron Job

1.  **Open the Crontab Editor:**
    Open your terminal and type the following command to edit the cron configuration file for your user.
    ```bash
    crontab -e
    ```
    *(If it's your first time, you may be asked to choose a text editor. Select `nano` if you are unsure, as it is the easiest to use.)*

2.  **Add the Job Definition:**
    Go to the bottom of the file and add the following line.

    **Important:** You must replace `/path/to/your/project` with the **absolute path** to your project directory. You can find this path by navigating to your project folder in the terminal and running the `pwd` command.

    ```crontab
    # Run the HYPE price scraper every 5 minutes and log output
    */5 * * * * /path/to/your/project/venv/bin/python /path/to/your/project/main.py >> /path/to/your/project/cron.log 2>&1
    ```

    **Example:** If your project is located at `/home/USERNAME/Crypto_HYPE_scraper`, the line would be:
    ```crontab
    */5 * * * * /home/USERNAME/Crypto_HYPE_scraper/venv/bin/python /home/USERNAME/Crypto_HYPE_scraper/main.py >> /home/USERNAME/Crypto_HYPE_scraper/cron.log 2>&1
    ```

3.  **Save and Exit:**
    -   If using `nano`, press `Ctrl+X`, then `Y`, and finally `Enter` to save the file.
    -   You should see a confirmation message like `crontab: installing new crontab`.

### Understanding the Cron Job Command

Each part of the command has a specific purpose:

-   `*/5 * * * *`: **The Schedule.** This is the "cron expression" that means "run at every 5th minute of every hour, of every day."
-   `/path/to/your/project/venv/bin/python`: **The Python Interpreter.** This is the absolute path to the Python executable *inside your virtual environment*. This is crucial to ensure the script runs with all the correct installed packages.
-   `/path/to/your/project/main.py`: **The Script to Run.** This is the absolute path to your main scraper script.
-   `>> /path/to/your/project/cron.log`: **Redirecting Output.** The `>>` operator appends any printed output from your script to a file named `cron.log`. This allows you to see what the scraper is doing.
-   `2>&1`: **Redirecting Errors.** This is a standard shell command that means "redirect the standard error stream (`2`) to the same place as the standard output stream (`1`)". In short, it ensures that both normal output and any error messages are saved to your `cron.log` file, making debugging much easier.

### Managing the Cron Job

-   **To view your active cron jobs:**
    ```bash
    crontab -l
    ```
-   **To remove all of your cron jobs:**
    ```bash
    crontab -r
    ```
-   **To monitor the scraper's output in real-time:**
    ```bash
    tail -f /path/to/your/project/cron.log
    ```