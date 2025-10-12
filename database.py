DB_PATH = "app.db"


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn




def init_db() -> None:
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    created_at TEXT NOT NULL
    );
    """
    )

    cur.execute(
    """
    CREATE TABLE IF NOT EXISTS profiles (
    username TEXT PRIMARY KEY REFERENCES users(username) ON DELETE CASCADE,
    details_json TEXT NOT NULL,
    preferences_json TEXT NOT NULL,
    updated_at TEXT NOT NULL
    );
    """
    )

    cur.execute(
    """
    CREATE TABLE IF NOT EXISTS messages (
    id TEXT PRIMARY KEY,
    from_user TEXT NOT NULL REFERENCES users(username),
    to_user TEXT NOT NULL REFERENCES users(username),
    content TEXT NOT NULL,
    sent_at TEXT NOT NULL,
    read_at TEXT
    );
    """
    )

    cur.execute("CREATE INDEX IF NOT EXISTS idx_messages_inbox ON messages(to_user, sent_at DESC);")

    cur.execute(
    "CREATE INDEX IF NOT EXISTS idx_messages_convo ON messages(from_user, to_user, sent_at DESC);"
    )
    
    cur.execute(
    """
    CREATE TABLE IF NOT EXISTS notes (
    id TEXT PRIMARY KEY,
    author TEXT NOT NULL REFERENCES users(username),
    target TEXT NOT NULL REFERENCES users(username),
    content TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
    );
    """
    )
    cur.execute(
    """
    CREATE TABLE IF NOT EXISTS session_state (
    id INTEGER PRIMARY KEY CHECK (id=1),
    current_user TEXT REFERENCES users(username)
    );
    """
    )
    # ensure exactly one row exists
    cur.execute("INSERT OR IGNORE INTO session_state (id, current_user) VALUES (1, NULL);")
    conn.commit()
    conn.close()