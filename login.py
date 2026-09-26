import bcrypt
import json
import os
import getpass
import hashlib
import userui.py

USER_DB = "users.json"


#Prompt user to log in or create account
def prompt_user():
    Choice = input("Create Account or Sign In?")
    choice = Choice.lower()
    if choice == "create account":
        sign_up()
    elif choice == "sign in":
        sign_in()
    else:
        print("Error Input in Wrong Format")
        prompt_user()

    

def sign_up():
    # load users from database
    if os.path.exists('users.json'):
        with open ('users.json', 'r') as file:
            users = json.load(file)
    else: 
        users = {}

    # prompt for username - if already availabe have user input another
    while True:
        username = input("Username: ")
        username = username.lower()
        if username in users:
            print("Error! Username Not Available. Please Try Again")
            continue
        break
    #have user enter a valid email address
    while True:
        email = input("Email: ")
        email = email.lower()
        if "@" not in email or "." not in email.split("@")[-1]:
            print("Please enter a valid email address")
            continue
        if any(user['email'] == email for user in users.values()):
            print("Error! Email address already registered")
            continue
        break
    #securely enter password using getpass, password must be > 10 characters, have a number and special character
    while True:
        password = getpass.getpass("Password: ") 
        if len(password) < 10 or not any(char.isdigit() for char in password) or not any(not char.isalnum() for char in password):
            print("Password must be at least 10 characters, include a special character, and a number")
            continue
        confirmPW = getpass.getpass("Confirm Password: ")
        if password != confirmPW:
            print("Passwords do not match")
            continue
        break
    #hash and salt the password before entering in the database
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    users[username] = {
        "email": email,
        "hash": hashed.decode()
    }
    with open('users.json', 'w') as file:
        json.dump(users, file, indent=2)
    Ui(users)

def sign_in():
    if os.path.exists('users.json'):
            with open ('users.json', 'r') as file:
                users = json.load(file)
    else: 
        print("No Users Registered, Please Sign Up")
        sign_up()
        return
    counter = 0
    while True:
        UName = input("Enter Username: ")
        pwurd = getpass.getpass("Enter Password: ")
        if UName in users and bcrypt.checkpw(pwurd.encode(), users[UName]["hash"].encode()):
            print("Login Successful!")
            break
        else:
            print("Incorrect Username or Password.")
            counter += 1
            if counter > 4:
                print("Too Many Failed Attempts, Account Temporarily Locked")
                return False
            continue
    Ui(users)


if __name__ == "__main__":
    login()
