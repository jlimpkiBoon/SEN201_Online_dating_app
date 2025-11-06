# file: user_repo.py
# purpose: Manage user profiles — including creation, retrieval, update, deletion, and profile editing.
# author: Boon
# date: 2025-09-29

import sqlite3
from database import init_db, get_conn

def create_user(username, age, city, hobby, gender, language):
    """
    Create a new user record in the database.

    Args:
        username (str): Unique username.
        age (int): User's age.
        city (str): User's city.
        hobby (str): User's hobby.
        gender (str): User's gender.
        language (str): User's preferred language.

    Returns: None
    """
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
    """
    Retrieve a user record by username.

    Args:
        username (str): Username to search for.

    Returns:
        dict: User data as a dictionary, or None if not found.
    """
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
    """
    Update a user's profile details.

    Args:
        username (str): Username of the user to update.
        age (int): Updated age.
        city (str): Updated city.
        hobby (str): Updated hobby.
        gender (str): Updated gender.
        language (str): Updated language.

    Returns: None
    """
    conn = get_conn()
    cur = conn.cursor()
    
    # Update user information
    cur.execute(
        "UPDATE users SET age = ?, city = ?, hobby = ?, gender = ?, language = ? WHERE username = ?;",
        (age, city, hobby, gender, language, username)
    )
    conn.commit()
    conn.close()
    print("User updated successfully!")

def delete_user(username):
    """
    Delete a user record from the database.

    Args:
        username (str): Username of the user to delete.

    Returns: None
    """
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
    """
    Display a user's profile information.

    Args:
        username (str): Username whose profile to view.

    Returns: None
    """
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
    """
    Allow the user to interactively edit their profile fields.
    Prompts for each field and keeps the existing value if left blank.

    Args:
        username (str): Username of the profile to edit.

    Returns:
        None
    """
    user = get_user(username)
    if not user:
        print("User not found.")
        return
    print("Leave a field blank to keep the current value.")

     # Prompt for new values
    age = input(f"Enter new age (current: {user['age']}): ").strip()
    city = input(f"Enter new city (current: {user['city']}): ").strip()
    hobby = input(f"Enter new hobby (current: {user['hobby']}): ").strip()
    gender = input(f"Enter new gender (current: {user['gender']}): ").strip()
    language = input(f"Enter new language (current: {user['language']}): ").strip()

    # Use existing values if left blank
    age = int(age) if age else user['age']
    city = city if city else user['city']
    hobby = hobby if hobby else user['hobby']
    gender = gender if gender else user['gender']
    language = language if language else user['language']

    update_user(username, age, city, hobby, gender, language)
