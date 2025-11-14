# api.py (The Server)
from flask import Flask, jsonify, request
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

if __name__ == "__main__":
    # This is for local testing only. For production, we use Gunicorn.
    app.run(debug=True, port=5000)