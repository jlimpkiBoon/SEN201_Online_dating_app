import database as db
from user_repo import create_user, get_user, update_user, delete_user, view_profile, edit_profile
from utility import is_number, check_blank
from message import send_message, view_messages
hobbies = ['reading', 'traveling', 'cooking', 'sports', 'music', 'gaming']

def match_users(city, hobby, min_age, max_age, prefer_gender, language, username):
    conn = db.get_conn()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE username != ?;", (username,))
    all_users = cur.fetchall()

    matches = []
    for user in all_users:
        score = 0

        if user["city"].lower() == city.lower():
            score += 30

        if user["hobby"].lower() == hobby.lower():
            score += 25

        if min_age <= user["age"] <= max_age:
            score += 20
        elif user["age"] < min_age - 5 or user["age"] > max_age + 5:
            score -= 10

        if "gender" in user.keys() and user["gender"].lower() == prefer_gender.lower():
            score += 15

        if "language" in user.keys() and user["language"].lower() == language.lower():
            score += 10

        matches.append({
            "username": user["username"],
            "age": user["age"],
            "city": user["city"],
            "hobby": user["hobby"],
            "gender": user.get("gender", "unknown"),
            "language": user.get("language", "unknown"),
            "score": score
        })

    # Sort by best match
    matches.sort(key=lambda x: x["score"], reverse=True)

    conn.close()
    return matches
