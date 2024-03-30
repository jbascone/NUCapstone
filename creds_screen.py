import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import bookings as bk
import menu as menu
from tracking_sites import Credentials

def creds_screen(connection, username):

    def get_creds_info(self, connection, username):
        #call to database table with creds to get current users credentials, call update_creds_data to update data 
        #for labels, call update_data_labels to show current creds
        creds = Credentials.get_all_credentials_from_database(self, connection)
        creds_data = update_creds_data(creds)
        update_data_labels(creds_data)


    def add_creds():
        #call new screen to add cred info
        pass

    def delete_cred(cred):
        #take info from line, pass to database table for drop, call get_creds_info
        pass

    def update_creds_data(creds):
        creds_data = []
        for cred in creds:
            temp_list = []
            temp_list.append(cred.username_track)
            temp_list.append(cred.password_track)
            temp_list.append(cred.url)
            creds_data.append(temp_list)
        return creds_data
        
    def update_data_labels(creds_data):
        for row, data in enumerate(creds_data):
            for col, value in enumerate(data):
                label_data = tk.Label(inner_frame, text=value, width=15, relief="solid")
                label_data.grid(row=row + 1, column=col, padx=5, pady=5)
            delete_button = tk.Button(inner_frame, text = "Delete", command= lambda i = data: 
                                delete_cred(i))
            print("Button created for row " + str(row))
            delete_button.grid(row=row+1, column = 9, padx= 1, pady= 1)


    def destroy_children():
         for widget in inner_frame.winfo_children():
              widget.destroy()
         inner_frame.pack_forget()
         print("clicked")

    def create_header_labels():
        date_label = tk.Label(header_frame, text="Username", width=15, relief="solid", anchor="center")
        date_label.grid(row=0, column=0, padx=5, pady=5)

        time_label = tk.Label(header_frame, text="Password", width=15, relief="solid")
        time_label.grid(row=0, column=1, padx=5, pady=5)

        name_label = tk.Label(header_frame, text="URL", width=15, relief="solid")
        name_label.grid(row=0, column=2, padx=5, pady=5)

    root = tk.Tk()
    root.title("Credentials Management")
    root.geometry("455x500")

    btn_frame = ttk.Frame(root)
    btn_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10,sticky="nsew")

    username = username
    connection = connection

    # Top side buttons

    btn_back = tk.Button(btn_frame, text="back", height=2, width=12, command=lambda: root.quit())
    btn_back.pack(side="right")

    btn_add_creds = tk.Button(btn_frame, text="Add Credential", height=2, width=12, command=lambda: add_creds(connection, username) )
    btn_add_creds.pack(side="right")



    #frame for creds information
    creds_frame = ttk.Frame(root)
    creds_frame.grid(row=2, column=0, columnspan=3, rowspan=8, padx=10, pady=10, sticky="nsew")

    # Create a canvas with a scrollbar
    canvas = tk.Canvas(creds_frame, width=420, height=500)
    scrollbar = ttk.Scrollbar(creds_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Place the canvas and scrollbar
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Create a frame inside the canvas
    inner_frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=inner_frame, anchor="nw")
    canvas.yview_scroll(0, 'units')

    header_frame = ttk.Frame(root)
    header_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10,sticky="nsew")





    # Sample reservation data (you can replace this with actual data)
    creds_data = [
        #["Username", "pass", "URL"],
        # Add more rows as needed
    ]

    creds_data = Credentials.get_all_credentials_from_database(connection, connection)
    creds_data = update_creds_data(creds_data)


    create_header_labels()
    
    for row, data in enumerate(creds_data):
        for col, value in enumerate(data):
            label_data = tk.Label(inner_frame, text=value, width=15, relief="solid")
            label_data.grid(row=row + 1, column=col, padx=5, pady=5)
        delete_button = tk.Button(inner_frame, text = "Delete", command= lambda i = data: 
                            delete_cred(i))
        print("Button created for row " + str(row))
        delete_button.grid(row=row+1, column = 9, padx= 1, pady= 1)
        print(data)

    # Update the canvas scroll region
    inner_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    root.mainloop()
