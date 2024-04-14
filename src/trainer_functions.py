import psycopg2
from psycopg2 import OperationalError
from datetime import datetime, timedelta

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

# Trainer Menus
def trainerMenu(trainer_id):
    user_type = 'trainer'
    while True:
        print("\nTrainer Menu")
        print("1. View Training Sessions")
        print("2. Change Availability")
        print("3. Search Members")
        print("4. Change Info")
        print("5. Logout")

        choice = input("Selected: ")
        if choice == '1':
            viewTrainerSessions(trainer_id)
        elif choice == '2':
            changeAvailabilityMenu(trainer_id)
        elif choice == '3':
            searchMembers()
        elif choice == '4':
            changeInfoMenu(user_type, trainer_id)
        elif choice == '5':
            print("Logging out...")
            break
        else:
            print("Invalid option, please try again.")

def changeAvailabilityMenu(trainer_id):
    while True:
        print("\nChange Availability Menu")
        print("1. View Availability")
        print("2. Add Availability")
        print("3. Remove Availability")
        print("4. Return to Main Menu")

        choice = input("Selected: ")
        if choice == '1':
            viewAvailability(trainer_id)
        elif choice == '2':
            addAvailability(trainer_id)
        elif choice == '3':
            removeAvailability(trainer_id)
        elif choice == '4':
            break
        else:
            print("Invalid option, please try again.")

def viewTrainerSessions(trainer_id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        SELECT ts.session_id, ts.session_date, ts.session_time, m.first_name, m.last_name, m.user_name
        FROM training_sessions ts
        JOIN members m ON ts.member_id = m.member_id
        WHERE ts.trainer_id = %s
        ORDER BY ts.session_date, ts.session_time
        """, (trainer_id,))
        sessions = cursor.fetchall()
        print("Scheduled Training Sessions:")
        for session in sessions:
            print(f"Session ID: {session[0]}, Date: {session[1]}, Time: {session[2]}, Member: {session[3]} {session[4]} (Username: {session[5]})")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        cursor.close()
        conn.close()

def addAvailability(trainer_id):
    available_date = input("Enter available date (YYYY-MM-DD): ")
    available_time = input("Enter available time (HH:MM): ")
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        INSERT INTO trainer_availability (trainer_id, available_date, available_time)
        VALUES (%s, %s, %s)
        """, (trainer_id, available_date, available_time))
        conn.commit()
        print("Availability added successfully")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        cursor.close()
        conn.close()

def removeAvailability(trainer_id):
    availability_id = input("Enter the ID of the availability slot to remove: ")
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM trainer_availability WHERE availability_id = %s AND trainer_id = %s", (availability_id, trainer_id))
        conn.commit()
        print("Availability removed successfully")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        cursor.close()
        conn.close()

def viewAvailability(trainer_id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        SELECT availability_id, available_date, available_time
        FROM trainer_availability
        WHERE trainer_id = %s
        ORDER BY available_date, available_time
        """, (trainer_id,))
        availabilities = cursor.fetchall()
        print("Available Slots:")
        for availability in availabilities:
            print(f"ID: {availability[0]}, Date: {availability[1]}, Time: {availability[2]}")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        cursor.close()
        conn.close()









def searchMembers():
    search_query = input("Enter member's username or name to search for: ")
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        SELECT first_name, last_name, user_name, email, membership_status
        FROM members
        WHERE user_name ILIKE %s OR first_name ILIKE %s OR last_name ILIKE %s
        """, (f'%{search_query}%', f'%{search_query}%', f'%{search_query}%'))
        members = cursor.fetchall()
        print("Search Results:")
        for member in members:
            print(f"Name: {member[0]} {member[1]}, Username: {member[2]}, Email: {member[3]}, Status: {'Active' if member[4] else 'Inactive'}")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        cursor.close()
        conn.close()

def changeUsername(user_type, user_id, new_user_name):
    table = {
        'member': 'members',
        'trainer': 'trainers',
        'admin': 'admins'
    }.get(user_type)

    if table is None:
        raise ValueError("Invalid user type provided.")
    
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f"""
            UPDATE {table}
            SET user_name = %s
            WHERE {user_type}_id = %s;
        """, (new_user_name, user_id))
        conn.commit()
        print("Username updated successfully")
    except Exception as e:
        print(f"Error '{e}' occurred")
    finally:
        cursor.close()
        conn.close()

def verifyCurrentPassword(user_type, user_id, current_pwd):
    table = {
        'member': 'members',
        'trainer': 'trainers',
        'admin': 'admins'
    }.get(user_type)

    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT pwd FROM {table} WHERE {user_type}_id = %s", (user_id,))
        stored_pwd = cursor.fetchone()
        if stored_pwd and stored_pwd[0] == current_pwd:
            return True
        return False
    finally:
        cursor.close()
        conn.close()

def changePassword(user_type, user_id):
    table = {
        'member': 'members',
        'trainer': 'trainers',
        'admin': 'admins'
    }.get(user_type)

    current_pwd = input("Enter your current password: ")
    if verifyCurrentPassword(user_type, user_id, current_pwd):
        new_pwd = input("Enter new password: ")
        confirm_new_pwd = input("Confirm new password: ")
        
        if new_pwd != confirm_new_pwd:
            print("Passwords do not match. Try again.")
            return
        
        conn = create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(f"UPDATE {table} SET pwd = %s WHERE {user_type}_id = %s", (new_pwd, user_id))
            conn.commit()
            print("Password updated successfully")
        except Exception as e:
            print(f"Error '{e}' occurred")
        finally:
            cursor.close()
            conn.close()
    else:
        print("Current password is incorrect.")

def changeInfoMenu(user_type, user_id):
    while True:
        print("\nChange Information Menu")
        print("1. Change Username")
        print("2. Change Password")
        if user_type == 'member':
            print("3. Change Email")
            print("4. Return to Main Menu")
        else:
            print("3. Return to Main Menu")

        choice = input("Selected: ")
        if choice == '1':
            new_username = input("Enter new username: ")
            changeUsername(user_type, user_id, new_username)
        elif choice == '2':
            changePassword(user_type, user_id)
        elif choice == '3':
            break
        else:
            print("Invalid option, please try again.")