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


####################################  STUDENT FUNCTIONS  ######################################

# 1. View all available jobs
def view_available_jobs():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    # Joining with Companies so they see "Google" not "ID 1"
    query = """
        SELECT j.job_id, c.company_name, j.role_name, j.package_ctc, j.min_cgpa_required 
        FROM Jobs j
        JOIN Companies c ON j.company_id = c.company_id
    """
    cursor.execute(query)
    jobs = cursor.fetchall()
    cursor.close()
    conn.close()
    return jobs

# 2. Apply for a job
def apply_for_job(student_id, job_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = "INSERT INTO Applications (student_id, job_id, apply_date, status) VALUES (%s, %s, CURDATE(), 'Applied')"
        cursor.execute(query, (student_id, job_id))
        conn.commit()
        return "Applied successfully!"
    except Exception as e:
        # This will catch the 'CGPA too low' error from your Trigger!
        return f"Error: {e}"
    finally:
        cursor.close()
        conn.close()

# 3. View my specific applications
def get_my_applications(student_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT j.role_name, c.company_name, a.apply_date, a.status 
        FROM Applications a
        JOIN Jobs j ON a.job_id = j.job_id
        JOIN Companies c ON j.company_id = c.company_id
        WHERE a.student_id = %s
    """
    cursor.execute(query, (student_id,))
    apps = cursor.fetchall()
    cursor.close()
    conn.close()
    return apps


def get_student_offers(student_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT o.offer_id, c.company_name, j.role_name, o.package_ctc, o.joining_date, o.status
        FROM Offers o
        JOIN Jobs j ON o.job_id = j.job_id
        JOIN Companies c ON j.company_id = c.company_id
        WHERE o.student_id = %s
    """
    cursor.execute(query, (student_id,))
    offers = cursor.fetchall()
    cursor.close()
    conn.close()
    return offers


def get_student_interviews(student_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT i.interview_date, i.mode, i.location, j.role_name, c.company_name
        FROM Interviews i
        JOIN Applications a ON i.app_id = a.app_id
        JOIN Jobs j ON a.job_id = j.job_id
        JOIN Companies c ON j.company_id = c.company_id
        WHERE a.student_id = %s
    """
    cursor.execute(query, (student_id,))
    interviews = cursor.fetchall()
    cursor.close()
    conn.close()
    return interviews