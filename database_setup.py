# database_setup.py
import sqlite3

# Connect to the database (this will create the file if it doesn't exist)
conn = sqlite3.connect('prices.db')
cursor = conn.cursor()

# Create the table to store price data
# Using "IF NOT EXISTS" prevents errors if you run this script multiple times
cursor.execute('''
CREATE TABLE IF NOT EXISTS hype_prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME NOT NULL,
    dex_name TEXT NOT NULL,
    token_pair TEXT NOT NULL,
    price REAL NOT NULL
)
''')

print("Database and table created successfully.")

# Commit the changes and close the connection
conn.commit()
conn.close()