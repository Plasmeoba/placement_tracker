import operations

def main_menu():
    while True:
        print("\n=== STUDENT PLACEMENT TRACKER ===")
        print("1. View Students")
        print("2. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            operations.view_students()
        elif choice == '2':
            print("Exiting...")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main_menu()