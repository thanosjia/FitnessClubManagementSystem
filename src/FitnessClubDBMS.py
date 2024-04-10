import psycopg2
from psycopg2 import OperationalError

def create_connection():
    try:
        conn = psycopg2.connect()
        return conn
    except OperationalError as e:
        print(f"Error '{e}' occured")
        return None

def register_user():
    return None

def login():
    return None

def changeUsername():
    return None

def changePassword():
    return None

def changeInfo():
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

def getStats():
    return None

def newSession():
    return None

def rescheduleSession():
    return None

def cancelSession():
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