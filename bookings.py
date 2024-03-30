from models import KayakReservation

class Bookings: 
    def __init__(self, connection, username):
        self.username = username
        self.connection = connection
        self.cursor = self.connection.cursor

    def view_reservations(self, reservations):
        for idx, reservation in enumerate(reservations, start=1):
            print(f"{idx}. Confirmation: {reservation.confirmation}, Renting: {reservation.rent}, Name: {reservation.name}, Date: {reservation.date}, Time: {reservation.time}, Duration: {reservation.duration} hours, Website: {reservation.tracking}")

    def insert_reservation_to_database(self, reservation):
        self.cursor.execute("""
            INSERT INTO Reservation (confirmation, username, name, date, time, duration, tracking, rent)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, reservation.confirmation, reservation.username, reservation.name, reservation.date, reservation.time, reservation.duration, reservation.tracking, reservation.rent)
        self.connection.commit()
    
    def add_reservation(self, username):
        rent = input("What item(s) would you like to rent?: ")
        name = input("Enter customer name: ")
        date = input("Enter reservation date (YYYY-MM-DD): ")
        time = input("Enter time of reservation (00:00:00): ")
        duration = int(input("Enter reservation duration (in hours): "))
        tracking = input("Enter tracking website: ")

        while True:
            confirmation = input("Enter 8-digit confirmation code (all uppercase): ")
            if len(confirmation) == 8 and confirmation.isupper():
                break  # Code is valid, exit the loop
            else:
                print("Invalid confirmation code. Please enter 8 uppercase digits.")

        reservation = KayakReservation(confirmation, username, name, date, time, duration, tracking, rent)
        self.insert_reservation_to_database(reservation)
        print("\nReservation added successfully!\n")

    def delete_reservation_from_database(self, confirmation):
        self.cursor.execute("DELETE FROM Reservation WHERE confirmation = ?", confirmation)
        self.connection.commit()
    
    def get_all_reservations_from_database(self, username):
        self.cursor.execute("SELECT confirmation, username, name, date, time, duration, tracking, rent FROM Reservation WHERE username = ?", (username,))
        rows = self.cursor.fetchall()
        reservations = [KayakReservation(row.confirmation, row.username, row.name, row.date, row.time, row.duration, row.tracking, row.rent) for row in rows]
        return reservations    
    
    def sort_reservations_date(self, username):
        self.cursor.execute("SELECT * FROM Reservation WHERE username=? ORDER BY date", (username,))
        rows = self.cursor.fetchall()
        reservations = [KayakReservation(*row) for row in rows]
        return reservations
    
    def filter_name(self, username, name):
        query = "SELECT * FROM Reservation WHERE username=?"
        params = [username]

        # Search for matches in both first and last names, using OR conditions
        search_fields = ["name LIKE ?", "name LIKE ?"]
        params.extend(["%" + name + "%", "%" + name + "%"])
        query += " AND (" + " OR ".join(search_fields) + ")"

        self.cursor.execute(query, params)
        rows = self.cursor.fetchall()
        reservation = [KayakReservation(*row) for row in rows]
        return reservation

    def filter_date(self, username, start_date=None):
        if not start_date:
            # No date provided, so no filtering possible
            return []

        query = "SELECT * FROM Reservation WHERE username=? AND date = ?"
        params = [username, start_date]

        self.cursor.execute(query, params)
        rows = self.cursor.fetchall()
        reservation = [KayakReservation(*row) for row in rows]
        return reservation

    def filter_confirmation(self, username, confirmation):
        if not confirmation:
            # No date provided, so no filtering possible
            return []

        query = "SELECT * FROM Reservation WHERE username=? AND confirmation = ?"
        params = [username, confirmation]

        self.cursor.execute(query, params)
        rows = self.cursor.fetchall()
        reservation = [KayakReservation(*row) for row in rows]
        return reservation    

    def filter_tracking(self, username, tracking):
        if not tracking:
            # No date provided, so no filtering possible
            return []

        query = "SELECT * FROM Reservation WHERE username=? AND tracking = ?"
        params = [username, tracking]

        self.cursor.execute(query, params)
        rows = self.cursor.fetchall()
        reservation = [KayakReservation(*row) for row in rows]
        return reservation   

    def edit_reservation(self, username):
        """Allows the user to edit an existing reservation."""

        reservations = self.get_all_reservations_from_database(username)
        self.view_reservations(reservations)

        if reservations:
            while True:
                try:
                    index = int(input("Enter the index of the reservation you want to edit (or 0 to cancel): ")) -1
                    if -1 <= index < len(reservations):
                        break
                    else:
                        print("Invalid index. Please enter a number between 0 and", len(reservations) - 1)
                        print(index)
                except ValueError:
                    print("Invalid input. Please enter a number.")

            if index == -1:
                print("Canceling edit...")
                return

            old_reservation = reservations[index]
            print("Current item(s): ", old_reservation.rent)
            new_rent = input("New item(s): ")
            print("Current name: ", old_reservation.name)
            new_name = input("New name: ")
            print("Current date: ", old_reservation.date)
            new_date = input("New date: ")
            print("Current time: ", old_reservation.time)
            new_time = input("New time: ")
            print("Current duration: ", old_reservation.duration)
            new_duration = input("New duration: ")

            new_reservation = KayakReservation(old_reservation.confirmation, old_reservation.username, new_name, new_date, new_time, new_duration, old_reservation.tracking, new_rent)

            self.update_reservation_in_database(new_reservation)  # Assuming a function for database update
            print("Reservation updated successfully!")
        else:
            print("No reservations found.")

    def update_reservation_in_database(self, new_reservation):
        self.delete_reservation_from_database(new_reservation.confirmation)
        self.insert_reservation_to_database(new_reservation)
