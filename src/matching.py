
# file: matching.py
# purpose: Provide user matching logic based on preferences and profile similarity
# author: Boon
# date: 2025-09-29

import database as db
hobbies = ['reading', 'traveling', 'cooking', 'sports', 'music', 'gaming']

def match_users(city, hobby, min_age, max_age, prefer_gender, language, username):
    """
    Find and rank the top 5 users that best match the given user's preferences.

    Args:
        city (str): The preferred city to match with.
        hobby (str): The preferred hobby to match.
        min_age (int): Minimum preferred age.
        max_age (int): Maximum preferred age.
        prefer_gender (str): Preferred gender.
        language (str): Preferred spoken language.
        username (str): The current user's username (excluded from matching).

    Returns:
        list[dict]: A list of up to 5 dictionaries, each representing a matched user
                    with their details and a calculated matching score.
    """
    conn = db.get_conn()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE username != ? AND LOWER(gender) = LOWER(?);", (username, prefer_gender))
    all_users = cur.fetchall()

    matches = []
    for user in all_users:
        score = 0

        # --- Matching Criteria and Scoring System ---
        # City match (case-insensitive, safe for NULL values)
        if (user["city"] or "").lower() == city.lower():
            score += 20

        # Hobby match (case-insensitive, safe for NULL values)
        if (user["hobby"] or "").lower() == hobby.lower():
            score += 40

        # Age match (adds or deducts points based on closeness)
        age = user["age"]
        if isinstance(age, (int, float)):
            if min_age <= age <= max_age:
                score += 20
            elif age < min_age - 5 or age > max_age + 5:
                score -= 20

        # Gender preference match (case-insensitive)
        if (user["gender"] or "").lower() == prefer_gender.lower():
            score += 100

        # Language preference match (case-insensitive)
        if (user["language"] or "").lower() == language.lower():
            score += 20

        # Avoid overwriting function argument 'language'
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
    top_matches = matches[:5]

    conn.close()
    return top_matches
