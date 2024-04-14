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

# Admin Menus
def adminMenu(admin_id):
    user_type = 'admin'
    while True:
        print("\nAdministrator Menu")
        print("1. Room Booking Management")
        print("2. Equipment Maintenance Monitoring")
        print("3. Billing and Payment Processing")
        print("4. Change Info")
        print("5. Logout")

        choice = input("Selected: ")
        if choice == '1':
            roomBookingMenu()
        elif choice == '2':
            equipmentMaintenanceMenu()
        elif choice == '3':
            billingPaymentProcessing()
        elif choice == '4':
            changeInfoMenu(user_type, admin_id)
        elif choice == '5':
            print("Logging out...")
            break
        else:
            print("Invalid option, please try again.")

def roomBookingMenu():
    while True:
        print("\nRoom Booking Management")
        print("1. View All Rooms")
        print("2. View Booked Rooms")
        print("3. Add a New Booking")
        print("4. Reschedule Bookings")
        print("5. Delete a Booking")
        print("6. Return to Main Menu")

        choice = input("Selected: ")
        if choice == '1':
            viewAllRooms()
        elif choice == '2':
            viewBookedRooms()
        elif choice == '3':
            addNewBooking()
        elif choice == '4':
            rescheduleBooking()
        elif choice == '5':
            deleteBooking()
        elif choice == '6':
            break
        else:
            print("Invalid option, please try again.")

def equipmentMaintenanceMenu():
    while True:
        print("\nEquipment Maintenance Monitoring")
        print("1. View All Equipment")
        print("2. View Maintenance Equipment")
        print("3. Change Equipment Status")
        print("4. Return to Main Menu")

        choice = input("Selected: ")
        if choice == '1':
            viewAllEquipment()
        elif choice == '2':
            viewMaintenanceEquipment()
        elif choice == '3':
            changeEquipmentStatus()
        elif choice == '4':
            break
        else:
            print("Invalid option, please try again.")

def billingPaymentProcessing():
    while True:
        print("\nBilling and Payment Processing")
        print("1. Search Members")
        print("2. Process Payment Status")
        print("3. View Member Payments")
        print("4. Return to Main Menu")

        choice = input("Selected: ")
        if choice == '1':
            searchMembers()  # Reuse from Trainer Menu
        elif choice == '2':
            processMemberPayment()
        elif choice == '3':
            viewAllPayments()
        elif choice == '4':
            break
        else:
            print("Invalid option, please try again.")

def viewAllRooms():
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT room_id, room_name, room_capacity FROM rooms")
        rooms = cursor.fetchall()
        if rooms:
            print("Available Rooms:")
            for room in rooms:
                print(f"Room ID: {room[0]}, Name: {room[1]}, Capacity: {room[2]}")
        else:
            print("No rooms available.")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        cursor.close()
        conn.close()

def viewBookedRooms():
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        SELECT fc.class_id, fc.class_name, fc.class_date, fc.class_time, r.room_name
        FROM fitness_classes fc
        JOIN rooms r ON fc.class_room = r.room_id
        ORDER BY fc.class_date, fc.class_time
        """)
        classes = cursor.fetchall()
        if classes:
            print("Booked Rooms:")
            for cl in classes:
                print(f"Class ID: {cl[0]}, Class Name: {cl[1]}, Date: {cl[2]}, Time: {cl[3]}, Room: {cl[4]}")
        else:
            print("No bookings found.")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        cursor.close()
        conn.close()

def addNewBooking():
    class_name = input("Enter class name: ")
    room_id = input("Enter room ID: ")
    class_date = input("Enter date (YYYY-MM-DD): ")
    class_time = input("Enter time (HH:MM): ")
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        INSERT INTO fitness_classes (class_name, class_room, class_date, class_time)
        VALUES (%s, %s, %s, %s)
        """, (class_name, room_id, class_date, class_time))
        conn.commit()
        print("Booking added successfully")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        cursor.close()
        conn.close()

