import database as db
from user_repo import create_user, get_user, update_user, delete_user, view_profile, edit_profile
from utility import  check_blank, press_enter_to_continue, check_number
from message import send_message, get_unread_count, fetch_unread_messages, mark_unread_as_read, view_conversation
from matching import match_users
from note import create_note, get_notes, get_notes_by_user
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
        hobby = check_blank("Enter your hobby: ").lower()
        gender = check_blank("Enter your gender: ").lower()
        language = check_blank("Enter your speak language: ").lower()
        create_user(username, age, city, hobby, gender, language)
    else:
        print("Exiting the application.")
        exit()
#while True:
username = check_blank("Enter your username: ").strip()
print("checking if username exists")
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

while True:
    print("\n")
    print("1.Change account")
    print("2.Edit Profil")
    print("3.Find match")
    print("4.Send message")
    print("5.View Messages")
    print("6.Write note")
    print("7.View Notes")
    print("8.Exit")
    choice = check_blank("Enter your choice: ")

    if choice == '1':
        print("\n")
        username = check_blank("Enter your new username: ").strip()
        if not get_user(username):
            print("Username not found. Please create an account first.")
            exit()
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
        view_profile(username)
        press_enter_to_continue()
        print("\n")
        edit = check_blank("Do you want to edit your profile? (yes/no): ").strip().lower()
        if edit == 'yes':
            edit_profile(username)
            press_enter_to_continue()
        else: 
            print("Profile not edited.")
            press_enter_to_continue()

    elif choice == '3':
        print("\n")
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
        press_enter_to_continue()

    elif choice == '4':
        print("\n")
        receiver = check_blank("Enter the username of the person you want to message: ").strip()
        content = input("Enter your message: ").strip()
        send_message(username, receiver, content)
        print("Message sent successfully!\n")
        press_enter_to_continue()

    elif choice == '5':
        print("\n")
        print("1.View all messages with a user")
        print("2.View conversation with a user and mark incoming messages as read")
        choice = check_blank("Enter your choice: ")
        if choice == '1':
            other_user = check_blank("Enter the username of the user to view messages with: ").strip()
            messages = view_conversation(username, other_user)
            for m in messages:
                direction = "You →" if m['sender'] == username else f"{m['sender']} →"
                print(f"[{m['timestamp']}] {direction} {m['receiver']}: {m['content']}")
            press_enter_to_continue()
        elif choice == '2':
            other_user = check_blank("Enter the username of the user to view conversation with: ").strip()
            messages = view_conversation(username, other_user, mark_read_for=username)
            for m in messages:
                direction = "You →" if m['sender'] == username else f"{m['sender']} →"
                print(f"[{m['timestamp']}] {direction} {m['receiver']}: {m['content']}")
            press_enter_to_continue()
        else:
            print("Invalid choice. Please try again.")
            press_enter_to_continue()

    elif choice == '6':
        print("\n")
        about_user = check_blank("Who is your note about? ").strip()
        content = check_blank("Note content: ").strip()
        create_note(username, about_user, content)
        print("Note successfully created!\n")
        press_enter_to_continue()


    elif choice == '7':
        print("\n")
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
        print("\n")
        print("Exit")
        break
    else:
        print("Invalid choice. Please try again.")


