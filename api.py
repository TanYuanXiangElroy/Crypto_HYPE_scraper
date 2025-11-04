# api.py (The Server)
from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    """Creates a connection to the SQLite database."""
    conn = sqlite3.connect('prices.db')
    conn.row_factory = sqlite3.Row # This lets us access columns by name
    return conn

@app.route('/data', methods=['GET'])
def get_all_data():
    """API endpoint to fetch all stored price data."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT timestamp, dex_name, token_pair, price FROM hype_prices ORDER BY timestamp DESC')
    rows = cursor.fetchall()
    conn.close()

    # Convert the database rows to a list of dictionaries
    data = [dict(row) for row in rows]
    
    return jsonify(data)

@app.route('/', methods=['GET'])
def index():
    return "Welcome to the HYPE Price API! Try accessing the /data endpoint."

if __name__ == "__main__":
    # This is for local testing only. For production, we use Gunicorn.
    app.run(debug=True, port=5000)