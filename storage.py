import sqlite3
from pathlib import Path

class Database:
    def __init__(self, path):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(path)
        self.create_tables()

    def create_tables(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS coins (
            id TEXT PRIMARY KEY,
            name TEXT,
            symbol TEXT,
            price_usd REAL,
            volume_usd REAL,
            developer TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            source TEXT
        )
        """)
        self.conn.commit()

    def insert_coin(self, coin):
        self.conn.execute("""
        INSERT OR REPLACE INTO coins (id, name, symbol, price_usd, volume_usd, developer, source)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            coin["id"], 
            coin["name"], 
            coin["symbol"], 
            coin["price_usd"], 
            coin["volume_usd"], 
            coin["developer"], 
            coin["source"]
        ))
        self.conn.commit()

    def fetch_all(self):
        return self.conn.execute("SELECT * FROM coins").fetchall()
