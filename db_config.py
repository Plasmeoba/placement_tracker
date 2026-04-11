import mysql.connector

def get_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='password', # ENTER YOUR WORKBENCH PASSWORD HERE
            database='placement_tracker' # MUST MATCH WORKBENCH EXACTLY
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None