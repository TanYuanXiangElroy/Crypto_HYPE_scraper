# api.py (The Server)
from flask import Flask, jsonify, request
import sqlite3
import os
import logging

from apscheduler.schedulers.background import BackgroundScheduler
import atexit

from scraper import scrape_gecko_terminal_pool

# Import the scraper logic from  main.py file
from main import main as run_scraper_job 

from flask_cors import CORS 


app = Flask(__name__)


CORS(app) 

# --- Logging Setup ---
# craper output in the API terminal
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("api_server.log"), # Saves logs to this file
        logging.StreamHandler()                # Prints logs to your terminal
    ]
)
# Explicitly tell the Scheduler to be noisy so we can see it working
logging.getLogger('apscheduler').setLevel(logging.DEBUG)
# --- Database Setup ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, 'prices.db')

def get_db_connection():
    """Creates a connection to the SQLite database."""
    conn = sqlite3.connect('prices.db')
    conn.row_factory = sqlite3.Row # This lets us access columns by name
    return conn

@app.route('/lastest_data', methods=['GET'])
def get_latest_data():
    """API endpoint to fetch the latest price data entry."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT timestamp, dex_name, token_pair, buy_price, sell_price
                FROM hype_prices
                ORDER BY timestamp DESC
                LIMIT 1
            ''')
            row = cursor.fetchone()
            if row:
                data = dict(row)
            else:
                data = {}
    except sqlite3.Error as e:
        # Log the error and return an appropriate error response
        app.logger.error(f"Database error: {e}")
        return jsonify({"error": "A database error occurred"}), 500
    
    return jsonify(data)

@app.route('/data', methods=['GET'])
def get_all_data():
    """API endpoint to fetch all stored price data."""

    limit = request.args.get('limit', type=int)
    dex_name = request.args.get('dex_name', type=str)
    # Start with a base query
    query = 'SELECT timestamp, dex_name, token_pair, spot_price,fee_percentage,buy_price,sell_price FROM hype_prices'
    params = []

    if dex_name:
        query += ' WHERE dex_name = ?'
        params.append(dex_name)

    query += ' ORDER BY timestamp DESC'

    if limit:
        query += ' LIMIT ?'
        params.append(limit)


    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            # Convert the database rows to a list of dictionaries
            data = [dict(row) for row in rows]
    except sqlite3.Error as e:
        # Log the error and return an appropriate error response
        app.logger.error(f"Database error: {e}")
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
scheduler = BackgroundScheduler()

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
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if this pool address already exists in the database
        cursor.execute("SELECT id FROM monitored_pools WHERE pool_address = ?", (data['pool_address'],))
        if cursor.fetchone():
            conn.close()
            return jsonify({"error": "This pool is already being monitored."}), 409 # 409 Conflict
            
    except sqlite3.Error as e:
        return jsonify({"error": "Database check failed"}), 500

    # 3. The "Dry Run" (Validation via API)
    # We actually try to scrape it ONCE right now. 
    # If the scraper returns None, the data is bad (wrong network, wrong address, or token not found).
    print(f"Validating new pool: {data['pool_address']}...")
    
    test_result = None
    if data['scraper_function'] == 'geckoterminal':
        test_result = scrape_gecko_terminal_pool(
            network=data['network'],
            pool_address=data['pool_address'],
            target_token_address=data['target_token_address']
        )
    
    if not test_result:
        conn.close()
        return jsonify({
            "error": "Validation failed. Could not scrape this pool.",
            "details": "Check the network, pool address, and target token address."
        }), 400

    # 4. Insert into Database (Only if steps 1, 2, and 3 passed)
    try:
        cursor.execute('''
            INSERT INTO monitored_pools (dex_name, scraper_function, network, pool_address, target_token_address)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            data['dex_name'],
            data['scraper_function'],
            data['network'],
            data['pool_address'],
            data['target_token_address']
        ))
        conn.commit()
        conn.close()
        
        # Optional: Return the data we just scraped as proof it works
        return jsonify({
            "status": "Pool added successfully.",
            "initial_data": test_result
        }), 201
        
    except sqlite3.Error as e:
        app.logger.error(f"Database error: {e}")
        return jsonify({"error": "A database error occurred during insertion"}), 500


def start_scheduler():          
    """Starts the background scheduler to run scraping jobs periodically."""

    if not scheduler.running:
        # Add the job. 
        scheduler.add_job(func=run_scraper_job, trigger="interval", minutes=1, max_instances=1)
        
        scheduler.start()
        print("--- Internal Scraper Scheduler Started ---")
        
        atexit.register(lambda: scheduler.shutdown())    
    

if __name__ == "__main__":
    # This is for local testing only. For production, we use Gunicorn.

    start_scheduler()
    app.run(debug=True, port=5000, use_reloader=False)