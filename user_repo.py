import sqlite3
from database import init_db, get_conn


def create_user(username, age, city, hobby):
    init_db()
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users (username, age, city, hobby) VALUES (?, ?, ?, ?);",
            (username, age, city, hobby)
        )
        conn.commit()
        print("User created successfully!")
    except sqlite3.IntegrityError:
        print("Username already exists.")
    finally:
        conn.close()

def get_user(username):   
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM users WHERE username = ?;",
        (username,)
    )
    user = cur.fetchone()
    conn.close()
    return user

def update_user(username, age, city, hobby):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "UPDATE users SET age = ?, city = ?, hobby = ? WHERE username = ?;",
        (age, city, hobby, username)
    )
    conn.commit()
    conn.close()
    print("User updated successfully!")

def delete_user(username):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM users WHERE username = ?;",
        (username,)
    )
    conn.commit()
    conn.close()
    print("User deleted successfully!")
             


