# file: database.py
# purpose: Database initialization and connection management
# author: Boon
# date: 2025-09-29

import sqlite3

# Global constant defining the database file path.
DB_PATH = "app.db"


def get_conn() -> sqlite3.Connection:
    """
    Establish and return a connection to the SQLite database.

    This function ensures all connections have dictionary-like row access
    and enforce foreign key constraints, maintaining referential integrity
    between related tables.

    Args: None

    Returns:
    sqlite3.Connection: A configured connection object to the database.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row # Enables accessing query results by column name
    conn.execute("PRAGMA foreign_keys = ON;") # Ensures foreign key constraints are active
    return conn

def init_db() -> None:
    """
    Initialize the database schema by creating required tables if they do not exist.

    This function creates three main tables:
        - users: stores user profiles and personal details.
        - messages: stores messages sent between users.
        - notes: stores personal notes a user writes about another user.

    It ensures the tables are created with proper foreign key relationships,
    enforcing automatic deletion of related records when a user is removed.

    Args: None

    Returns: None
    """
    conn = get_conn()
    cur = conn.cursor()

    # Create table for storing user profiles
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            age INTEGER,
            city TEXT,
            hobby TEXT,
            gender TEXT,
            language TEXT
        );
    """)

    # Create table for storing user messages with sender and receiver
    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL references users(username) ON DELETE CASCADE,
            receiver TEXT NOT NULL,
            content TEXT NOT NULL,
            read INTEGER DEFAULT 0,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );     
    """)

    # Create table for storing personal notes written by users about others
    cur.execute("""
        CREATE TABLE IF NOT EXISTS notes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL references users(username) ON DELETE CASCADE,
            about_user TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conn.commit()
    conn.close()
