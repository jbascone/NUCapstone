from bookings import Bookings
from tracking_sites import Credentials
from pass_reset import Password
import sys
import re

class Menu:
    def __init__(self, connection, username): 
        self.username = username
        self.connection = connection
        self.cursor = self.connection.cursor

    def GUI_login(self):
        data = self.connection
        if data.authenticate_user(username, password):
            print("Login successful!")
            return username  # Break out of both loops and proceed
        else:
            print("Invalid username or password. Please try again.")
        

    def display_menu(self, username):
        while True:    
            print("\n1. View Reservations")
            print("2. Add Reservation")
            print("3  Edit Reservation")
            print("4. Delete Reservation")
            print("5. Manage Tracking Login Credentials")
            print("6. Exit\n")
        
            bookings = Bookings(self.connection, username)
            choice = input("Enter your choice (1-5): ")
            if choice == "1":
                print()
                reservations = bookings.get_all_reservations_from_database(bookings.username)
                bookings.view_reservations(reservations)
                self.filter_reservations(username)
            elif choice == "2":
                bookings.add_reservation(username)
            elif choice == "3":
                bookings.edit_reservation(username)
            elif choice == "4":
                self.delete_reservation_menu(username)
            elif choice == "5":
                self.manage_tracking_credentials()
            elif choice == "6":
                print("Exiting Kayak Reservation System. Goodbye!")
                break
                

    def login_menu(self):
        while True:  # Outer loop for overall login process
            print("\nUser Menu: \n1. Register \n2. Login \n3. Reset Password")
            choice = input("Enter your choice (1-2): ")

            if choice == "1":
                while True:  # Inner loop for registration
                    username = input("Enter your desired username (or 'm' to return): ")
                    if username.lower() == 'm':  # Check for 'm' to return
                        break  # Exit inner loop to go back to main menu

                    password = input("Enter your password (or 'm' to return): ")
                    if password.lower() == 'm':  # Check for 'm' to return
                        break  # Exit inner loop to go back to main menu

                    email = input("Register Email (or 'm' to return): ")
                    if email.lower() == 'm':
                        break

                    # Check for valid email format using regular expression
                    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
                    if not re.match(email_regex, email):
                        print("Invalid email format. Please try again.")
                        continue  # Restart registration loop

                    data = self.connection
                    try:
                        data.register_user(username, password, email)
                        print("User registered successfully!")
                        break  # Successful registration exits inner loop
                    except ValueError as e:  # Handle registration errors
                        print(f"Registration failed: {e}")
            elif choice == "2":
                while True:  # Inner loop for login attempts
                    username = input("Enter your username (or 'm' to return): ")
                    if username.lower() == 'm':  # Check for 'm' to return
                        break  # Exit inner loop to go back to main menu

                    password = input("Enter your password (or 'm' to return): ")
                    if password.lower() == 'm':  # Check for 'm' before authentication
                        break  # Exit inner loop to go back to main menu

                    data = self.connection
                    if data.authenticate_user(username, password):
                        print("Login successful!")
                        return username  # Break out of both loops and proceed
                    else:
                        print("Invalid username or password. Please try again.")
            elif choice == '3':
                password = Password(self.connection)
                password.handle_reset_password_menu()


    
    def manage_tracking_credentials(self):
        while True: 
            print("\n1. View Registered Credentials")
            print("2. Register Credentials")
            print("3. Delete Credentials")
            print("4. Go Back")
            choice = input("Enter your choice (1-4): ")

            if choice == "1":
                print()
                credentials = Credentials.get_all_credentials_from_database(self, self.connection)
                Credentials.view_credentials(self, credentials)

                while True:  # Inner loop to handle "Go Back" option within choice 1
                    back_choice = input("\nEnter 'b' to go back to the menu, or any other key to view credentials again: ")
                    if back_choice.lower() == 'b':
                        break  # Exit the inner loop to return to the main menu
                    else:
                        print()
                        credentials = Credentials.get_all_credentials_from_database(self, self.connection)
                        Credentials.view_credentials(self, credentials)

            elif choice == "2":
                data = self.connection
                data.cursor.execute("SELECT UserID FROM Users WHERE Username = ?", (self.username,))
                userid = data.cursor.fetchone()[0]  # Fetch and assign the ID
                website = input("Website name: ")
                username_track = input("Username: ")
                password_track = input("Password: ")
                url = input("URL to login page: ")
                credentials = Credentials(self.connection, None, userid, username_track, password_track, website, url)
                credentials.insert_credentials_to_database(credentials)
                print("\nCredentials added successfully!")
            
            elif choice == "3":
                while True:
                    print()
                    credentials = Credentials.get_all_credentials_from_database(self, self.connection)
                    Credentials.view_credentials(self, credentials)

                    try:
                        index = int(input(f"\nPlease select: 1 - {len(credentials)} (or 0 to go back): ")) - 1

                        if index == -1:  # User chose to go back
                            break  # Exit the inner loop

                        elif 0 <= index < len(credentials):
                            Credentials.delete_credentials_from_database(self, self.connection, index)
                            break  # Exit the loop after deletion

                        else:
                            print("Invalid number. Please try again.")

                    except ValueError:
                        print("Invalid input. Please enter a valid number.")

            elif choice == "4":
                    break

    def delete_reservation_menu(self, username):
        data = Bookings(self.connection, username)
        reservations = data.get_all_reservations_from_database(username)
        self.view_reservations(reservations)

        while True:  # Loop until valid confirmation code is entered
            confirmation_code = input("Please enter the 8-letter, all-caps confirmation code (or 0 to go back): ").upper()

            if confirmation_code == "0":
                break  # Go back to previous menu

            if len(confirmation_code) == 8 and confirmation_code.isalpha():
                if confirmation_code in [reservation.confirmation for reservation in reservations]:
                    data.delete_reservation_from_database(confirmation_code)
                    print("Reservation deleted successfully!")
                    break  # Exit loop after successful deletion
                else:
                    print("Invalid confirmation code. Please try again.")
            else:
                print("Invalid confirmation code format. Please enter 8 letters, all uppercase.")


    def view_reservations(self, reservations):
        for idx, reservation in enumerate(reservations, start=1):
            print(f"{idx}. Confirmation: {reservation.confirmation}, Name: {reservation.name}, Date: {reservation.date}, Duration: {reservation.duration} hours, Time: {reservation.time}, Website: {reservation.tracking}")

    def filter_reservations(self, username):
        data = Bookings(self.connection, username)
        reservations = data.get_all_reservations_from_database(username)
       
        while True:
            print("\nMenu Options")
            print("1. Filter by name", end=" ")
            print("2. Sort by date", end=" ")
            print("3. Filter by date")
            print("4. Filter by confirmation code", end=" ")
            print("5. FIlter by website", end=" ")
            print("6. Clear filters")
            print("7. Go back to main menu")


            choice = input("Enter your choice (1-5): ")

            if choice == "1":
                name = input("Enter name to filter by (first or last): ")
                instance = Bookings(self, self.username)
                reservations = instance.filter_name(self.username, name)
            elif choice == "2":
                date = input("What date would you like filter (YYYY-MM-DD)?: ")
                reservations = data.filter_date(self.username, date)
            elif choice == "3":
                reservations = data.sort_reservations_date(self.username)
            elif choice == "4":
                confirmation = input("Input conrirmation code: ")
                reservations = data.filter_confirmation(self.username, confirmation)
            elif choice == "5":    
                website = input("Input website: ")
                reservations = data.filter_tracking(self.username, website)
            elif choice == "6":
                reservations = data.get_all_reservations_from_database(username)  # Fetch all reservations again
            elif choice == "7":
                self.display_menu(username)
                data.connection.close()
                sys.exit()
                
    
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")

            if reservations:
                self.view_reservations(reservations)  # Display filtered reservations
            else:
                print("No reservations found matching the filter criteria.")
            
