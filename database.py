import pyodbc
import hashlib

class Database:
    def __init__(self):
        self.connection_string = (
            "DRIVER={SQL Server};SERVER=MSI;DATABASE=reservations"
        )
        self.connection = None
        self.cursor = None

    def connect_to_database(self):
        self.connection = pyodbc.connect(self.connection_string)
        self.cursor = self.connection.cursor()
        
        try:
            # Execute a test query to check the connection
            self.cursor.execute("SELECT 1")
            result = self.cursor.fetchone()
            if result and result[0] == 1:
                print("Database connection established successfully.")
            else:
                print("Failed to establish a connection to the database.")
        except pyodbc.OperationalError as e:
            print(f"OperationalError connecting to the database: {e}")
            raise

    def register_user(self, username, password, email):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.cursor.execute("""
            INSERT INTO Users (Username, Password, Email)
            VALUES (?, ?, ?)
        """, username, hashed_password, email)
        self.connection.commit()
        print(f"User {username} registered successfully!")

    def authenticate_user(self, username, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.cursor.execute("""
            SELECT UserID FROM Users
            WHERE Username = ? AND Password = ?
        """, username, hashed_password)
        result = self.cursor.fetchone()
        return result is not None     

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()
        print("Connection closed")