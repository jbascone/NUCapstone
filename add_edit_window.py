import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from models import KayakReservation
import bookings

def create_add_edit_window(connection, username, data):

    def save_changes():
        bk = bookings.Bookings(connection, username)
        duration = 2
        reservation = KayakReservation(code_entry.get(), username, name_entry.get(), date_entry.get(), time_entry.get(), duration, track_entry.get(), rent_entry.get())
        

        if add_edit_flag == "edit":

            bk.delete_reservation_from_database(code_entry.get())
            bk.insert_reservation_to_database(reservation)

            root.quit()
            root.destroy()
            
        else:
            bk.insert_reservation_to_database(reservation)
            
            root.quit()
            root.destroy()
            

    #record management flag
    add_edit_flag = "add"

    root = ctk.CTk()
    root.title("")
    root.geometry("500x400")
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)

    # Create the frame
    frame = ctk.CTkFrame(root, fg_color=root._fg_color)
    frame.grid(row=1, column=0)

    # Create the header label
    header_label = ctk.CTkLabel(root, text= "Add Reservation")
    header_label.grid(row=0, padx=10, pady=10)

    # Create the name label and entry
    name_label = ctk.CTkLabel(frame, text='Name')
    name_label.grid(row=2, column=0, padx=10, pady=10)
    name_entry = ctk.CTkEntry(frame)
    name_entry.grid(row=2, column=1, padx=10, pady=10)
    

    # Create the date label and entry
    date_label = ctk.CTkLabel(frame, text='Date')
    date_label.grid(row=3, column=0, padx=10, pady=10)
    date_entry = ctk.CTkEntry(frame)
    date_entry.grid(row=3, column=1, padx=10, pady=10)
    

    # Create the Time label and entry
    time_label = ctk.CTkLabel(frame, text='Time')
    time_label.grid(row=4, column=0, padx=10, pady=10)
    time_entry = ctk.CTkEntry(frame)
    time_entry.grid(row=4, column=1, padx=10, pady=10)
    

    # Create the Rent label and entry
    rent_label = ctk.CTkLabel(frame, text='Rent')
    rent_label.grid(row=5, column=0, padx=10, pady=10)
    rent_entry = ctk.CTkEntry(frame)
    rent_entry.grid(row=5, column=1, padx=10, pady=10)

    # Create the tracking label and entry
    track_label = ctk.CTkLabel(frame, text='Tracking site')
    track_label.grid(row=6, column=0, padx=10, pady=10)
    track_entry = ctk.CTkComboBox(frame, values = ["Airbnb.com", "Booking.com", "N/A"])
    track_entry.grid(row=6, column=1, padx=10, pady=10)

    
    # Create the code label and entry
    code_label = ctk.CTkLabel(frame, text='Code')
    code_label.grid(row=7, column=0, padx=10, pady=10)
    code_entry = ctk.CTkEntry(frame)
    code_entry.grid(row=7, column=1, padx=10, pady=10)


    # Create save and back buttons
    save_button = ctk.CTkButton(frame, text='Save', command=save_changes)
    save_button.grid(row=8, column=0, padx=10, pady=10)

    back_button = ctk.CTkButton(frame, text='Back', command=lambda: root.destroy())
    back_button.grid(row=8, column=1, padx=10, pady=10)

    if data != None:
        add_edit_flag = "edit"
        header_label.configure(text="Edit reservation")
        name_entry.insert(0, data[2])
        date_entry.insert(0, data[0])
        time_entry.insert(0, data[1])
        rent_entry.insert(0, data[3])
        code_entry.insert(0, data[4])
        code_entry.configure(state='disabled')

    root.mainloop()

#create_add_edit_window("none", "daniel", ["12/31/23",  "09:00:00", "joe dirt", "booking.com", "IJYHTDFG"])