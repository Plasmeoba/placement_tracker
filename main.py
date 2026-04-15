import operations




def student_dashboard(student_id, student_name):
    #Fetching summary of student
    summary = operations.get_login_summary(student_id)

    while True:
        print(f"\n--- STUDENT DASHBOARD (Welcome {student_name}) ---")
        print(f"📊 YOUR STATUS: {summary}") # This shows the current student status
        print("1. View Available Jobs")
        print("2. Apply for a Job")
        print("3. View My Applications")
        print("4. Check Interview Schedules")
        print("5. View My Offers")
        print("6. Logout")
        
        choice = input("Select Option: ")

        if choice == '1':
            jobs = operations.view_available_jobs(student_id)
            if not jobs:
                print("\n✨ You're all caught up! No new jobs match your criteria right now.")
            else:
                print("\nID | Company | Role | Package | Min CGPA")
                print("-" * 55)
                for j in jobs:
                    print(f"{j['job_id']} | {j['company_name']} | {j['role_name']} | {j['package_ctc']} | {j['min_cgpa_required']}")

        elif choice == '2':
            job_id = input("Enter the Job ID you've got your eye on: ")
            result = operations.apply_for_job(student_id, job_id)
            if "Duplicate entry" in result:
                print("⚠️ You've already applied for this role! Check 'View My Applications'.")
            else:
                print(result)

        elif choice == '3':
            apps = operations.get_my_applications(student_id)
            if not apps:
                print("\nYou haven't applied for any jobs yet. Go get 'em!")
            else:
                print("\nRole | Company | Date Applied | Status")
                print("-" * 55)
                for a in apps:
                    print(f"{a['role_name']} | {a['company_name']} | {a['apply_date']} | {a['status']}")

        elif choice == '4':
            interviews = operations.get_student_interviews(student_id)
            if not interviews:
                print("\n📅 No interviews scheduled yet. Keep an eye on your application status!")
            else:
                for i in interviews:
                    print(f"✅ Upcoming: {i['role_name']} at {i['company_name']} on {i['interview_date']} ({i['mode']})")

        elif choice == '5':
            offers = operations.get_student_offers(student_id)
            if not offers:
                print("\n💼 No offers yet—stay persistent, the right one is coming!")
            else:
                for o in offers:
                    print(f"🎉 CONGRATS: {o['role_name']} at {o['company_name']} | CTC: {o['package_ctc']}")

        elif choice == '6':
            print("Logging out... see you next time!")
            break

def admin_dashboard(admin_name):
    while True:
        print(f"\n--- ADMIN MENU (Welcome {admin_name}) ---")
        print("1. View Students")
        print("2. Add Student")
        print("3. Delete Student")
        print("4. View Top Students")
        print("5. Run Eligibility Report")
        print("6. Manage Applications & Schedule Interviews")
        print("7. Logout")

        admin_choice = input("Enter choice: ")

        if admin_choice == '1':
            operations.view_students()

        elif admin_choice == '2':
            print("\n--- Register New Student ---")
            name = input("Name: ")
            email = input("Email: ")
            password = input("Password: ")
            try:
                cgpa = float(input("CGPA: "))
                branch = input("Branch: ")
                operations.add_student(name, email, password, cgpa, branch)
            except ValueError:
                print("❌ Invalid CGPA format. Please use a number (e.g. 8.5).")

        elif admin_choice == '3':
            sid = input("Enter the Student ID to remove: ")
            confirm = input(f"Are you sure you want to delete {sid}? (y/n): ")
            if confirm.lower() == 'y':
                operations.delete_student(sid)
            else:
                print("Action cancelled.")

        elif admin_choice == '4':
            try:
                cgpa = float(input("Find students with CGPA above: "))
                operations.get_top_students(cgpa)
            except ValueError:
                print("❌ Please enter a valid numerical threshold.")

        elif admin_choice == '5':
            try:
                jid = int(input("Enter Job ID for eligibility check: "))
                operations.run_eligibility_report(jid)
            except ValueError:
                print("❌ Job ID must be a number.")

        elif admin_choice == '6':
            print("\n--- Recruitment Pipeline ---")
            apps = operations.view_all_applications()
            
            if not apps:
                print("No pending applications to process.")
                continue
                
            for a in apps:
                print(f"ID: {a['app_id']} | {a['full_name']} -> {a['company_name']} [{a['status']}]")
            
            app_id = input("\nEnter Application ID to manage: ")
            valid_ids = [str(a['app_id']) for a in apps]

            if app_id not in valid_ids:
                print(f"❌ '{app_id}' isn't a valid application ID. Please check the list.")
                continue
            
            print("\nNext Steps:")
            print("1. Schedule Interview")
            print("2. Reject Application")
            print("3. Generate Final Offer")
            sub_choice = input("Select action: ")
            
            if sub_choice == '1':
                print(f"(Current Date: {date.today()})")
                d = input("Interview Date (YYYY-MM-DD): ")
                m = input("Mode (Online/Offline): ")
                l = input("Location/Link: ")
                msg = operations.schedule_interview_process(app_id, d, m, l)
                # Cleaning up the SQL trigger error if it happens
                if "45000" in msg:
                    print("❌ Error: You cannot schedule interviews in the past!")
                else:
                    print(msg)

            elif sub_choice == '2':
                msg = operations.reject_application(app_id)
                print(msg)

            elif sub_choice == '3':
                sid = input("Confirm Student ID: ")
                jid = input("Confirm Job ID: ")
                pkg = input("Final CTC Package: ")
                join_date = input("Joining Date (YYYY-MM-DD): ")
                msg = operations.generate_offer(app_id, sid, jid, pkg, join_date)
                print(msg)


        elif admin_choice == '7':
            print("Admin session ended.")
            break

def main():
    while True:
        print("\n" + "="*30)
        print(" CAMPUS PLACEMENT SYSTEM 2026 ")
        print("="*30)
        print("1. Student Login")
        print("2. Admin Login")
        print("3. Exit System")
        choice = input("Select Option: ")

        if choice == '1':
            email = input("Email: ")
            password = input("Password: ")
            user = operations.login(email, password, "student")

            if user:
                # user[0] = student_id, user[1] = full_name
                student_dashboard(user[0], user[1])
            else:
                print("❌ Invalid email or password. Please try again.")

        elif choice == '2':
            username = input("Username: ")
            password = input("Password: ")
            user = operations.login(username, password, "admin")

            if user:
                print(f"\n✅ Admin Access Verified.")
                
                admin_dashboard(user[1])
            else:
                print("⚠️ Access Denied. Check your admin credentials.")
        
        elif choice == '3':
            print("Shutting down system. Goodbye!")
            break
        else:
            print("Please select a valid option (1-3).")

if __name__ == "__main__":
    main()