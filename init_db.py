import sqlite3

# Run once to initiate the sql database
def init_db():
    conn = sqlite3.connect("dns_log.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS dns_queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            client_ip TEXT,
            domain TEXT
        )
    ''')
    conn.commit()
    conn.close()