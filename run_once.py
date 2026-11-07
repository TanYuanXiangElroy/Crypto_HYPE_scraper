import logging
from jobs import run_scraper_job
import export_json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    logging.info("Starting one-off scrape job...")
    run_scraper_job()
    logging.info("Scrape job finished. Exporting data to JSON...")
    export_json.main()
    logging.info("Run once complete.")
