from db_config import get_connection

def view_students():
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT student_id, full_name, cgpa, branch FROM Students")
        results = cursor.fetchall()
        
        print("\n--- Student List ---")
        for row in results:
            print(f"ID: {row[0]} | Name: {row[1]} | CGPA: {row[2]} | Branch: {row[3]}")
            
        cursor.close()
        conn.close()


def login(email_or_user, password, role):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        if role == "student":
            query = "SELECT student_id, full_name FROM Students WHERE email = %s AND password = %s"
        else:
            # Check if these column names match your Workbench table exactly!
            query = "SELECT admin_id, username FROM Admins WHERE username = %s AND password = %s"
            
        cursor.execute(query, (email_or_user, password))
        user = cursor.fetchone()
        
        # DEBUG: Remove this after it works
        print(f"DEBUG: Found user: {user}") 
        
        cursor.close()
        conn.close()
        return user 
    return None