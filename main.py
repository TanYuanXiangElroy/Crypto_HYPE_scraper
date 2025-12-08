# main.py (The Worker Entry Point)
import logging
from jobs import run_scraper_job

# Main execution block
if __name__ == "__main__":
    # Ensure logging is configured when running this file directly
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("cron.log"), # Log to a file
            logging.StreamHandler()          # And to the console
        ]
    )
    run_scraper_job()