# Crypto HYPE Price Scraper & API

A robust, production-ready data pipeline designed to scrape, store, and serve real-time token prices from various decentralized exchanges (DEXs). Built with a modular architecture, it features automated scheduling, a RESTful API. This repository hosts the **backend service**.

## Key Features

*   **Modular Architecture:** Scraper logic is decoupled from the application core using a Strategy Pattern, allowing for easy extension.
*   **Automated Scheduling:** Integrated `APScheduler` runs background jobs to keep price data fresh.
*   **RESTful API:** A Flask-based API serves data and allows for dynamic management of monitored pools.
*   **Robust Error Handling:** Custom exception handling and structured logging ensure reliability.
*   **Database Management:** Efficient SQLite integration with context-managed connections.
*   **Containerized:** Fully Dockerized for consistent deployment across environments.
*   **Tested:** Includes a `pytest` suite for ensuring scraper reliability.

---

## Quick Start (Docker)

To run **just the backend service** using Docker:

1.  **Clone this Repository:**
    ```bash
    git clone https://github.com/TanYuanXiangElroy/Crypto_HYPE_scraper.git
    cd Crypto_HYPE_scraper
    ```

2.  **Run with Docker Compose:**
    ```bash
    docker compose up --build
    ```

    *   The backend API will be available at `http://localhost:5000`.

    *(Note: To run the frontend, please refer to the `Crypto_HYPE_scraper_frontend` repository's README for its Docker setup instructions.)*

---

## Running the Full Stack (Backend + Frontend)

We have a dedicated frontend dashboard to visualize this data!

**Frontend Repository:** [Crypto_HYPE_scraper_frontend](https://github.com/TanYuanXiangElroy/Crypto_HYPE_scraper_frontend)

To run both services together using Docker Compose, create a `compose.yaml` file in a parent directory containing both cloned repositories:

```yaml
services:
  backend:
    build:
      context: ./Crypto_HYPE_scraper
      dockerfile: Dockerfile
    container_name: crypto_hype_scraper_backend
    ports:
      - "5000:5000"
    restart: unless-stopped

  frontend:
    build:
      context: ./Crypto_HYPE_scraper_frontend # Make sure this matches your frontend folder name
      dockerfile: Dockerfile
    container_name: crypto_hype_scraper_frontend
    ports:
      - "5173:80"
    restart: unless-stopped
    depends_on:
      - backend
```

Then run:
```bash
docker compose up --build
```

---

## Development Setup

If you prefer to run the backend locally for development:

### 1. Prerequisites
*   Python 3.12+
*   `pip`

### 2. Installation
```bash
# Navigate to the backend directory
cd Crypto_HYPE_scraper

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Database Setup
Initialize the SQLite database with default pools:
```bash
python seed_pools.py
```

### 4. Running the Application
Start the API server and the background scheduler:
```bash
python api.py
```

### 5. Running Tests
Execute the test suite to verify everything is working:
```bash
pytest tests/
```

---

## Architecture Overview

The project follows a clean separation of concerns:

| Module | Description |
| :--- | :--- |
| **`api.py`** | Entry point. Runs the Flask server and initializes the scheduler. |
| **`jobs.py`** | The worker logic. Orchestrates the scraping process independent of the trigger source. |
| **`database.py`** | Centralized database layer. Handles all SQL interactions safely. |
| **`scraper/`** | Contains individual scraper modules (`geckoterminal_api.py`, etc.). |
| **`config.py`** | Centralized configuration for ports, URLs, and paths. |

---

## API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/data` | Fetch all stored price data. Supports `limit` and `dex_name` filters. |
| `GET` | `/latest_data` | Get the single most recent price entry. |
| `POST` | `/run_scraper` | Manually trigger a background scraping job. |
| `POST` | `/add_scrap_pool` | Add a new pool to monitor. Validates the pool via a "dry run" first. |

---

## Contributing

### Adding a New Scraper
1.  Create a new file in `scraper/` (e.g., `mynewdex.py`).
2.  Implement a `scrape(**kwargs)` function.
3.  Register it in `scraper/__init__.py`.

```python
# scraper/__init__.py
from .mynewdex import scrape as scrape_mynewdex

SCRAPER_DISPATCHER = {
    # ... existing scrapers
    'mynewdex': scrape_mynewdex,
}
```