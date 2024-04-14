import psycopg2
from psycopg2 import OperationalError

def create_connection():
    try:
        connection = psycopg2.connect(
            dbname="FitnessClub",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        return connection
    except OperationalError as e:
        print(f"An error occurred: {e}")
        return None

def execute_sql_from_file(filename):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        with open(filename, 'r') as sql_file:
            sql_script = sql_file.read()
        for command in sql_script.split(';'):
            if command.strip():
                cursor.execute(command)
        conn.commit()
        print(f"SQL from {filename} executed successfully.")
    except Exception as e:
        print(f"Failed to execute SQL from {filename}: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    execute_sql_from_file('../SQL/ddl.sql')
    execute_sql_from_file('../SQL/dml.sql')
