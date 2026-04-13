import operations

def student_dashboard(student_id, student_name):
    while True:
        print(f"\n--- STUDENT DASHBOARD (Welcome {student_name}) ---")
        print("1. View Available Jobs")
        print("2. Apply for a Job")
        print("3. View My Applications")
        print("4. Check Interview Schedules")
        print("5. View My Offers")
        print("6. Logout")
        
        choice = input("Select Option: ")

        if choice == '1':
            jobs = operations.view_available_jobs()
            print("\nID | Company | Role | Package | Min CGPA")
            print("-" * 50)
            for j in jobs:
                print(f"{j['job_id']} | {j['company_name']} | {j['role_name']} | {j['package_ctc']} | {j['min_cgpa_required']}")

        elif choice == '2':
            job_id = input("Enter Job ID to apply: ")
            # Note: We pass student_id from the login
            result = operations.apply_for_job(student_id, job_id)
            print(result)

        elif choice == '3':
            apps = operations.get_my_applications(student_id)
            print("\nRole | Company | Date Applied | Status")
            for a in apps:
                print(f"{a['role_name']} | {a['company_name']} | {a['apply_date']} | {a['status']}")

        elif choice == '4':
            interviews = operations.get_student_interviews(student_id)
            for i in interviews:
                print(f"Interview for {i['role_name']} at {i['company_name']}: {i['interview_date']} ({i['mode']})")

        elif choice == '5':
            offers = operations.get_student_offers(student_id)
            for o in offers:
                print(f"OFFER: {o['role_name']} at {o['company_name']} | CTC: {o['package_ctc']} | Status: {o['status']}")

        elif choice == '6':
            print("Logging out...")
            break

def main():
    while True: # Added a loop so the app doesn't close after one login
        print("\n--- WELCOME TO PLACEMENT PORTAL ---")
        print("1. Student Login")
        print("2. Admin Login")
        print("3. Exit")
        choice = input("Select Option: ")

        if choice == '1':
            email = input("Email: ")
            password = input("Password: ")
            user = operations.login(email, password, "student")
            if user:
                # user[0] is student_id, user[1] is full_name
                student_dashboard(user[0], user[1])
            else:
                print("Invalid Credentials!")

        elif choice == '2':
            username = input("Username: ")
            password = input("Password: ")
            user = operations.login(username, password, "admin")
            if user:
                print(f"\nAdmin Access Granted: {user[1]}")
                
            else:
                print("Access Denied!")
        
        elif choice == '3':
            break

if __name__ == "__main__":
    main()