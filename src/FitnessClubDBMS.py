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

def registerMember(first_name, last_name, user_name, email, pwd):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO members (first_name, last_name, user_name, email, pwd) VALUES (%s, %s, %s, %s, %s)", (first_name, last_name, user_name, email, pwd))
        conn.commit()
        print("New User Member added")
    except Exception as e:
        print(f"Error '{e}' occured")
    finally:
        cursor.close()
        conn.close()

def registerTrainer(first_name, last_name, user_name, pwd):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO trainers (first_name, last_name, user_name, pwd) VALUES (%s, %s, %s, %s)", (first_name, last_name, user_name, pwd))
        conn.commit()
        print("New User Trainer added")
    except Exception as e:
        print(f"Error '{e}' occured")
    finally:
        cursor.close()
        conn.close()

def registerAdmin(user_name, pwd):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO admins (user_name, pwd) VALUES (%s, %s)", (user_name, pwd))
        conn.commit()
        print("New User Administrator added")
    except Exception as e:
        print(f"Error '{e}' occured")
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

# main
if __name__ == "__main__":
    loggedIn = False
    user_id = None
    userType = None

    while True:
        if not loggedIn:
            startMenu()
            choice = input("Selected: ")

            if choice == '1':
                loggedIn, user_id, userType = login()
            elif choice == '2':
                print("Registration not implemented yet")
            elif choice == '3':
                print("Exiting...")
                break
            else:
                print("Invalid option, please try again.")
        else:
            if userType == 'member':
                member_id = user_id
                member_functions.memberMenu(member_id)
                break
            elif userType == 'trainer':
                trainer_id = user_id
                trainer_functions.trainerMenu(trainer_id)
                break
            elif userType == 'admin':
                admin_id = user_id
                admin_functions.adminMenu(admin_id)
                break