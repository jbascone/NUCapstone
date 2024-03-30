import hashlib
import smtplib
import random

class Password:
    def __init__(self, connection): 
        self.connection = connection
        self.cursor = self.connection.cursor


    def reset_password(self, username, new_password):
            hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
            self.cursor.execute("""
                UPDATE Users
                SET Password = ?
                WHERE Username = ?
            """, hashed_password, username)
            self.connection.commit()
            print(f"Password for user {username} reset successfully!")

    def handle_reset_password_menu(self):
        while True:  # Loop for username check
            username = input("Enter your username: ")

            sql = "SELECT Username, Email FROM Users WHERE Username = ?"
            self.cursor.execute(sql, (username,))
            user_data = self.cursor.fetchone()

            if user_data:
                break  # Correct username found, exit username loop
            else:
                print("Invalid username. Please try again.")

        registered_email = user_data[1]

        while True:  # Loop for email check
            input_email = input("Input email associated with " + username + ":")

            if input_email == registered_email:
                break  # Correct email entered, exit email loop
            else:
                print(input_email, "is not associated with", username)

        code = self.generate_code()
        self.send_verification_email(input_email, code)

        while True:  # Loop for code check
            code_check = input("Enter code: ")

            if code == code_check:
                break  # Correct code entered, exit code loop
            else:
                print("Code does not match. Please try again.")

        while True:  # Loop for new password check
            new_password = input("Enter new password: ")
            new_password_check = input("Re-enter new password: ")

            if new_password == new_password_check:
                break  # Passwords match, exit password loop
            else:
                print("Passwords do not match. Please try again.")

        self.reset_password(username, new_password)
        print("Password reset successful!")



    def generate_code(self):
        code = random.randint(10000, 99999)
        return str(code)
    
    def send_verification_email(self, recipient_email, code):
        message = f"Subject: Verification Code\n\nYour verification code is: {code}"
        message_bytes = message.encode("utf-8")
        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:  # Replace with your SMTP server
                server.starttls()
                server.login("jakebascone@gmail.com", "lqaf ufsp hthu vzwt")  # Replace with your email credentials
                server.sendmail("jakebascone@gmail.com", recipient_email, message_bytes)
                print("Verification code sent successfully!")
        except Exception as e:
            print("Error sending email:", e)



