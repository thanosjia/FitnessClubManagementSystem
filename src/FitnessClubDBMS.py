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

def newGoal(member_id, goal_type, goal_value):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO fitness_goals (member_id, goal_type, goal_value) VALUES (%s, %s, %s)", (member_id, goal_type, goal_value))
        conn.commit()
        print("New goal added successfully")
    except Exception as e:
        print(f"Error '{e}' occurred")
    finally:
        cursor.close()
        conn.close()

def changeGoal(goal_id, new_goal_type, new_goal_value):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE fitness_goals SET goal_type = %s, goal_value = %s WHERE goal_id = %s", (new_goal_type, new_goal_value, goal_id))
        conn.commit()
        print("Goal updated successfully")
    except Exception as e:
        print(f"Error '{e}' occurred")
    finally:
        cursor.close()
        conn.close()

def deleteGoal(goal_id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM fitness_goals WHERE goal_id = %s", (goal_id,))
        conn.commit()
        print("Goal deleted successfully")
    except Exception as e:
        print(f"Error '{e}' occurred")
    finally:
        cursor.close()
        conn.close()

def getGoals(member_id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT goal_id, goal_type, goal_value FROM fitness_goals WHERE member_id = %s", (member_id,))
        goals = cursor.fetchall()
        print(goals)
    except Exception as e:
        print(f"Error '{e}' occurred")
        return []
    finally:
        cursor.close()
        conn.close()

def getExerciseRoutines():
    return None

def getAchievements():
    return None

def setStats(member_id, height, mass):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO member_stats (member_id, height, mass) VALUES (%s, %s, %s)", (member_id, height, mass))
        conn.commit()
        print("Stats set")
    except Exception as e:
        print(f"Error '{e}' occured")
    finally:
        cursor.close()
        conn.close()

def getStats(member_id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT height, mass FROM member_stats WHERE member_id = %s", (member_id,))
        stats = cursor.fetchall()
        print(stats)
    except Exception as e:
        print(f"Error '{e}' occurred")
        return []
    finally:
        cursor.close()
        conn.close()

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

def setAvailability(trainer_id, available_date, available_time):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO trainer_availability (trainer_id, available_date, available_time)
            VALUES (%s, %s, %s)
        """, (trainer_id, available_date, available_time))
        conn.commit()
        print("Availability set successfully")
    except Exception as e:
        print(f"Error '{e}' occurred")
    finally:
        cursor.close()
        conn.close()

def getMemberProfile(member_id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT member_id, first_name, last_name, user_name, email, membership_status
            FROM members
            WHERE member_id = %s
        """, (member_id,))
        member_details = cursor.fetchone()
        if member_details:
            print("Member Profile:")
            print("Member ID: ", member_details[0])
            print("First Name: ", member_details[1])
            print("Last Name: ", member_details[2])
            print("Username: ", member_details[3])
            print("Email: ", member_details[4])
            print("Membership Status: ", "Active" if member_details[5] else "Inactive")
        else:
            print("No member found with ID", member_id)
    except Exception as e:
        print(f"Error '{e}' occurred")
    finally:
        cursor.close()
        conn.close()

def viewEquipment():
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM equipment")
        equipment = cursor.fetchall()
        print(equipment)
    except Exception as e:
        print(f"Error '{e}' occurred")
    finally:
        cursor.close()
        conn.close()

def changeEquipmentStatus(equipment_id, new_equipment_status):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE equipment SET new_equipment_status = %s WHERE equipment_id = %s", (new_equipment_status, equipment_id))
    except Exception as e:
        print(f"Error '{e}' occurred")
    finally:
        cursor.close()
        conn.close()

def processPayment(member_id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        # Check the current status of the member
        cursor.execute("SELECT membership_status FROM members WHERE member_id = %s", (member_id,))
        status = cursor.fetchone()
        
        if status is None:
            print("No member found with ID", member_id)
            return

        if status[0]:  # membership_status is True
            # Member is already active, fetch the most recent payment's next payment date
            cursor.execute("""
                SELECT next_payment_date FROM payments
                WHERE member_id = %s
                ORDER BY payment_date DESC
                LIMIT 1
            """, (member_id,))
            next_payment_date = cursor.fetchone()
            if next_payment_date:
                print("This member has already paid.")
                print("Next payment date is:", next_payment_date[0])
            else:
                print("No payment records found, but the member is marked as active.")
        else:
            # Process the payment and update membership status and payments table
            today = datetime.now().date()
            next_payment_date = today + timedelta(days=30)
            
            # Update member status
            cursor.execute("""
                UPDATE members
                SET membership_status = TRUE
                WHERE member_id = %s
            """, (member_id,))
            
            # Insert new payment record
            cursor.execute("""
                INSERT INTO payments (member_id, payment_date, next_payment_date, payment_method)
                VALUES (%s, %s, %s, 'Default Method')  -- Assuming a default method for simplification
            """, (member_id, today, next_payment_date))
            
            conn.commit()
            print("Payment processed successfully.")
            print("Membership activated.")
            print("Next payment date is:", next_payment_date)

    except Exception as e:
        print(f"Error '{e}' occurred")
        conn.rollback()  # Rollback in case of error
    finally:
        cursor.close()
        conn.close()

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
