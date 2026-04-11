import operations

def main():
    print("--- WELCOME TO PLACEMENT PORTAL ---")
    print("1. Student Login")
    print("2. Admin Login")
    choice = input("Select Option: ")

    if choice == '1':
        email = input("Email: ")
        password = input("Password: ")
        user = operations.login(email, password, "student")
        if user:
            print(f"\nWelcome, {user[1]}!")
            
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

if __name__ == "__main__":
    main()