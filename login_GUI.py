#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      Daniel
#
# Created:     27/01/2024
# Copyright:   (c) Daniel 2024
# Licence:     <your licence>
#-------------------------------------------------------------------------------

# Import modules
from tkinter import *
import customtkinter as ctk
from PIL import Image

from database import Database
import GUI


#define reservations array
reservations = []

# Define functions
def get_key_press(event):
    if event.keysym=='Return':
        validate_username_password()

def validate_username_password():
    # Get the input from the entry widgets

    username = username_entry.get()

    if username == "":
        msg_label.configure(text="Error! No username entered!")
        msg_label.update()
        login_frame.update_idletasks()
        return

    password = password_entry.get()

    if password == "":
        msg_label.configure(text="Error! No password entered!")
        msg_label.update()
        login_frame.update_idletasks()
        return

    
    if Database.authenticate_user(username, password):

        login_frame.pack_forget()
        login_frame.grid_forget()
        window.destroy()
        GUI.create_reservation_screen(Database, username)
    else:
        print("Fail")
        msg_label.configure(text="Error! nvalid username or password!")



    # Return True to allow the focus change
    return True

def change_frame(top_frame):
    if top_frame == "login":
        login_frame.grid_forget()
        registration_frame.grid(row = 1, column = 0)
    else:
        registration_frame.grid_forget()
        login_frame.grid(row = 1, column = 0)

def register_user():

    username = reg_username_entry.get()
    password = reg_password_entry.get()
    email = reg_email_entry.get()

    """if username or password or email is None:
        print("Error! Something is empty!")
        print("username: " + username)
        print("password: " + password)
        print("email: " + email)
        return"""

    if username == "":
        print("error: no username entered")

    Database.register_user(username, password, email)



# Create the main window

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

window = ctk.CTk()
window.title('Consolidate')
window.geometry('500x400')
window.grid_columnconfigure(index=0, weight= 2)

#------------------main login frame--------------------------------------------------------------------------------------------

# add the image
image = ctk.CTkImage(dark_image=Image.open('CSC480\Consolidate.png'), size=(300, 100))
image_label = ctk.CTkLabel(window, image=image, text="")
image_label.grid(row=0, column = 0, columnspan = 2)


# Create the login frame
login_frame = ctk.CTkFrame(window, fg_color=window._fg_color)

# Create the email label and entry
username_label = ctk.CTkLabel(login_frame, text='Username:')
username_label.grid(row=0, column=0, padx=10, pady=10)
username_entry = ctk.CTkEntry(login_frame)
username_entry.grid(row=0, column=1, padx=10, pady=10)

# Create the password label and entry
password_label = ctk.CTkLabel(login_frame, text='Password:')
password_label.grid(row=1, column=0, padx=10, pady=10)
password_entry = ctk.CTkEntry(login_frame, show='*')
password_entry.grid(row=1, column=1, padx=10, pady=10)

#create hidden label
hid_label = ctk.CTkLabel(login_frame, text="")
hid_label.grid(row=2, column=1, padx=10, pady=10)

# Create the login button
login_button = ctk.CTkButton(login_frame, text='Login', command=validate_username_password)
login_button.grid(row=3, column=1, padx=10, pady=10)

# create registration button
registration_button = ctk.CTkButton(login_frame, text='Register', command= lambda: change_frame("login"))
registration_button.grid(row=4, column=1, padx=10, pady=10)

#create message label
msg_label = ctk.CTkLabel(login_frame, text="", text_color='red')
msg_label.grid(row=5, column=1, padx=10, pady=10)

# create forgot password button

login_frame.grid(row = 1, column = 0)

#-----------regestration frame--------------------------------------------------------------

registration_frame = ctk.CTkFrame(window, fg_color=window._fg_color)

# Create the email label and entry
reg_username_label = ctk.CTkLabel(registration_frame, text='Username:')
reg_username_label.grid(row=0, column=0, padx=10, pady=10)
reg_username_entry = ctk.CTkEntry(registration_frame)
reg_username_entry.grid(row=0, column=1, padx=10, pady=10)

# Create the password label and entry
reg_password_label = ctk.CTkLabel(registration_frame, text='Password:')
reg_password_label.grid(row=1, column=0, padx=10, pady=10)
reg_password_entry = ctk.CTkEntry(registration_frame, show='*')
reg_password_entry.grid(row=1, column=1, padx=10, pady=10)

# Create the email label and entry
reg_email_label = ctk.CTkLabel(registration_frame, text='Email:')
reg_email_label.grid(row=2, column=0, padx=10, pady=10)
reg_email_entry = ctk.CTkEntry(registration_frame)
reg_email_entry.grid(row=2, column=1, padx=10, pady=10)

# Create the registration button to send reg info to database
reg_registration_button = ctk.CTkButton(registration_frame, text='Register', command= lambda: register_user())
reg_registration_button.grid(row=3, column=1, padx=10, pady=10)

# Create the back button
reg_back_button = ctk.CTkButton(registration_frame, text='back', command= lambda: change_frame("back"))
reg_back_button.grid(row=4, column=1, padx=10, pady=10)



Database = Database()
Database.connect_to_database()


# Start the main loop
window.bind("<KeyRelease>", get_key_press)
window.mainloop()
