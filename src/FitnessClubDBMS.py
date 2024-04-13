import psycopg2
from psycopg2 import OperationalError

def create_connection():
    try:
        conn = psycopg2.connect(
            dbname="FitnessClub",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        print("Connection to the database successful")
        return conn
    except OperationalError as e:
        print(f"Error '{e}' occured")
        return None

def register_member(first_name, last_name, user_name, email, pwd):
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

def register_trainer(first_name, last_name, user_name, pwd):
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

def register_admin(user_name, pwd):
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

def changePassword(user_type, user_id, new_pwd):
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
            SET pwd = %s
            WHERE {user_type}_id = %s;
        """, (new_pwd, user_id))
        conn.commit()
        print("Password updated successfully")
    except Exception as e:
        print(f"Error '{e}' occurred")
    finally:
        cursor.close()
        conn.close()

def changeEmail(member_id, new_email):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE members
            SET email = %s
            WHERE member_id = %s
        """, (new_email, member_id))
        conn.commit()
        print("Email updated successfully")
    except Exception as e:
        print(f"Error '{e}' occurred")
    finally:
        cursor.close()
        conn.close()

def changeInfo(weight):
    return None

def newGoal():
    return None

def changeGoal():
    return None

def getGoals():
    return None

def getExerciseRoutines():
    return None

def getAchievements():
    return None

def getStats(member_id):
    return None

def newSession(trainer_id, member_id, session_date, session_time):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO training_sessions (trainer_id, member_id, session_date, session_time) VALUES (%s, %s, %s, %s)", (trainer_id, member_id, session_date, session_time))
        conn.commit()
        print("New training session created")
    except Exception as e:
        print(f"Error '{e}' occured")
    finally:
        cursor.close()
        conn.close()

def rescheduleSession(session_id, new_session_date, new_session_time):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE training_session SET session_date = %s, session_time = %s WHERE session_id = %s", (new_session_date, new_session_time, session_id))
        conn.commit()
        print("Training session rescheduled successfully")
    except Exception as e:
        print(f"Error '{e}' occurred")
    finally:
        cursor.close()
        conn.close()

def cancelSession(session_id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM training_sessions WHERE session_id = %s", (session_id))
        conn.commit()
        print("Training session cancelled")
    except Exception as e:
        print(f"Error '{e}' occurred")
    finally:
        cursor.close()
        conn.close()

def newClass(class_name, class_room, class_date, class_time):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO fitness_classes (class_name, class_room, class_date, class_time) VALUES (%s, %s, %s, %s)", (class_name, class_room, class_date, class_time))
        conn.commit()
        print("New fitness class created")
    except Exception as e:
        print(f"Error '{e}' occured")
    finally:
        cursor.close()
        conn.close()

def rescheduleClass(class_id, class_room, class_date, class_time):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE fitness_classes SET class_room = %s, class_date = %s, class_time = %s WHERE class_id = %s", (class_room, class_date, class_time, class_id))
        conn.commit()
        print("Class rescheduled successfully")
    except Exception as e:
        print(f"Error '{e}' occurred")
    finally:
        cursor.close()
        conn.close()

def deleteClass(class_id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM fitness_classes WHERE class_id = %s", (class_id))
        conn.commit()
        print("Fitness class deleted")
    except Exception as e:
        print(f"Error '{e}' occurred")
    finally:
        cursor.close()
        conn.close()

def registerForClass(class_id, member_id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO class_registrations (class_id, member_id) VALUES (%s, %s)", (class_id, member_id))
        conn.commit()
        print("Registered for fitness class")
    except Exception as e:
        print(f"Error '{e}' occurred")
    finally:
        cursor.close()
        conn.close()

def leaveClass(class_id, member_id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM class_registrations WHERE class_id = %s AND member_id = %s", (class_id, member_id))
        conn.commit()
        print("Left fitness class")
    except Exception as e:
        print(f"Error '{e}' occurred")
    finally:
        cursor.close()
        conn.close()

def setAvailability():
    return None

def getMemberProfile():
    return None

def viewMaintenance():
    return None

def processPayment():
    return None

def login():
    return None

def startMenu():
    print("\nWelcome To The Fitness Club!")
    print("Please choose an option (enter the number):")
    print("1. Login")
    print("2. Register")
    print("3. Exit")

def memberMenu():
    print("\nWelcome To The Fitness Club!")
    print("Please choose an option (enter the number):")
    print("1. View Goals")
    print("2. Book Training Session")
    print("3. Class Sign Up/Leave")
    print("4. Change Info")
    print("5. Exit")

def trainerMenu():
    print("\nFitness Club Trainer Menu")
    print("Please choose an option (enter the number):")
    print("1. View Training Sessions")
    print("2. Change Availability")
    print("3. Search Members")
    print("4. Change Info")
    print("5. Exit")

def adminMenu():
    print("\nFitness Club Administrator Menu")
    print("Please choose an option (enter the number):")
    print("1. Room Booking Management")
    print("2. Equipment Maintenance Monitoring")
    print("3. Update Class Schedules")
    print("4. Billing and Payment Processing")
    print("5. Change Info")
    print("6. Exit")

def changeInfoMenu():
    print("\nSelect the information you would like to change (enter the number):")
    print("1. Username")
    print("2. Password")
    print("3. Email") # For members only
    print("4. Return to Main Menu")

# main
