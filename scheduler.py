
# scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
import logging
from jobs import run_scraper_job
import atexit


# --- Scheduler Setup ---
scheduler = BackgroundScheduler()

def start_scheduler():
    """Starts the background scheduler to run scraping jobs periodically."""
    if not scheduler.running:
        scheduler.add_job(func=run_scraper_job, trigger="interval", minutes=1, max_instances=1)
        scheduler.start()
        print("--- Internal Scraper Scheduler Started ---")
        atexit.register(lambda: scheduler.shutdown())

