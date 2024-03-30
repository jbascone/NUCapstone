import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from models import KayakReservation
import bookings

def create_filter_window(connection, username):

    bk = bookings.Bookings(connection, username)

    reservations = []

    def apply_filter():
        filter_type = type_dropdown.get()
        print(filter_type)

        if filter_type == "Name":
            reservations = bk.filter_name(username, filter_entry.get())
        elif filter_type == "Date":
            reservations = bk.filter_date(username, filter_entry.get())
        elif filter_type == "Site":
            reservations = bk.filter_tracking(username, filter_entry.get())
        elif filter_type == "Confirmation Code":
            reservations = bk.filter_confirmation(username, filter_entry.get())
        else:
            print("Error in filter types")
        for reservation in reservations:
            print(reservation.username)

    def update_label_text(choice):
        filter_label.configure(text=choice)
            
    root = ctk.CTk()
    root.title("Filter")
    root.geometry("500x400")
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)

    # Create the frame
    frame = ctk.CTkFrame(root, fg_color=root._fg_color)
    frame.grid(row=1, column=0)

    # Create the header label
    header_label = ctk.CTkLabel(root, text= "Filter Reservation")
    header_label.grid(row=0, padx=10, pady=10)

    # Create the filter type label and entry
    type_label = ctk.CTkLabel(frame, text='Filter Type')
    type_label.grid(row=2, column=0, padx=10, pady=10)
    type_dropdown = ctk.CTkComboBox(frame, values=["Name", "Date", "Site", "Confirmation Code"], command=update_label_text)
    type_dropdown.grid(row=2, column=1, padx = 10, pady = 10)

    # Create the filter by label and entry
    filter_label = ctk.CTkLabel(frame, text='Name')
    filter_label.grid(row=3, column=0, padx=10, pady=10)
    filter_entry = ctk.CTkEntry(frame)
    filter_entry.grid(row=3, column=1, padx=10, pady=10)
    
    # Create save and back buttons
    filter_button = ctk.CTkButton(frame, text='Apply Filter', command=lambda: apply_filter())
    filter_button.grid(row=8, column=0, padx=10, pady=10)

    back_button = ctk.CTkButton(frame, text='Back', command=lambda: root.destroy())
    back_button.grid(row=8, column=1, padx=10, pady=10)

    root.mainloop()

#create_filter_window("none", "daniel")