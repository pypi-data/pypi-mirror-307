"""
    Explanation:
    Database Connection: connect_db() connects to the MySQL database. Replace your_username, your_password, and
    your_database with actual values.
    TreeView Setup: A TreeView widget displays the data from the MySQL table tcmp_fcexits with columns cExitNo,
    cFlrSide_Id, Is_Active, and cInspt_date.
    Highlight Rows: Rows where Is_Active is 0 are highlighted in red using the TreeView tag feature.
    TreeView Selection: When an item is double-clicked in the TreeView, the corresponding data is populated in the edit
    fields below for editing.
    Edit and Save: Once the user modifies the data in the fields and clicks "Save," the corresponding record in the
     MySQL table is updated and the TreeView refreshes with the new data.
    Error Handling: Basic error handling is implemented for database operations using try-except.
    Notes:
    Ensure that the MySQL table structure matches the column names (cExitNo, cFlrSide_Id, Is_Active, cInspt_date).
    Update the connection details (host, user, password, database) in the connect_db() function.
"""


import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import arrow
from datetime import datetime

from FeasFrmCls import *
from FeasLblCls import *
from FeasInputCls import *
import FeasDBCls
import FeasMsgCls



# Database connection (Update with your credentials)
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="MeOnly@007",
        database="feas"
    )

# Main Application class using OOP and Tkinter
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("FEAS Application - Fire Exits Management")
        self.root.geometry("850x450")
        self.root.resizable(False, False)
        #self.heading_label = tk.Label(root, text="Fire Exits Management", font=("Segoe UI", 18, "bold"))
        #self.heading_label.place(relx=0.5, rely=0.05, anchor="center")


        # Connect to the MySQL database
        self.conn = connect_db()
        self.cursor = self.conn.cursor()

        # Create TreeView for displaying data
        self.tree = ttk.Treeview(root, columns=("cExitNo", "cFlrSide_Id", "Is_Active", "cInspt_date"), show='headings')
        self.tree.heading("cExitNo", text="Exit No")
        self.tree.heading("cFlrSide_Id", text="Floor/Side")
        self.tree.heading("Is_Active", text="Active")
        self.tree.heading("cInspt_date", text="Inspection Date")
        self.tree.grid(row=0, column=0, padx=10, pady=10)

        # Scrollbar for TreeView
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Bind treeview click
        self.tree.bind("<Double-1>", self.on_tree_select)

        # Create edit frame for updating selected row
        self.edit_frame = tk.Frame(root, bg="white")
        self.edit_frame.grid(row=1, column=0, columnspan=2, pady=12, padx=12, sticky="ew")

        tk.Label(self.edit_frame, text="Exit No", fg="brown", bg="white", font=("Segoe UI", 10, 'bold')).grid(row=0, column=0, padx=5, pady=5)
        self.cExitNo_entry = tk.Entry(self.edit_frame)
        self.cExitNo_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.edit_frame, text="Floor/Side", fg="brown", bg="white",font=("Segoe UI", 10, 'bold')).grid(row=1, column=0, padx=5, pady=5)
        self.cFlrSide_Id_entry = tk.Entry(self.edit_frame)
        self.cFlrSide_Id_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.edit_frame, text="Active", fg="brown", bg="white", font=("Segoe UI", 10, 'bold')).grid(row=2, column=0, padx=5, pady=5)
        self.Is_Active_entry = tk.Entry(self.edit_frame)
        self.Is_Active_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.edit_frame, text="Inspection Date", fg="brown", bg="white", font=("Segoe UI", 10, 'bold')).grid(row=3, column=0, padx=5, pady=5)
        self.cInspt_date_entry = tk.Entry(self.edit_frame)
        self.cInspt_date_entry.grid(row=3, column=1, padx=5, pady=5)


        # Save Button
        save_button = tk.Button(self.edit_frame, text="Save", font=("Segoe UI", 12), bg="#0078D7", fg="white",
                                activebackground="#005A9E", activeforeground="white", command=self.update_record,
                                height=2, width=15)
        save_button.grid(row=24, column=40, columnspan=2, pady=10)

        # Exit Button
        exit_button = tk.Button(self.edit_frame, text="Exit", font=("Segoe UI", 12), bg="#D83B01", fg="white",
                                activebackground="#A52A2A", activeforeground="white", command=self.root.quit,
                                height=2, width=15)
        exit_button.grid(row=24, column=100, columnspan=8, pady=10)


        # Initialize selected record ID
        self.selected_item = None

        # Load data into the TreeView
        self.load_data()

    # Load data from MySQL into the TreeView
    def load_data(self):
        self.cursor.execute("SELECT cExitNo, cFlrSide_Id, Is_Active, cInspt_date FROM tcmp_fcexits")
        rows = self.cursor.fetchall()
        for row in rows:
            tags = ('inactive',) if row[2] == 0 else ('active',)
            self.tree.insert('', 'end', values=row, tags=tags)
            #if row[2] == 0:
            #    self.tree.tag_configure('inactive', background='red', foreground='white')
            #else:
            #    self.tree.tag_configure('active', background='white', foreground='green')

        # Apply styles based on the Is_Active value
        self.tree.tag_configure('inactive', background='red', foreground='white')
        self.tree.tag_configure('active', background='white', foreground='green')

    # Function to handle TreeView item selection
    def on_tree_select(self, event):
        selected = self.tree.selection()[0]
        self.selected_item = self.tree.item(selected, "values")

        # Fill the entries with selected data
        self.cExitNo_entry.delete(0, tk.END)
        self.cExitNo_entry.insert(0, self.selected_item[0])

        self.cFlrSide_Id_entry.delete(0, tk.END)
        self.cFlrSide_Id_entry.insert(0, self.selected_item[1])

        self.Is_Active_entry.delete(0, tk.END)
        self.Is_Active_entry.insert(0, self.selected_item[2])

        self.cInspt_date_entry.delete(0, tk.END)
        self.cInspt_date_entry.insert(0, self.selected_item[3])

    # Function to update record in MySQL and TreeView
    def update_record(self):
        if not self.selected_item:
            messagebox.showwarning("No Selection", "Please select a record to edit")
            return

        cExitNo = self.cExitNo_entry.get()
        cFlrSide_Id = self.cFlrSide_Id_entry.get()
        Is_Active = self.Is_Active_entry.get()
        cInspt_date = self.cInspt_date_entry.get()

        try:
            # Update MySQL database
            update_query = "UPDATE tcmp_fcexits SET cFlrSide_Id=%s, Is_Active=%s, cInspt_date=%s WHERE cExitNo=%s"
            self.cursor.execute(update_query, (cFlrSide_Id, Is_Active, cInspt_date, cExitNo))
            self.conn.commit()

            # Clear TreeView and reload updated data
            self.tree.delete(*self.tree.get_children())
            self.load_data()

            messagebox.showinfo("Success", "Record updated successfully")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

# Create and run the Tkinter application
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
