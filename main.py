import database as db
from user_repo import create_user, get_user, update_user, delete_user, view_profile, edit_profile
from utility import check_number, check_blank
from message import send_message, view_messages
from matching import match_users
hobbies = ['reading', 'traveling', 'cooking', 'sports', 'music', 'gaming']  

print("welcome to dating app")
new = check_blank("Are you a new user? (yes/no): ").strip().lower()
if new == 'yes':
    create = check_blank("Do you want to create a new account? (yes/no): ").strip().lower()
    if create == 'yes':
        username = check_blank("Enter your username: ").lower()
        age = check_number("Enter your age: ")
        city = check_blank("Enter your city: ").lower()
        print("Please select your hobby from the following options:")
        for i, hobby in enumerate(hobbies, start=1):
            print(f"{i}. {hobby}")
        hobby = check_blank("Enter your hobby: ").lower()
        gender = check_blank("Enter your gender: ").lower()
        language = check_blank("Enter your speak language: ").lower()
        create_user(username, age, city, hobby)
    else:
        print("Exiting the application.")
        exit()
#while True:
username = check_blank("Enter your username: ").strip()
print("checking if username exists")
print(f"Hello, {username}!")

while True:
    print("1.Change account")
    print("2.Edit Profil")
    print("3.Find match")
    print("4.send message")
    print("5.View Messages")
    print("6.write note")
    print("7.View Notes")
    print("8.Exit")
    choice = input("Enter your choice: ").strip()
    if choice == '1':
        username = check_blank("Enter your new username: ").strip()
        if get_user(username):
            print(f"Hello, {username}!")
        else:
            print("Username does not exist.")
    elif choice == '2':
        view_profile(username)
        edit = check_blank("Do you want to edit your profile? (yes/no): ").strip().lower()
        if edit == 'yes':
            edit_profile(username)
        else: 
            print("Profile not edited.")
    elif choice == '3':
        match_city = check_blank("Enter the city to find matches: ").lower()
        for i, hobby in enumerate(hobbies, start=1):
            print(f"{i}. {hobby}")
        match_hobby = check_blank("Enter the hobby to find matches: ").lower()
        maximum_age = check_number("Enter the maximum age to find matches: ")
        minimum_age = check_number("Enter the minimum age to find matches: ")
        prefer_gender = check_blank("Enter preferred gender to find matches: ").lower()
        language = check_blank("Enter preferred language to find matches: ").lower()
        matches = match_users(match_city, match_hobby, minimum_age, maximum_age, prefer_gender, language, username)
        if matches:
            print("Matched Users:")
            for match in matches:
                print(f"Username: {match['username']}, Age: {match['age']}, City: {match['city']}, Hobby: {match['hobby']}, Gender: {match['gender']}")
    elif choice == '4':
        print("send message")
    elif choice == '5':
        print("view messages")
    elif choice == '6':
        print("write note")
    elif choice == '7':
        print("view notes")
    elif choice == '8':
        print("exit")
        break
    else:
        print("Invalid choice. Please try again.")


