# database_setup.py (Upgraded Version)
import sqlite3

conn = sqlite3.connect('prices.db')
cursor = conn.cursor()

# We are adding new columns for the spot price, fee, and effective buy/sell prices
cursor.execute('''
CREATE TABLE IF NOT EXISTS hype_prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME NOT NULL,
    dex_name TEXT NOT NULL,
    token_pair TEXT NOT NULL,
    spot_price REAL NOT NULL,
    fee_percentage REAL,
    buy_price REAL,
    sell_price REAL
)
''')

print("table created successfully.")

conn.commit()
conn.close()