import sqlite3
from database import init_db, get_conn

def create_user(username, age, city, hobby, gender, language):
    init_db()
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users (username, age, city, hobby, gender, language) VALUES (?, ?, ?, ?, ?, ?);",
            (username, age, city, hobby, gender, language)
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

def update_user(username, age, city, hobby, gender, language):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "UPDATE users SET age = ?, city = ?, hobby = ?, gender = ?, language = ? WHERE username = ?;",
        (age, city, hobby, gender, language, username)
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

def view_profile(username):
    user = get_user(username)
    if user:
        print(f"Username: {user['username']}")
        print(f"Age: {user['age']}")
        print(f"City: {user['city']}")
        print(f"Hobby: {user['hobby']}")
        print(f"Gender: {user['gender']}")
        print(f"Language: {user['language']}")
    else:
        print("User not found.")

def edit_profile(username):
    user = get_user(username)
    if not user:
        print("User not found.")
        return
    print("Leave a field blank to keep the current value.")
    age = input(f"Enter new age (current: {user['age']}): ").strip()
    city = input(f"Enter new city (current: {user['city']}): ").strip()
    hobby = input(f"Enter new hobby (current: {user['hobby']}): ").strip()
    gender = input(f"Enter new gender (current: {user['gender']}): ").strip()
    language = input(f"Enter new language (current: {user['language']}): ").strip()

    age = int(age) if age else user['age']
    city = city if city else user['city']
    hobby = hobby if hobby else user['hobby']
    gender = gender if gender else user['gender']
    language = language if language else user['language']

    update_user(username, age, city, hobby, gender, language)
