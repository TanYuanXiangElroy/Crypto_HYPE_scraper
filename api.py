# api.py (The Server)
from flask import Flask, jsonify, request
import sqlite3
import logging
from scheduler import start_scheduler

import config
from scraper import SCRAPER_DISPATCHER
from jobs import run_scraper_job
from flask_cors import CORS
from database import get_latest_data_database, get_all_data_of_DEX, is_pool_monitored, add_pool

app = Flask(__name__)
CORS(app)



# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("api_server.log"),
        logging.StreamHandler()
    ]
)
logging.getLogger('apscheduler').setLevel(logging.WARNING) # Make scheduler less noisy

@app.route('/latest_data', methods=['GET'])
def get_latest_data():
    """API endpoint to fetch the latest price data entry."""
    data = get_latest_data_database()
    if data is None:
        return jsonify({"error": "A database error occurred"}), 500
    return jsonify(data)

@app.route('/data', methods=['GET'])
def get_all_data():
    """API endpoint to fetch all stored price data."""
    limit = request.args.get('limit', type=int)
    dex_name = request.args.get('dex_name', type=str)
    
    data = get_all_data_of_DEX(limit=limit, dex_name=dex_name)
    if data is None:
        return jsonify({"error": "A database error occurred"}), 500
    return jsonify(data)

@app.route('/', methods=['GET'])
def index():
    return "Welcome to the HYPE Price API! Try accessing the /data endpoint."

@app.route('/run_scraper', methods=['POST'])
def run_scraper_endpoint():
    """API endpoint to manually trigger the scraper job."""
    try:
        run_scraper_job()
        return jsonify({"status": "Scraper job executed successfully."})
    except Exception as e:
        app.logger.error(f"Error running scraper job: {e}")
        return jsonify({"error": "Failed to run scraper job."}), 500

@app.route('/add_scrap_pool', methods=['POST'])
def add_scrape_pool():
    """
    API endpoint to add a new pool.
    1. Checks for duplicates.
    2. Validates the pool by attempting a real scrape.
    3. Saves to DB only if valid.
    """
    data = request.json
    required_fields = ['dex_name', 'scraper_function', 'network', 'pool_address', 'target_token_address']
    
    # 1. Basic Validation
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields."}), 400
    
    # 2. Duplicate Check
    if is_pool_monitored(data['pool_address']):
        return jsonify({"error": "This pool is already being monitored."}), 409 # 409 Conflict

    # 3. The "Dry Run" (Validation via API)
    logging.info(f"Validating new pool: {data['pool_address']}...")
    
    scraper_name = data['scraper_function']
    scraper_to_run = SCRAPER_DISPATCHER.get(scraper_name)

    if not scraper_to_run:
        return jsonify({"error": f"Validation failed. Unknown scraper function: '{scraper_name}'"}), 400

    try:
        # Note: Some scrapers might not need all arguments, but passing them shouldn't hurt
        # as long as the scraper functions can handle extra **kwargs.
        # For now, this assumes they have similar signatures or are robust enough.
        test_result = scraper_to_run(
            network=data['network'],
            pool_address=data['pool_address'],
            target_token_address=data['target_token_address']
        )
    except Exception as e:
        logging.error(f"Dry run for {scraper_name} failed with an exception: {e}")
        return jsonify({
            "error": "Validation failed during scrape attempt.",
            "details": str(e)
        }), 400

    if not test_result:
        return jsonify({
            "error": "Validation failed. Could not scrape this pool.",
            "details": "The scraper ran but returned no data. Check the network, pool address, and target token address."
        }), 400

    # 4. Insert into Database
    add_pool(data)
    
    return jsonify({
        "status": "Pool added successfully.",
        "initial_data": test_result
    }), 201



if __name__ == "__main__":
    start_scheduler()
    app.run(debug=True, port=config.API_PORT, use_reloader=False)
    