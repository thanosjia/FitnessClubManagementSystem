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
    
# Member Menus
def memberMenu(member_id):
    user_type = 'member'
    while True:
        print("\nMember Menu")
        print("1. Goals")
        print("2. Training Sessions")
        print("3. Classes")
        print("4. Change Info")
        print("5. Logout")

        choice = input("Selected: ")
        if choice == '1':
            goalsMenu(member_id)
        elif choice == '2':
            trainingSessionsMenu(member_id)
        elif choice == '3':
            classesMenu(member_id)
        elif choice == '4':
            changeInfoMenu(user_type, member_id)
        elif choice == '5':
            print("Logging out...")
            return  # Exiting the function logs the user out
        else:
            print("Invalid option, please try again.")

def goalsMenu(member_id):
    while True:
        print("\nGoals Menu")
        print("1. View Goals")
        print("2. Add Goal")
        print("3. Change Goal")
        print("4. Delete Goal")
        print("5. Return to Main Menu")

        choice = input("Selected: ")
        if choice == '1':
            getGoals(member_id)
        elif choice == '2':
            goal_type = input("Enter goal type: ")
            goal_value = int(input("Enter goal value: "))
            newGoal(member_id, goal_type, goal_value)
        elif choice == '3':
            goal_id = int(input("Enter goal ID to change: "))
            new_goal_type = input("Enter new goal type: ")
            new_goal_value = int(input("Enter new goal value: "))
            changeGoal(goal_id, new_goal_type, new_goal_value)
        elif choice == '4':
            goal_id = int(input("Enter goal ID to delete: "))
            deleteGoal(goal_id)
        elif choice == '5':
            break
        else:
            print("Invalid option, please try again.")

def trainingSessionsMenu(member_id):
    while True:
        print("\nTraining Sessions Menu")
        print("1. View All Training Sessions")
        print("2. Book Training Session")
        print("3. Reschedule Training Session")
        print("4. Cancel Training Session")
        print("5. Return to Main Menu")

        choice = input("Selected: ")
        if choice == '1':
            getSessions(member_id)
        elif choice == '2':
            bookTrainingSession(member_id)
        elif choice == '3':
            rescheduleTrainingSession(member_id)
        elif choice == '4':
            cancelSession(member_id)
        elif choice == '5':
            break
        else:
            print("Invalid option, please try again.")

def classesMenu(member_id):
    while True:
        print("\nClasses Menu")
        print("1. View All Classes")
        print("2. View Signed Up Classes")
        print("3. Leave a Class")
        print("4. Search for Classes")
        print("5. Sign Up for a Class")
        print("6. Return to Main Menu")

        choice = input("Selected: ")
        if choice == '1':
            listAllClasses()
        elif choice == '2':
            viewSignedUpClasses(member_id)
        elif choice == '3':
            leaveClass(member_id)
        elif choice == '4':
            class_name = input("Enter class name to search for: ")
            searchClasses(class_name)
        elif choice == '5':
            signUpForClass(member_id)
        elif choice == '6':
            break
        else:
            print("Invalid option, please try again.")

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
            new_email = input("Enter new email: ")
            changeEmail(user_type, user_id, new_email)
        elif choice == '4':
            break
        else:
            print("Invalid option, please try again.")

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

def listTrainers():
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT trainer_id, first_name, last_name FROM trainers")
        trainers = cursor.fetchall()
        if trainers:
            print("Available Trainers:")
            for trainer in trainers:
                print(f"Trainer ID: {trainer[0]}, Name: {trainer[1]} {trainer[2]}")
        else:
            print("No trainers found.")
    except Exception as e:
        print(f"Error '{e}' occurred")
    finally:
        cursor.close()
        conn.close()

