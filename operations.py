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