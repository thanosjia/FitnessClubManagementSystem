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

def register_user(first_name, last_name, user_name, email, pwd, payment_method):
    conn = create_connection()
    cursor = conn.cursor
    try:
        cursor.execute("INSERT INTO members (first_name, last_name, user_name, email, pwd, payment_method) VALUES (%s, %s, %s, %s, %s, %s)", (first_name, last_name, user_name, email, pwd, payment_method))
        conn.commit()
        print("New Member registration Successful")
    except Exception as e:
        print(f"Error '{e}' occured")
    finally:
        cursor.close()
        conn.close()

def login():
    return None

def changeUsername(member_id, new_user_name):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE members SET user_name = %s WHERE member_id = %s", (new_user_name, member_id))
        conn.commit()
        print("Username updated successfully")
    except Exception as e:
        print(f"Error '{e}' occurred")
    finally:
        cursor.close()
        conn.close()

def changePassword(member_id, new_pwd):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE members SET pwd = %s WHERE member_id = %s", (new_pwd, member_id))
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
        cursor.execute("UPDATE members SET email = %s WHERE member_id = %s", (new_email, member_id))
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
        # Find out the proper % type for date and time
        cursor.execute("INSERT INTO fitness_classes (class_name, class_room, class_date, class_time) VALUES (%s, %d, %date, %time)", (class_name, class_room, class_date, class_time))
        conn.commit()
        print("New Class created")
    except Exception as e:
        print(f"Error '{e}' occured")
    finally:
        cursor.close()
        conn.close()

def deleteClass():
    return None

def registerForClass():
    return None

def leaveClass():
    return None

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