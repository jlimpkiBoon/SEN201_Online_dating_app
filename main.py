import database as db
from user_repo import create_user, get_user, update_user, delete_user

print("welcome to dating app")

new = input("Are you a new user? (yes/no): ").strip().lower()
if new == 'yes':
    create = input("Do you want to create a new account? (yes/no): ").strip().lower()
    print("create account")
    print("checking if username exists")
#while True:
username = input("Enter your username: ").strip()
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
        print("change account")
    elif choice == '2':
        print("edit profile")
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


