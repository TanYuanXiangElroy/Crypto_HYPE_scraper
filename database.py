import sqlite3
import config
import logging
from datetime import datetime
import contextlib

@contextlib.contextmanager
def get_db_connection():
    """
    Provides a connection to the SQLite database using a context manager.
    Ensures the connection is properly closed after use.
    """
    conn = None
    try:
        conn = sqlite3.connect(config.DB_PATH)
        conn.row_factory = sqlite3.Row  # This lets us access columns by name
        yield conn
    except sqlite3.Error as e:
        logging.error(f"Database connection error: {e}")
        raise # Re-raise the exception after logging
    finally:
        if conn:
            conn.close()

def store_price_data(dex_name, token_pair, data):
    """Inserts a new price record into the SQLite database."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            timestamp = datetime.now()
            cursor.execute('''
                INSERT INTO hype_prices (timestamp, dex_name, token_pair, spot_price, fee_percentage, buy_price, sell_price)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                timestamp,
                dex_name,
                token_pair,
                data.get('spot_price'),
                data.get('fee_percentage'),
                data.get('buy_price'),
                data.get('sell_price')
            ))
            conn.commit()
            logging.info(f"-> Successfully stored: {dex_name} | {token_pair} | Spot Price=${data.get('spot_price'):.4f}")
    except sqlite3.Error as e:
        logging.error(f"-> Error storing data: {e}")

def getting_pools_to_scrape():
    """Fetches the list of pools to scrape from the monitored_pools table."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM monitored_pools")
            rows = cursor.fetchall()
            # Convert database rows to a list of dictionaries
            return [dict(row) for row in rows]
    except sqlite3.Error as e:
        logging.error(f"Error fetching pools config: {e}")
        return []

def get_latest_data_database():
    """Fetches the latest price data entry from the database."""
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
                return dict(row)
            return {}
    except sqlite3.Error as e:
        logging.error(f"Database error in get_latest_data_database: {e}")
        return None

def get_all_data_of_DEX(limit=None, dex_name=None):
    """Fetches all stored price data, with optional filtering by DEX name and limit."""
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
            return [dict(row) for row in rows]
    except sqlite3.Error as e:
        logging.error(f"Database error in get_all_data_of_DEX: {e}")
        return None

def is_pool_monitored(pool_address):
    """Checks if a pool is already being monitored."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM monitored_pools WHERE pool_address = ?", (pool_address,))
            return cursor.fetchone() is not None
    except sqlite3.Error as e:
        logging.error(f"Database error in is_pool_monitored: {e}")
        # If the check fails, returning True prevents accidental duplicates.
        return True

def add_pool(pool_data):
    """Adds a new pool to the monitored_pools table."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO monitored_pools (dex_name, scraper_function, network, pool_address, target_token_address)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                pool_data['dex_name'],
                pool_data['scraper_function'],
                pool_data['network'],
                pool_data['pool_address'],
                pool_data['target_token_address']
            ))
            conn.commit()
        logging.info(f"-> Successfully added pool: {pool_data['dex_name']} | {pool_data['pool_address']}")
    except sqlite3.Error as e:
        logging.error(f"-> Error adding pool: {e}")

def delete_all_pool():
    """Deletes all entries from the monitored_pools table. Used for resetting during testing."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM monitored_pools')
            conn.commit()
        logging.info("-> Successfully deleted all pools from monitored_pools.")
    except sqlite3.Error as e:
        logging.error(f"-> Error deleting pools: {e}")