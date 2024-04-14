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

# Member Menus
def memberMenu(member_id):
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
            changeInfoMenu(member_id)
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
        elif user_type == 'member' and choice == '3':
            new_email = input("Enter new email: ")
            changeEmail(user_type, user_id, new_email)
        elif user_type == 'member' and choice == '4':
            break
        elif user_type == 'trainer' or user_type == 'admin' and choice == '3':
            break
        else:
            print("Invalid option, please try again.")

# Trainer Menus
def trainerMenu():
    print("\nFitness Club Trainer Menu")
    print("Please choose an option (enter the number):")
    print("1. View Training Sessions")
    print("2. Change Availability")
    print("3. Search Members")
    print("4. Change Info")
    print("5. Logout")



# Admin Menus
def adminMenu():
    print("\nFitness Club Administrator Menu")
    print("Please choose an option (enter the number):")
    print("1. Room Booking Management")
    print("2. Equipment Maintenance Monitoring")
    print("3. Update Class Schedules")
    print("4. Billing and Payment Processing")
    print("5. Change Info")
    print("6. Logout")

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
                memberMenu(member_id)
                break
            elif userType == 'trainer':
                trainerMenu()
                trainer_choice = input("Selected: ")
                print(f"Trainer option {trainer_choice} was selected")

                if trainer_choice == '5':
                    loggedIn = False
                    userType = None
                    print("Logged out successfully.")
                    break

            elif userType == 'admin':
                adminMenu()
                admin_choice = input("Selected: ")
                print(f"Admin option {admin_choice} was selected")

                if admin_choice == '6':
                    loggedIn = False
                    userType = None
                    print("Logged out successfully.")
                    break