def rescheduleBooking():
    class_id = input("Enter the class ID to reschedule: ")
    new_date = input("Enter new date (YYYY-MM-DD): ")
    new_time = input("Enter new time (HH:MM): ")
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        UPDATE fitness_classes SET class_date = %s, class_time = %s WHERE class_id = %s
        """, (new_date, new_time, class_id))
        conn.commit()
        print("Booking rescheduled successfully")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        cursor.close()
        conn.close()

def deleteBooking():
    class_id = input("Enter the class ID to delete: ")
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM fitness_classes WHERE class_id = %s", (class_id,))
        conn.commit()
        print("Booking deleted successfully")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        cursor.close()
        conn.close()

def viewAllEquipment():
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT equipment_id, equipment_name, maintenance_status FROM equipment")
        equipment = cursor.fetchall()
        if equipment:
            print("All Equipment:")
            for eq in equipment:
                status = "Under Maintenance" if eq[2] else "Not Under Maintenance"
                print(f"Equipment ID: {eq[0]}, Name: {eq[1]}, Status: {status}")
        else:
            print("No equipment found.")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        cursor.close()
        conn.close()

def viewMaintenanceEquipment():
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT equipment_id, equipment_name, maintenance_status FROM equipment WHERE maintenance_status = TRUE")
        equipment = cursor.fetchall()
        if equipment:
            print("Equipment Under Maintenance:")
            for eq in equipment:
                print(f"Equipment ID: {eq[0]}, Name: {eq[1]}, Status: 'Under Maintenance'")
        else:
            print("No equipment under maintenance.")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        cursor.close()
        conn.close()

def changeEquipmentStatus():
    equipment_id = input("Enter the equipment ID to change status: ")
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT maintenance_status FROM equipment WHERE equipment_id = %s", (equipment_id,))
        status = cursor.fetchone()
        if status:
            new_status = not status[0]  # Toggle the boolean value
            cursor.execute("UPDATE equipment SET maintenance_status = %s WHERE equipment_id = %s", (new_status, equipment_id))
            conn.commit()
            status_text = "Under Maintenance" if new_status else "Not Under Maintenance"
            print(f"Equipment status changed to {status_text}")
        else:
            print("Equipment not found.")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        cursor.close()
        conn.close()

def processMemberPayment():
    member_id = input("Enter the member ID to process payment: ")
    conn = create_connection()
    cursor = conn.cursor()
    
    try:
        # Check if the member exists
        cursor.execute("SELECT membership_status FROM members WHERE member_id = %s", (member_id,))
        member = cursor.fetchone()
        
        if not member:
            print("No member found with ID", member_id)
            return  # Exit the function if no member found

        # Proceed if member exists
        payment_method = input("Enter payment method: ")
        today = datetime.now().date()
        next_payment_date = today + timedelta(days=30)
        
        # Update member status to active
        cursor.execute("UPDATE members SET membership_status = TRUE WHERE member_id = %s", (member_id,))
        
        # Insert new payment record
        cursor.execute("""
        INSERT INTO payments (member_id, payment_method, payment_date, next_payment_date)
        VALUES (%s, %s, %s, %s)
        """, (member_id, payment_method, today, next_payment_date))
        conn.commit()
        print("Payment processed and membership activated.")
        
    except Exception as e:
        print(f"Error occurred: {e}")
        conn.rollback()  # Ensure you rollback in case of any error
    finally:
        cursor.close()
        conn.close()

def viewAllPayments():
    member_id = input("Enter the member ID to view payments: ")
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT payment_id, payment_date, next_payment_date, payment_method FROM payments WHERE member_id = %s", (member_id,))
        payments = cursor.fetchall()
        if payments:
            print("Payments for Member ID", member_id)
            for payment in payments:
                print(f"Payment ID: {payment[0]}, Date: {payment[1]}, Next Payment: {payment[2]}, Method: {payment[3]}")
        else:
            print("No payments found for this member.")
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
        SELECT member_id, first_name, last_name, user_name, email, membership_status
        FROM members
        WHERE user_name ILIKE %s OR first_name ILIKE %s OR last_name ILIKE %s
        """, (f'%{search_query}%', f'%{search_query}%', f'%{search_query}%'))
        members = cursor.fetchall()
        print("Search Results:")
        for member in members:
            print(f"Member ID: {member[0]}, Name: {member[1]} {member[2]}, Username: {member[3]}, Email: {member[4]}, Status: {'Active' if member[5] else 'Inactive'}")
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