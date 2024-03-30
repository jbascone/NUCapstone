from tkinter import messagebox
import customtkinter as ctk
import bookings as bk
import menu as menu
import add_edit_window as aew


def create_reservation_screen(connection, username):
   
    def get_reservation_info(connection, username):

        if connection == "debug":
            return

        bookings = bk.Bookings(connection, username)
        reservations = bookings.get_all_reservations_from_database(bookings.username)

        if len(reservations) == 0:
            print("no reservations found. Breaking")
            destroy_children()
            return
        
        print(reservations[0].username)
        reservation_data = update_reservation_data(reservations)
        destroy_children()
        update_data_labels(reservation_data)
        scroll_frame.update_idletasks()
        print("button clicked")

    def update_reservation_data(reservations):
        reservation_data = []
        for reservation in reservations:
            temp_list = []
            temp_list.append(reservation.date)
            temp_list.append(reservation.time)
            temp_list.append(reservation.name)
            temp_list.append(reservation.tracking)
            temp_list.append(reservation.confirmation)
            reservation_data.append(temp_list)
        return reservation_data
        
    def update_data_labels(reservation_data):
        for row, data in enumerate(reservation_data):
            for col, value in enumerate(data):
                label_data = ctk.CTkLabel(scroll_frame, text=value, width=20, wraplength=75)
                label_data.grid(row=row + 1, column=col, padx=10, pady=5)
            visit_button = ctk.CTkButton(scroll_frame, text = "Visit", width = 75, command= lambda i = data: 
                                print(i))
            edit_button = ctk.CTkButton(scroll_frame, text = "Edit", width = 75, command= lambda i = data: 
                                edit_reservation(i))
            delete_button = ctk.CTkButton(scroll_frame, text = "Delete", width = 75, command= lambda i = data: 
                                delete_reservation(i))
            print("Button created for row " + str(row))
            visit_button.grid(row=row+1, column = 5, padx= 1, pady= 1)
            edit_button.grid(row=row+1, column = 7, padx= 1, pady= 1)
            delete_button.grid(row=row+1, column = 9, padx= 1, pady= 1)


    def destroy_children():
         for widget in scroll_frame.winfo_children():
              widget.destroy()
         scroll_frame.pack_forget()
         print("Children destroyed")

    def create_header_labels():


        date_label = ctk.CTkLabel(header_frame, text="Date", width=20, font=header_font)
        date_label.grid(row=0, column=0, padx=[17, 13], pady=5)

        time_label = ctk.CTkLabel(header_frame, text="Time", width=20, font=header_font)
        time_label.grid(row=0, column=1, padx=[18, 12], pady=5)

        name_label = ctk.CTkLabel(header_frame, text="Name", width=20, font=header_font)
        name_label.grid(row=0, column=2, padx=[16, 14], pady=5)

        renting_label = ctk.CTkLabel(header_frame, text="Renting", width=20, font=header_font)
        renting_label.grid(row=0, column=3, padx=15, pady=5)

        code_label = ctk.CTkLabel(header_frame, text="Code", width=20, font=header_font)
        code_label.grid(row=0, column=4, padx=15, pady=5)

        ex_width = 75

        ex_label_1 = ctk.CTkLabel(header_frame, text=" ", width=ex_width)
        ex_label_1.grid(row=0, column=5, padx=1, pady=5)
        ex_label_2 = ctk.CTkLabel(header_frame, text=" ", width=ex_width)
        ex_label_2.grid(row=0, column=6, padx=1, pady=5)
        ex_label_3 = ctk.CTkLabel(header_frame, text=" ", width=ex_width)
        ex_label_3.grid(row=0, column=7, padx=1, pady=5)


    def apply_filter():
        filter_type = type_dropdown.get()

        bookings = bk.Bookings(connection, username)

        if filter_type == "Name":
            reservation_data = bookings.filter_name(username, filter_entry.get())
        elif filter_type == "Date":
            reservation_data = bookings.filter_date(username, filter_entry.get())
        elif filter_type == "Site":
            reservation_data = bookings.filter_tracking(username, filter_entry.get())
        elif filter_type == "Confirmation Code":
            reservation_data = bookings.filter_confirmation(username, filter_entry.get())
        else:
            print("Error in filter types")

        reservation_data = update_reservation_data(reservation_data)
        destroy_children()
        update_data_labels(reservation_data)
        scroll_frame.update_idletasks()

    def edit_reservation(data):
        aew.create_add_edit_window(connection, username, data)
        print("out")
        get_reservation_info(connection, username)
        print("done")

    def delete_reservation(data):
        if messagebox.askyesno("Confirm", "Are you sure you want to delete reservation " + data[4] + "?"):
            bookings = bk.Bookings(connection, username)
            bookings.delete_reservation_from_database(data[4])
            get_reservation_info(connection, username)
            print("booking deleted")
        else:
            print("booking not deleted")

    def quit_app():
        if messagebox.askokcancel(title="Quit", message="Are you sure you want to quit?"):
            root.destroy()

    root = ctk.CTk()
    root.title("Consolidate")
    root.geometry("750x500")
    root.grid_columnconfigure(0, weight=1)
    root.minsize(755, 500)

    reservation_data = []

    header_font = ctk.CTkFont(weight="bold", underline=True)

    btn_frame = ctk.CTkFrame(root, fg_color=root._fg_color)
    btn_frame.grid(row=0, column=0, sticky="e", padx=10, pady=10)

    username = username
    connection = connection

    # Top side buttons
    btn_add_reservation = ctk.CTkButton(btn_frame, text="Add Reservation", height=20, width=20, command=lambda: edit_reservation(None))
    btn_add_reservation.pack(side="right", padx=1)

    btn_filter = ctk.CTkButton(btn_frame, text="Filter", height=20, width=20, command=lambda : apply_filter())
    btn_filter.pack(side="right", padx=1)

    btn_logout = ctk.CTkButton(btn_frame, text="Logout", height=20, width=20, command=lambda: quit_app())
    btn_logout.pack(side="right", padx=1)

    # top side entry
    type_dropdown = ctk.CTkComboBox(btn_frame, values=["Name", "Date", "Site", "Confirmation Code"])
    type_dropdown.pack(padx = 10, pady = 10, side = "left")
    filter_entry = ctk.CTkEntry(btn_frame)
    filter_entry.pack(side = "left")

    scroll_frame = ctk.CTkScrollableFrame(root, width=root.winfo_width(), height=500, fg_color=root._fg_color)
    scroll_frame.grid(row=2, column=0, sticky="ew")
    scroll_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1, minsize=100)

    my_label = ctk.CTkLabel(scroll_frame, text="hi")
    my_label.pack()


    header_frame = ctk.CTkFrame(root, fg_color=root._fg_color)
    header_frame.grid(row=1,sticky="ew", padx=[0, 15])
    header_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1, minsize=100)

    create_header_labels()
    
    get_reservation_info(connection, username)

    # Update the canvas scroll region
    scroll_frame.update_idletasks()
    #canvas.config(scrollregion=canvas.bbox("all"))

    root.mainloop()

#create_reservation_screen("debug", "name")