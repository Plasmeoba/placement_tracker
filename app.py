import streamlit as st
import operations
from datetime import date

# 1. Page Configuration
st.set_page_config(page_title="Placement Portal 2026", page_icon="🎓", layout="wide")

# 2. Session State Initialization (The "Memory" of your app)
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_role = None  # 'student' or 'admin'
    st.session_state.user_id = None
    st.session_state.user_name = None

# --- LOGIN PAGE ---
if not st.session_state.logged_in:
    st.title("🚀 Campus Placement Portal 2026")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔑 Student Login")
        s_email = st.text_input("Student Email", key="s_email")
        s_pass = st.text_input("Student Password", type="password", key="s_pass")
        if st.button("Login as Student"):
            user = operations.login(s_email, s_pass, "student")
            if user:
                st.session_state.logged_in = True
                st.session_state.user_role = 'student'
                st.session_state.user_id = user[0]
                st.session_state.user_name = user[1]
                st.rerun()
            else:
                st.error("Invalid Student Credentials")

    with col2:
        st.subheader("🛠️ Admin Login")
        a_user = st.text_input("Username", key="a_user")
        a_pass = st.text_input("Admin Password", type="password", key="a_pass")
        if st.button("Login as Admin"):
            user = operations.login(a_user, a_pass, "admin")
            if user:
                st.session_state.logged_in = True
                st.session_state.user_role = 'admin'
                st.session_state.user_name = user[1]
                st.rerun()
            else:
                st.error("Access Denied")

