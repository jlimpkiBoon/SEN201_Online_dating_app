from database import init_db
import database as db
from user_repo import create_user, get_user, update_user, delete_user, view_profile, edit_profile
from utility import  check_blank, press_enter_to_continue, check_number
from message import send_message, get_unread_count, fetch_unread_messages, mark_unread_as_read, view_conversation
from matching import match_users
from note import create_note, get_notes, get_notes_by_user
init_db()
hobbies = ['reading', 'traveling', 'cooking', 'sports', 'music', 'gaming']  

print("Welcome to dating app")
new = check_blank("Are you a new user? (yes/no): ").strip().lower()
if new == 'yes':
    create = check_blank("Do you want to create a new account? (yes/no): ").strip().lower()
    if create == 'yes':
        username = check_blank("Enter your username: ").lower()
        age = check_blank("Enter your age: ")
        city = check_blank("Enter your city: ").lower()
        print("Please select your hobby from the following options:")
        for i, hobby in enumerate(hobbies, start=1):
            print(f"{hobby}")
        while True:
            hobby = check_blank("Enter your hobby: ").lower()
            if hobby in hobbies:
                break
            else:
                print("Invalid hobby. Please choose from the listed options.")
        gender = check_blank("Enter your gender: ").lower()
        language = check_blank("Enter your speak language: ").lower()
        create_user(username, age, city, hobby, gender, language)
    else:
        print("Exiting the application.")
        exit()

#while True:
username = check_blank("Enter your username: ").strip()
print(f"\nHello, {username}!")
unread = get_unread_count(username)
if unread > 0:
    print(f"\nYou have {unread} unread message(s). Showing them now:\n")
    msgs = fetch_unread_messages(username)
    for m in msgs:
        print(f"[{m['timestamp']}] {m['sender']} → You: {m['content']}")
    mark_unread_as_read(username)
    press_enter_to_continue()
else:
    print("No unread messages.\n")

while True:
    print()
    print("-----------------------------------")
    print("Main Menu:")
    print("-----------------------------------")
    print("1.Change Account")
    print("2.Edit Profile")
    print("3.Find Match")
    print("4.Send Message")
    print("5.View Messages")
    print("6.Write Note")
    print("7.View Notes")
    print("8.Exit")
    choice = check_blank("Enter your choice: ")


    if choice == '1':
        print()
        print("1. Create a new account")
        print("2. Switch to an existing account")
        sub_choice = check_blank("Enter your choice: ")
        if sub_choice == '1':
            username = check_blank("Enter your new username: ").lower()
            if get_user(username):
                print("Username already exists. Please choose a different username.")
                press_enter_to_continue()
            else:
                age = check_blank("Enter your age: ")
                city = check_blank("Enter your city: ").lower()
                print("Please select your hobby from the following options:")
                for i, hobby in enumerate(hobbies, start=1):
                    print(f"{hobby}")
                hobby = check_blank("Enter your hobby: ").lower()
                gender = check_blank("Enter your gender: ").lower()
                language = check_blank("Enter your speak language: ").lower()
                create_user(username, age, city, hobby, gender, language)
                print(f"Account created successfully! You are now logged in as {username}.\n")
                press_enter_to_continue()
        elif sub_choice == '2':
            username = check_blank("Enter your new username: ").strip()
            if not get_user(username):
                press_enter_to_continue()
                continue
            if get_user(username):
                print("\n")
                print(f"Hello, {username}!")
                unread = get_unread_count(username)
                if unread > 0:
                    print(f"\nYou have {unread} unread message(s). Showing them now:\n")
                    msgs = fetch_unread_messages(username)
                    for m in msgs:
                        print(f"[{m['timestamp']}] {m['sender']} → You: {m['content']}")
                    mark_unread_as_read(username)
                    press_enter_to_continue()
                else:
                    print("No unread messages.\n")
        
            
    elif choice == '2':
        print()
        view_profile(username)
        press_enter_to_continue()
        print()
        edit = check_blank("Do you want to edit your profile? (yes/no): ").strip().lower()
        if edit == 'yes':
            edit_profile(username)
            press_enter_to_continue()
        else: 
            print("Profile not edited.")
            press_enter_to_continue()


    elif choice == '3':
        print()
        match_city = check_blank("Enter the city to find matches: ").lower()
        for i, hobby in enumerate(hobbies, start=1):
            print(f"{i}. {hobby}")
        while True:
            match_hobby = check_blank("Enter the hobby to find matches(input text): ").lower()
            if match_hobby in hobbies:
                break
            else:
                print("Invalid hobby. Please choose from the listed options.")
        maximum_age = check_number("Enter the maximum age to find matches: ")
        minimum_age = check_number("Enter the minimum age to find matches: ")
        prefer_gender = check_blank("Enter preferred gender to find matches: ").lower()
        language = check_blank("Enter preferred language to find matches: ").lower()
        matches = match_users(match_city, match_hobby, minimum_age, maximum_age, prefer_gender, language, username)
        if matches:
            print("\nMatched Users:")
            for match in matches:
                print(f"Username: {match['username']}, Age: {match['age']}, City: {match['city']}, Hobby: {match['hobby']}, Gender: {match['gender']}")
        press_enter_to_continue()


    elif choice == '4':
        print()
        receiver = check_blank("Enter the username of the person you want to message: ").strip()
        content = check_blank("Enter your message: ").strip()
        send_message(username, receiver, content)
        press_enter_to_continue()


    elif choice == '5':
        print()
        print("1.View all messages with a user")
        print("2.View conversation with a user and mark incoming messages as read")
        choice = check_blank("Enter your choice: ")
        if choice == '1':
            other_user = check_blank("Enter the username of the user to view messages with: ").strip()
            messages = view_conversation(username, other_user)
            for m in messages:
                direction = "You →" if m['sender'] == username else f"{m['sender']} →"
                print(f"[{m['timestamp']}] {direction} {m['receiver']}: {m['content']}")
            if not messages:
                print("No messages found with this user.")
            press_enter_to_continue()
        elif choice == '2':
            other_user = check_blank("Enter the username of the user to view conversation with: ").strip()
            messages = view_conversation(username, other_user, mark_read_for=username)
            for m in messages:
                direction = "You →" if m['sender'] == username else f"{m['sender']} →"
                print(f"[{m['timestamp']}] {direction} {m['receiver']}: {m['content']}")
            if not messages:
                print("No messages found with this user.")
            press_enter_to_continue()
        else:
            print("Invalid choice. Please try again.")
            press_enter_to_continue()


    elif choice == '6':
        print()
        about_user = check_blank("Who is your note about? ").strip()
        content = check_blank("Note content: ").strip()
        create_note(username, about_user, content)
        print("Note successfully created!\n")
        press_enter_to_continue()


    elif choice == '7':
        print()
        print("1.View all notes")
        print("2.Search note by username")
        choice = check_blank("Enter your choice: ")
        if choice == '1':
            get_notes(username)
            press_enter_to_continue()
        elif choice == '2':
            print("\n")
            about_user = check_blank("Who do you want yo search your note about? ").strip()
            get_notes_by_user(username, about_user)
            press_enter_to_continue()
        else:
            print("Invalid choice. Please try again.")
            press_enter_to_continue()


    elif choice == '8':
        print()
        print("Exit")
        break
    
    else:
        print("Invalid choice. Please try again.")


