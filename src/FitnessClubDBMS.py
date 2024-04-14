import psycopg2
from psycopg2 import OperationalError
from datetime import datetime, timedelta

import admin_functions
import trainer_functions
import member_functions

def create_connection():
    try:
        conn = psycopg2.connect(
            dbname="FitnessClub",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        # print("Connection to the database successful")
        return conn
    except OperationalError as e:
        print(f"Error '{e}' occured")
        return None

def registerMemberProcess():
    print("\nRegister as a New Member")
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    email = input("Enter email: ")
    # Validate username
    valid_username = False
    while not valid_username:
        user_name = input("Enter username (no spaces allowed): ")
        if ' ' in user_name:
            print("Username cannot contain spaces. Please try again.")
        else:
            if checkUsernameExists(user_name):
                print("This username already exists. Please try another.")
            else:
                valid_username = True
    pwd = input("Enter password: ")
    return registerMember(first_name, last_name, user_name, email, pwd)

def checkUsernameExists(username):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT user_name FROM members WHERE user_name = %s", (username,))
        if cursor.fetchone():
            return True
        else:
            return False
    except Exception as e:
        print(f"Error occurred during username check: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def registerMember(first_name, last_name, user_name, email, pwd):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        INSERT INTO members (first_name, last_name, user_name, email, pwd)
        VALUES (%s, %s, %s, %s, %s)
        """, (first_name, last_name, user_name, email, pwd))
        conn.commit()
        print("New User Member added")
        return True, cursor.lastrowid, 'member'  # Assuming 'member_id' is returned correctly
    except Exception as e:
        print(f"Error '{e}' occurred")
        return False, None, None  # Handle registration failure
    finally:
        cursor.close()
        conn.close()


def login():
    username = input("Enter username: ")
    password = input("Enter password: ")
    conn = create_connection()
    cursor = conn.cursor()

    try:
        # Check members
        cursor.execute("SELECT pwd, member_id FROM members WHERE user_name = %s", (username,))
        result = cursor.fetchone()
        if result and result[0] == password:
            print("Login successful - Welcome Member!")
            return True, result[1], 'member'

        # Check trainers
        cursor.execute("SELECT pwd, trainer_id FROM trainers WHERE user_name = %s", (username,))
        result = cursor.fetchone()
        if result and result[0] == password:
            print("Login successful - Welcome Trainer!")
            return True, result[1], 'trainer'

        # Check admins
        cursor.execute("SELECT pwd, admin_id FROM admins WHERE user_name = %s", (username,))
        result = cursor.fetchone()
        if result and result[0] == password:
            print("Login successful - Welcome Admin!")
            return True, result[1], 'admin'

        print("Invalid username or password. Try again? Yes (y) or No (n):")
        retry = input()
        if retry.lower() != 'y':
            return False, None, None
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()
    return False, None, None

def startMenu():
    print("\nWelcome To The Fitness Club!")
    print("Please choose an option (enter the number):")
    print("1. Login")
    print("2. Register")
    print("3. Exit")

    choice = input("Selected: ")
    if choice == '1':
        return login()
    elif choice == '2':
        return registerMemberProcess()
    elif choice == '3':
        print("Exiting...")
        return False, None, None
    else:
        print("Invalid option, please try again.")
        return False, None, None


# main
if __name__ == "__main__":
    loggedIn = False
    user_id = None
    userType = None

    while not loggedIn:
        loggedIn, user_id, userType = startMenu()
        if not loggedIn:
            break  # Exit the loop if user chooses to exit or fails to login/register

    if loggedIn:
        if userType == 'member':
            member_functions.memberMenu(user_id)
        elif userType == 'trainer':
            trainer_functions.trainerMenu(user_id)
        elif userType == 'admin':
            admin_functions.adminMenu(user_id)