# --- AUTHORIZED AREA ---
else:
    # Sidebar for Navigation & Logout
    st.sidebar.title(f"Welcome, {st.session_state.user_name}")
    st.sidebar.write(f"Role: {st.session_state.user_role.capitalize()}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # STUDENT DASHBOARD
    if st.session_state.user_role == 'student':
        st.title("👨‍🎓 Student Dashboard")
        
        # Real-time Status Bar (Calls your MySQL Function)
        summary = operations.get_login_summary(st.session_state.user_id)
        st.info(f"📊 Current Status: {summary}")

        tab1, tab2, tab3, tab4 = st.tabs(["🔍 Browse Jobs", "📝 My Applications", "📅 Interviews", "🎉 Offers"])

        with tab1:
            st.subheader("Eligible Jobs")
            jobs = operations.view_available_jobs(st.session_state.user_id)
            if jobs:
                st.dataframe(jobs, use_container_width=True)
                st.divider()
                # Use a dropdown so they can't type a wrong ID
                job_list = [j['job_id'] for j in jobs]
                selected_job = st.selectbox("Select a Job ID to apply:", job_list)
                if st.button("Submit Application"):
                    res = operations.apply_for_job(st.session_state.user_id, selected_job)
                    if "Error" in res:
                        st.error(res)
                    else:
                        st.success("Application Sent Successfully!")
                        st.balloons()
            else:
                st.warning("No jobs currently match your CGPA.")

        with tab2:
            st.subheader("Application History")
            my_apps = operations.get_my_applications(st.session_state.user_id)
            if my_apps:
                st.table(my_apps)
            else:
                st.write("You haven't applied to any roles yet.")

        with tab3:
            st.subheader("Your Schedule")
            interviews = operations.get_student_interviews(st.session_state.user_id)
            if interviews:
                for i in interviews:
                    st.warning(f"**{i['role_name']}** at {i['company_name']} \n\n 📅 {i['interview_date']} | 📍 {i['mode']} ({i['location']})")
            else:
                st.write("No upcoming interviews.")

        with tab4:
            st.subheader("Offers Received")
            offers = operations.get_student_offers(st.session_state.user_id)
            if offers:
                for o in offers:
                    st.success(f"🎊 **Offer from {o['company_name']}** for **{o['role_name']}**! Package: {o['package_ctc']} LPA")
            else:
                st.write("No offers yet. Stay persistent!")

    # ADMIN DASHBOARD
    elif st.session_state.user_role == 'admin':
        st.title("⚙️ Admin Management Portal")
        
        menu = ["View Students", "Account Management", "Manage Applications", "Reports"]
        choice = st.sidebar.selectbox("Admin Menu", menu)

        if choice == "View Students":
            st.subheader("👥 Registered Students")
            # Automatically fetch and show the table
            student_data = operations.view_students()
            if student_data:
                st.dataframe(student_data, use_container_width=True)
            else:
                st.write("No students registered yet.")


        elif choice == "Account Management":
            tab1, tab2 = st.tabs(["➕ Add New Student", "🗑️ Delete Student"])
            
            with tab1:
                st.subheader("Register a New Student")
                # Using a form so the page doesn't refresh after every single letter you type
                with st.form("add_student_form", clear_on_submit=True):
                    name = st.text_input("Full Name")
                    email = st.text_input("Email Address")
                    pwd = st.text_input("Password", type="password")
                    col1, col2 = st.columns(2)
                    with col1:
                        cgpa = st.number_input("Current CGPA", min_value=0.0, max_value=10.0, step=0.01)
                    with col2:
                        branch = st.selectbox("Branch", ["CS", "IT", "ENTC", "Mechanical", "Civil"])
                    
                    submit = st.form_submit_state = st.form_submit_button("Add Student to Database")
                    
                    if submit:
                        if name and email and pwd:
                            operations.add_student(name, email, pwd, cgpa, branch)
                            st.success(f"Successfully added {name}!")
                        else:
                            st.error("Please fill in all fields.")

            with tab2:
                st.subheader("Remove Student Record")
                sid_to_delete = st.text_input("Enter Student ID to delete (e.g., S101)")
                
                # Popover for a safe delete confirmation
                with st.popover("Confirm Deletion"):
                    st.warning(f"Are you sure you want to permanently delete {sid_to_delete}?")
                    if st.button("Yes, Delete Forever"):
                        operations.delete_student(sid_to_delete)
                        st.success(f"Record {sid_to_delete} removed.")

        elif choice == "Manage Applications":
            st.subheader("Pipeline Management")
            apps = operations.view_all_applications()
            if apps:
                st.dataframe(apps, use_container_width=True)
                
                st.divider()
                app_id = st.number_input("Enter Application ID to process", step=1, min_value=1)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    # Using a popover keeps the fields open until the 'Confirm' button inside is clicked
                    with st.popover("📅 Schedule Interview"):
                        st.write(f"Scheduling for App ID: {app_id}")
                        d = st.date_input("Select Date", min_value=date.today())
                        m = st.selectbox("Interview Mode", ["Online", "Offline"])
                        l = st.text_input("Location/Link")
                        
                        if st.button("Confirm Schedule", key="conf_int"):
                            msg = operations.schedule_interview_process(app_id, str(d), m, l)
                            if "Error" in msg:
                                st.error(msg)
                            else:
                                st.success(msg)
                                st.balloons()

                with col2:
                    if st.button("❌ Reject Application", use_container_width=True):
                        msg = operations.reject_application(app_id)
                        st.info(msg)

                with col3:
                    with st.popover("🎓 Generate Offer"):
                        st.write("Finalizing Selection")
                        sid = st.text_input("Confirm Student ID (e.g. S101)")
                        jid = st.text_input("Confirm Job ID")
                        pkg = st.text_input("Final CTC (LPA)")
                        
                        if st.button("Send Official Offer", key="conf_off"):
                            msg = operations.generate_offer(app_id, sid, jid, pkg, str(date.today()))
                            st.success(msg)
                            st.snow() # Festive effect for an offer!
            else:
                st.write("No applications to show.")

        elif choice == "Reports":
            st.subheader("📊 Advanced Analytics")
            
            # Report 1: Top Students (Using Stored Procedure)
            st.markdown("### Top Students by CGPA")
            threshold = st.slider("Select Minimum CGPA Threshold", 0.0, 10.0, 8.0)
            if st.button("Generate Top Student List"):
                top_data = operations.get_top_students(threshold)
                if top_data:
                    st.success(f"Found {len(top_data)} students above {threshold} CGPA")
                    st.dataframe(top_data, use_container_width=True)
                else:
                    st.warning("No students meet this threshold.")

            st.divider()

            # Report 2: Job Eligibility (Using the other Stored Procedure)
            st.markdown("### Job Eligibility Check")
            jid = st.number_input("Enter Job ID to check eligibility", min_value=1, step=1)
            if st.button("Run Eligibility Report"):
                eligible_names = operations.run_eligibility_report(jid)
                if eligible_names:
                    st.success(f"The following students are eligible for Job ID {jid}:")
                    for name in eligible_names:
                        st.write(f"✅ {name}")
                else:
                    st.error("No eligible students found for this Job ID.")