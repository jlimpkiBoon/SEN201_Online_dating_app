import database as db
hobbies = ['reading', 'traveling', 'cooking', 'sports', 'music', 'gaming']

def match_users(city, hobby, min_age, max_age, prefer_gender, language, username):
    conn = db.get_conn()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE username != ?;", (username,))
    all_users = cur.fetchall()

    matches = []
    for user in all_users:
        score = 0

        # NULL-safe string compares
        if (user["city"] or "").lower() == city.lower():
            score += 30

        if (user["hobby"] or "").lower() == hobby.lower():
            score += 25

        # Age scoring (guard against None)
        age = user["age"]
        if isinstance(age, (int, float)):
            if min_age <= age <= max_age:
                score += 20
            elif age < min_age - 5 or age > max_age + 5:
                score -= 10

        # Preference matches (NULL-safe)
        if (user["gender"] or "").lower() == prefer_gender.lower():
            score += 15

        if (user["language"] or "").lower() == language.lower():
            score += 10

        # Do NOT shadow the function parameter 'language'
        user_gender = user["gender"] or "unknown"
        user_language = user["language"] or "unknown"

        matches.append({
            "username": user["username"],
            "age": user["age"],
            "city": user["city"],
            "hobby": user["hobby"],
            "gender": user_gender,
            "language": user_language,
            "score": score,
        })

    # Sort by best match
    matches.sort(key=lambda x: x["score"], reverse=True)

    conn.close()
    return matches
