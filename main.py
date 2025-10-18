import database as db
from user_repo import create_user, get_user, update_user, delete_user, view_profile, edit_profile
from utility import is_number, check_blank
from message import send_message, view_messages
hobbies = ['reading', 'traveling', 'cooking', 'sports', 'music', 'gaming']  

print("welcome to dating app")
new = check_blank("Are you a new user? (yes/no): ").strip().lower()
if new == 'yes':
    create = check_blank("Do you want to create a new account? (yes/no): ").strip().lower()
    if create == 'yes':
        username = check_blank("Enter your username: ").lower()
        age = check_blank("Enter your age: ")
        city = check_blank("Enter your city: ").lower()
        print("Please select your hobby from the following options:")
        for i, hobby in enumerate(hobbies, start=1):
            print(f"{i}. {hobby}")
        hobby = check_blank("Enter your hobby: ").lower()
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
    print("find match")
    print("4.send message")
    print("5.View Messages")
    print("6.write note")
    print("7.View Notes")
    print("8.Exit")
    choice = input("Enter your choice: ").strip()
    if choice == '1':
        username = check_blank("Enter your new username: ").strip()
        print(f"Hello, {username}!")
    elif choice == '2':
        view_profile(username)
        edit = check_blank("Do you want to edit your profile? (yes/no): ").strip().lower()
        if edit == 'yes':
            edit_profile(username)
        else: 
            print("Profile not edited.")
    elif choice == '3':
        print("find match")
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