def bookTrainingSession(member_id):
    listTrainers()
    trainer_id = input("Enter the Trainer ID to book a session with: ")
    # Ensure only future availability is shown
    viewTrainerAvailability(trainer_id)
    availability_id = input("Select Availability ID from the available slots: ")

    conn = create_connection()
    cursor = conn.cursor()
    try:
        # Fetch the availability slot based on ID and ensure it's in the future
        cursor.execute("SELECT available_date, available_time FROM trainer_availability WHERE availability_id = %s AND available_date >= %s", (availability_id, datetime.now().date()))
        availability_info = cursor.fetchone()
        if availability_info:
            available_date, available_time = availability_info
            cursor.execute("INSERT INTO training_sessions (trainer_id, member_id, session_date, session_time) VALUES (%s, %s, %s, %s)", (trainer_id, member_id, available_date, available_time))
            conn.commit()
            print("Training session booked successfully.")
        else:
            print("Invalid availability ID. Please try again.")
    except Exception as e:
        print(f"Error occurred: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def rescheduleTrainingSession(member_id):
    print("Your booked sessions:")
    getSessions(member_id)
    session_id = input("Enter the session ID to reschedule: ")

    conn = create_connection()
    cursor = conn.cursor()
    try:
        # Fetch both the trainer ID and trainer's name
        cursor.execute("""
            SELECT t.trainer_id, t.first_name, t.last_name 
            FROM training_sessions ts
            JOIN trainers t ON ts.trainer_id = t.trainer_id
            WHERE ts.session_id = %s AND ts.member_id = %s
        """, (session_id, member_id))
        result = cursor.fetchone()
        if result:
            trainer_id, first_name, last_name = result
            trainer_name = f"{first_name} {last_name}"
            print(f"Select a new time slot for Trainer {trainer_name}:")
            viewTrainerAvailability(trainer_id)
            availability_id = input("Select new Availability ID from the available slots: ")
            cursor.execute("SELECT available_date, available_time FROM trainer_availability WHERE availability_id = %s", (availability_id,))
            new_slot = cursor.fetchone()
            if new_slot:
                new_date, new_time = new_slot
                cursor.execute("UPDATE training_sessions SET session_date = %s, session_time = %s WHERE session_id = %s", (new_date, new_time, session_id))
                conn.commit()
                print("Session rescheduled successfully.")
            else:
                print("Invalid selection or no available slots. Returning to menu.")
                return
        else:
            print("No session found with the provided ID for this member. Returning to menu.")
            return
    except Exception as e:
        print(f"Error occurred: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def cancelSession(member_id):
    print("Your booked sessions:")
    sessions = getSessions(member_id)  # Retrieves and prints sessions
    if not sessions:
        print("No sessions to cancel. Returning to menu.")
        return
    session_id = input("Enter the session ID to cancel: ")
    conn = create_connection()
    cursor = conn.cursor()
    try:
        # Verify the session belongs to the member before cancelling
        cursor.execute("SELECT session_id FROM training_sessions WHERE session_id = %s AND member_id = %s", (session_id, member_id))
        session = cursor.fetchone()
        if session:
            cursor.execute("DELETE FROM training_sessions WHERE session_id = %s", (session_id,))
            conn.commit()
            print("Training session cancelled successfully.")
        else:
            print("No session found with that ID for this member. Returning to menu.")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        cursor.close()
        conn.close()

def viewTrainerAvailability(trainer_id=None):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        # The SQL query only fetches future availability for trainers
        query = """
            SELECT ta.availability_id, ta.available_date, ta.available_time
            FROM trainer_availability ta
            WHERE ta.available_date >= %s
        """
        params = (datetime.now().date(),)
        if trainer_id:
            query += " AND ta.trainer_id = %s"
            params += (trainer_id,)
        cursor.execute(query + " ORDER BY ta.available_date, ta.available_time", params)
        availabilities = cursor.fetchall()
        if availabilities:
            for av in availabilities:
                print(f"Availability ID: {av[0]}, Date: {av[1]}, Time: {av[2]}")
        else:
            print("No available slots found.")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        cursor.close()
        conn.close()

def getSessions(member_id):
    conn = create_connection()
    cursor = conn.cursor()
    sessions_found = []
    try:
        today = datetime.now().date()
        cursor.execute("""
            SELECT session_id, trainer_id, session_date, session_time
            FROM training_sessions
            WHERE member_id = %s AND session_date >= %s
            ORDER BY session_date, session_time
        """, (member_id, today))
        sessions = cursor.fetchall()
        if sessions:
            print("Upcoming Training Sessions:")
            for session in sessions:
                print(f"Session ID: {session[0]}, Trainer ID: {session[1]}, Date: {session[2]}, Time: {session[3]}")
            sessions_found = sessions  # Update to return sessions
        else:
            print("No upcoming training sessions found.")
    except Exception as e:
        print(f"Error '{e}' occurred")
    finally:
        cursor.close()
        conn.close()
    return sessions_found

def viewSignedUpClasses(member_id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT c.class_id, c.class_name, c.class_date, c.class_time, r.room_name
            FROM fitness_classes c
            JOIN class_registrations cr ON c.class_id = cr.class_id
            JOIN rooms r ON c.class_room = r.room_id
            WHERE cr.member_id = %s
            ORDER BY c.class_date, c.class_time
        """, (member_id,))
        classes = cursor.fetchall()
        if classes:
            print("Signed Up Classes:")
            for cl in classes:
                print(f"Class ID: {cl[0]}, Name: {cl[1]}, Date: {cl[2]}, Time: {cl[3]}, Room: {cl[4]}")
        else:
            print("No classes found.")
    except Exception as e:
        print(f"Error '{e}' occurred")
    finally:
        cursor.close()
        conn.close()

def signUpForClass(member_id):
    listAllClasses()
    class_id = input("Enter the Class ID to sign up for: ")
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO class_registrations (class_id, member_id) VALUES (%s, %s)", (class_id, member_id))
        conn.commit()
        print("Successfully registered for the class.")
    except Exception as e:
        print(f"Error '{e}' occurred")
    finally:
        cursor.close()
        conn.close()

def leaveClass(member_id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        # Check if the member has signed up for any classes
        cursor.execute("SELECT * FROM class_registrations WHERE member_id = %s", (member_id,))
        registrations = cursor.fetchall()
        if not registrations:
            print("You haven't signed up for any classes.")
            return

        # Display signed up classes and prompt for class ID to leave
        viewSignedUpClasses(member_id)
        class_id = input("Enter the Class ID to leave: ")

        # Remove the member's registration for the selected class
        cursor.execute("DELETE FROM class_registrations WHERE class_id = %s AND member_id = %s", (class_id, member_id))
        conn.commit()
        print("Successfully left the class.")
    except Exception as e:
        print(f"Error '{e}' occurred")
    finally:
        cursor.close()
        conn.close()

def searchClasses(class_name):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT class_id, class_name, class_date, class_time, room_name
            FROM fitness_classes
            JOIN rooms ON fitness_classes.class_room = rooms.room_id
            WHERE lower(class_name) LIKE lower(%s)
            ORDER BY class_date, class_time
        """, (f"%{class_name}%",))
        classes = cursor.fetchall()
        if classes:
            print("Search Results:")
            for cl in classes:
                print(f"Class ID: {cl[0]}, Name: {cl[1]}, Date: {cl[2]}, Time: {cl[3]}, Room: {cl[4]}")
        else:
            print("No classes found matching your search criteria.")
    except Exception as e:
        print(f"Error '{e}' occurred")
    finally:
        cursor.close()
        conn.close()

def listAllClasses():
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT class_id, class_name, class_date, class_time, room_name
            FROM fitness_classes
            JOIN rooms ON fitness_classes.class_room = rooms.room_id
            ORDER BY class_date, class_time
        """)
        classes = cursor.fetchall()
        if classes:
            print("All Available Classes:")
            for cl in classes:
                print(f"Class ID: {cl[0]}, Name: {cl[1]}, Date: {cl[2]}, Time: {cl[3]}, Room: {cl[4]}")
        else:
            print("No classes currently available.")
    except Exception as e:
        print(f"Error '{e}' occurred")
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

def changeEmail(user_type, user_id, new_email):
    if user_type != 'member':
        print("This option is only for members.")
        return
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE members SET email = %s WHERE member_id = %s", (new_email, user_id))
        conn.commit()
        print("Email updated successfully")
    except Exception as e:
        print(f"Error '{e}' occurred")
        return
    finally:
        cursor.close()
        conn.close()