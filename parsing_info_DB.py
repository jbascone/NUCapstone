from simplegmail import Gmail
from database import Database
from parsing_info import EmailParser
#from tkinter import messagebox
#import tkinter as tk
from plyer import notification

# Create a connection to the database using your Database class

database = Database()
database.connect_to_database()

# Authentication and message fetching
gmail = Gmail(client_secret_file=r'CSC480\client_secret.json')
print("Authentication Successful!")

all_messages = gmail.get_messages()  # Fetches all messages

def create_table_if_not_exists():
    # Create the table if it doesn't exist
    query = """
            IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'booking_info')
            BEGIN
                CREATE TABLE booking_info (
                    ReservationOrigin NVARCHAR(255),
                    CustomerName NVARCHAR(255),
                    EventName NVARCHAR(255),
                    ConfirmationCode NVARCHAR(255),
                    Date NVARCHAR(255),
                    StartTime NVARCHAR(255),
                    EndTime NVARCHAR(255),
                    SeatsBooked NVARCHAR(255),
                    TotalSeats NVARCHAR(255)
                )
            END
            """
    database.cursor.execute(query)
    database.commit()

def insert_into_database(booking_info):
    # Insert data into the database
    query = """
            INSERT INTO booking_info (ReservationOrigin, CustomerName, EventName, ConfirmationCode, Date, StartTime, EndTime, SeatsBooked, TotalSeats)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

    # Execute the SQL query
    database.cursor.execute(query, (
        booking_info["ReservationOrigin"],
        booking_info["CustomerName"],
        booking_info["EventName"],
        booking_info["ConfirmationCode"],
        booking_info["Date"],
        booking_info["StartTime"],
        booking_info["EndTime"],
        booking_info["SeatsBooked"],
        booking_info["TotalSeats"]
    ))


    # Commit the transaction
    database.commit()

def insert_into_reservations_table(booking_info):
    # Insert data into the reservations table in database
    query = """
            INSERT INTO Reservation (confirmation, username, name, date, time, duration, tracking, rent)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
        # Execute the SQL query
    database.cursor.execute(query, (
        booking_info["confirmation"],
        booking_info["username"],
        booking_info["name"],
        booking_info["date"],
        booking_info["time"],
        booking_info["duration"],
        booking_info["tracking"],
        booking_info["rent"]
    ))


    # Commit the transaction
    database.commit()

def output_table():
    # Output the contents of the table
    query = "SELECT * FROM Reservation;"
    database.cursor.execute(query)
    rows = database.cursor.fetchall()

    # Print the results
    for row in rows:
        print(row)

create_table_if_not_exists()

def notify_user(message, table_contents=None):
    # Show a system tray notification
    notification_title = "Booking Received!"
    notification_message = message

    notification.notify(
        title=notification_title,
        message=notification_message,
        timeout=10  # Adjust the timeout as needed
    )

# Define the label name you want to use
label_name = 'ParsedByConsolidate'

try:
    gmail.create_label(label_name)
    print(f"Label '{label_name}' created successfully.")
except Exception as e:
    print(f"Label '{label_name}' already exists or an error occurred: {e}")

def apply_label(message_id, label_name):
    # Apply the label to the email using Gmail API
    try:
        user_info = gmail.service.users().getProfile(userId='me').execute()
        user_email = user_info['emailAddress']
        
        gmail.service.users().messages().modify(
            userId=user_email,  # Use the user's email obtained from user_info
            id=message_id,
            body={'addLabelIds': [label_name]}
        ).execute()
        print(f"Label '{label_name}' applied successfully.")
    except Exception as e:
        print(f"Error applying label '{label_name}': {e}")

labels = gmail.list_labels()
consolidate_label = list(filter(lambda x: x.name == 'ParsedByConsolidate', labels))[0]

# Inside the loop where messages are processed
for message in all_messages:
    # Check if the email contains Airbnb or Kayak booking information
    if "Airbnb" not in message.html and "Kayak" not in message.html:
        print(f"Skipping email without booking information with subject: {message.subject}")
        continue
    
    if consolidate_label in message.label_ids:
        print(f"Skipping already labeled email with subject: {message.subject}")
        continue

    # Apply the label to the email
    message.add_label(consolidate_label)
    
    email_parser = EmailParser(message.html)
    booking_info = email_parser.extract_booking_info_reg_table()
    if booking_info is not None:
        try:
            insert_into_reservations_table(booking_info)

            # Fetch and show the contents of the table for this iteration
            query = "SELECT * FROM Reservation;"
            database.cursor.execute(query)
            rows = database.cursor.fetchall()
            notify_user("You have received a new reservation. Check it out.", table_contents=rows)
        except Exception as e:
            notify_user(f"Error inserting booking information: {str(e)}")

# Output the contents of the table
output_table()

# Close the database connection using the Database class
database.close()
