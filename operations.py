from db_config import get_connection


################################ AUTHENTICATION FUNCTION #############################





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
def view_available_jobs(student_id): # Add student_id as parameter
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    # This query joins Jobs with Companies 
    # and filters by comparing the student's CGPA to the job's requirement
    query = """
        SELECT j.job_id, c.company_name, j.role_name, j.package_ctc, j.min_cgpa_required 
        FROM Jobs j
        JOIN Companies c ON j.company_id = c.company_id
        WHERE j.min_cgpa_required <= (SELECT cgpa FROM Students WHERE student_id = %s)
    """
    
    cursor.execute(query, (student_id,))
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


def get_login_summary(student_id):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        # Calling the MySQL function
        query = "SELECT GetStudentStatusSummary(%s)"
        cursor.execute(query, (student_id,))
        summary = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return summary
    return "No data available"



####################################  ADMIN FUNCTIONS  ######################################



def view_students():
    conn = get_connection()
    if conn:
        # dictionary=True makes it easy for Streamlit to read headers
        cursor = conn.cursor(dictionary=True) 
        cursor.execute("SELECT student_id, full_name, cgpa, branch FROM Students")
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results # Send the list back to app.py
    return []





def add_student(name, email, password, cgpa, branch):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        query = "INSERT INTO Students (full_name, email, password, cgpa, branch) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (name, email, password, cgpa, branch))
        conn.commit()
        cursor.close()
        conn.close()

def delete_student(student_id):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        query = "DELETE FROM Students WHERE student_id = %s"
        cursor.execute(query, (student_id,))
        conn.commit()
        cursor.close()
        conn.close()


# 🔹 Stored Procedure Call
# Updated Top Students Function
def get_top_students(min_cgpa):
    conn = get_connection()
    students_list = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.callproc('GetTopStudents', [min_cgpa])
            for result in cursor.stored_results():
                students_list = result.fetchall()
        except Exception as e:
            print("Error:", e)
        finally:
            cursor.close()
            conn.close()
    return students_list

# Updated Eligibility Report Function
def run_eligibility_report(job_id):
    conn = get_connection()
    eligible_list = []
    if conn:
        cursor = conn.cursor() # Keep as standard cursor for simpler indexing
        try:
            cursor.callproc('GetEligibleStudents', [job_id])
            for result in cursor.stored_results():
                rows = result.fetchall()
                for row in rows:
                    eligible_list.append(row[0]) # Just getting the names
        except Exception as e:
            print("Error:", e)
        finally:
            cursor.close()
            conn.close()
    return eligible_list



# 🔹 View ALL applications (So the Admin knows who to shortlist/schedule)
def view_all_applications():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT a.app_id, s.full_name, c.company_name, j.role_name, a.status 
        FROM Applications a
        JOIN Students s ON a.student_id = s.student_id
        JOIN Jobs j ON a.job_id = j.job_id
        JOIN Companies c ON j.company_id = c.company_id
    """
    cursor.execute(query)
    apps = cursor.fetchall()
    cursor.close()
    conn.close()
    return apps

# 🔹 Update status (Shortlisted/Rejected) and Schedule Interview
def schedule_interview_process(app_id, date, mode, location):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        try:
            # 1. First, update the application status to 'Scheduled'
            update_query = "UPDATE Applications SET status = 'Scheduled' WHERE app_id = %s"
            cursor.execute(update_query, (app_id,))
            
            # 2. Then, insert the record into the Interviews table
            interview_query = """
                INSERT INTO Interviews (app_id, interview_date, mode, location)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(interview_query, (app_id, date, mode, location))
            
            conn.commit()
            return "✅ Status updated and Interview scheduled!"
        except Exception as e:
            conn.rollback()
            return f"❌ Error: {e}"
        finally:
            cursor.close()
            conn.close()



# 🔹 Admin selects student and generates an offer
def generate_offer(app_id, student_id, job_id, package, joining_date):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        try:
            # 1. Update Application status to 'Selected'
            cursor.execute("UPDATE Applications SET status = 'Selected' WHERE app_id = %s", (app_id,))
            
            # 2. Insert into Offers table
            query = """
                INSERT INTO Offers (student_id, job_id, package_ctc, joining_date, status)
                VALUES (%s, %s, %s, %s, 'Offered')
            """
            cursor.execute(query, (student_id, job_id, package, joining_date))
            
            conn.commit()
            return "🎉 Offer generated and student selected!"
        except Exception as e:
            conn.rollback()
            return f"❌ Error: {e}"
        finally:
            cursor.close()
            conn.close()


def reject_application(app_id):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        try:
            query = "UPDATE Applications SET status = 'Rejected' WHERE app_id = %s"
            cursor.execute(query, (app_id,))
            conn.commit()
            return "🗑️ Application has been moved to Rejected status."
        except Exception as e:
            return f"❌ Error: {e}"
        finally:
            cursor.close()
            conn.close()