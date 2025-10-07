import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        age INTEGER,
        city TEXT,
        gender TEXT,
        pref_gender TEXT,
        pref_city TEXT
    )
    """)

cur.execute
("""
    CREATE TABLE IF NOT EXISTS users(
        username TEXT PRIMARY KEY,
        age INTEGER,
        city TEXT
    )
""")


cur.execute
("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender TEXT,
        recipient TEXT,
        text TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        owner TEXT,
        about_user TEXT,
        text TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

conn.commit()
conn.close()
