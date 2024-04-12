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

def establishGoal():
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

def newSession():
    return None

def rescheduleSession():
    return None

def cancelSession():
    return None

def newClass(class_name, class_room, class_date, class_time):
    conn = create_connection()
    cursor = conn.cursor
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
        cursor.execute("DELETE FROM fitness_classes WHERE class_id = %s", (class_id,))
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

def bookRoom():
    return None

def changeBooking():
    return None

def deleteBooking():
    return None

def viewMaintenance():
    return None

def processPayment():
    return None

def login():
    return None

def loginMenu():
    return None

def mainMenu():
    return None

# main
