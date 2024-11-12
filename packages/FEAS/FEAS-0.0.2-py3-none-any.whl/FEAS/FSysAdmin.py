import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector


class SystemAdminApp:
    def __init__(self, root):
        self.root = root
        self.root.title("System Administrator Management")
        self.root.geometry("800x600+300+100")  # Centered screen with fixed dimensions
        self.root.resizable(False, False)  # Disable maximize button

        # MySQL Connection Details
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="MeOnly@007",
            database="feas"
        )
        self.cursor = self.conn.cursor()

        # Top Frame - Heading
        self.top_frame = tk.Frame(self.root, height=100)
        self.top_frame.place(relx=0.5, rely=0.05, anchor="center")
        self.heading_label = tk.Label(self.top_frame, text="System Administrators", font=("Segoe UI", 18, "bold"))
        self.heading_label.pack()

        # Center Frame - Treeview for Admin List
        self.center_frame = tk.Frame(self.root)
        self.center_frame.place(relx=0.5, rely=0.4, anchor="center")

        # Treeview Setup
        self.admin_tree = ttk.Treeview(self.center_frame, columns=("ID", "Password"), show="headings", height=15)
        self.admin_tree.heading("ID", text="Administrator ID")
        self.admin_tree.heading("Password", text="Password")
        self.admin_tree.column("ID", width=150, anchor="center")
        self.admin_tree.column("Password", width=150, anchor="center")
        self.admin_tree.bind("<Double-1>", self.on_treeview_double_click)

        # Scrollbar for Treeview
        self.scrollbar = ttk.Scrollbar(self.center_frame, orient="vertical", command=self.admin_tree.yview)
        self.admin_tree.configure(yscroll=self.scrollbar.set)

        self.admin_tree.pack(side="left")
        self.scrollbar.pack(side="right", fill="y")

        # Bottom Frame - Add, Save, and Exit Buttons

        self.bottom_frame = tk.Frame(self.root, height=300, width=600)
        self.bottom_frame.place(relx=0.5, rely=0.85, anchor="center")

        # Editable Fields in Bottom Frame
        self.id_label = tk.Label(self.bottom_frame, text="Admin ID:", anchor="w")
        self.id_label.place(x=180, y=40)
        self.id_entry = tk.Entry(self.bottom_frame)
        self.id_entry.place(x=260, y=40, width=120)

        self.pw_label = tk.Label(self.bottom_frame, text="Password:", anchor="w")
        self.pw_label.place(x=180, y=60)
        self.pw_entry = tk.Entry(self.bottom_frame, show="*")
        self.pw_entry.place(x=260, y=60, width=120)

        # Load Initial Data
        self.load_data()

#        self.add_button = tk.Button(self.bottom_frame, text="Add", command=self.add_data, fg="white", bg="blue",
#                                    width=10)
        self.add_button = tk.Button(self.bottom_frame, text="Add", font=("Segoe UI", 12), bg="#0078D7", fg="white",
                                activebackground="#005A9E", activeforeground="white", command=self.add_data,
                                height=2, width=15)
        self.add_button.place(x=80, y=130)

        self.save_button = tk.Button(self.bottom_frame, text="Save", font=("Segoe UI", 12), bg="#0078D7", fg="white",
                                activebackground="#005A9E", activeforeground="white", command=self.save_data,
                                height=2, width=15)
        self.save_button.place(x=240, y=130)

        self.exit_button = tk.Button(self.bottom_frame, text="Exit", font=("Segoe UI", 12), bg="#D83B01", fg="white",
                                activebackground="#A52A2A", activeforeground="white", command=self.root.quit,
                                height=2, width=15)
        self.exit_button.place(x=400, y=130)


    def load_data(self):
        """Load system administrators from the database and display in the treeview."""
        for row in self.admin_tree.get_children():
            self.admin_tree.delete(row)

        self.cursor.execute("SELECT cSysAdmin_ID, cSysAdmin_PW FROM tcmp_sysadmin")
        for row in self.cursor.fetchall():
            self.admin_tree.insert("", "end", values=row)

    def on_treeview_double_click(self, event):
        """Fill in the entry fields with the selected item for editing."""
        selected_item = self.admin_tree.selection()[0]
        admin_id, admin_pw = self.admin_tree.item(selected_item, "values")
        self.id_entry.delete(0, tk.END)
        self.id_entry.insert(0, admin_id)
        self.pw_entry.delete(0, tk.END)
        self.pw_entry.insert(0, admin_pw)
        self.save_button.config(state="normal")

    def add_data(self):
        """Prepare entry fields for new data entry."""
        self.id_entry.delete(0, tk.END)
        self.pw_entry.delete(0, tk.END)
        self.save_button.config(state="normal")
        self.id_entry.focus_set()

    def save_data(self):
        """Save or update data in the database."""
        admin_id = self.id_entry.get()
        admin_pw = self.pw_entry.get()

        if not admin_id or not admin_pw:
            messagebox.showerror("Error", "Both fields are required.")
            return

        # Check if the ID already exists
        self.cursor.execute("SELECT cSysAdmin_ID FROM tcmp_sysadmin WHERE cSysAdmin_ID = %s", (admin_id,))
        exists = self.cursor.fetchone()

        if exists:
            # Update existing record
            self.cursor.execute("UPDATE tcmp_sysadmin SET cSysAdmin_PW = %s WHERE cSysAdmin_ID = %s",
                                (admin_pw, admin_id))
            self.conn.commit()
            messagebox.showinfo("Updated", "Data Updated...")
        else:
            # Insert new record
            self.cursor.execute("INSERT INTO tcmp_sysadmin (cSysAdmin_ID, cSysAdmin_PW) VALUES (%s, %s)",
                                (admin_id, admin_pw))
            self.conn.commit()
            messagebox.showinfo("Saved", "Data Saved...")

        self.load_data()
        self.save_button.config(state="disabled")

    def close_app(self):
        """Close the database connection and quit the application."""
        self.cursor.close()
        self.conn.close()
        self.root.quit()


# Main Program
if __name__ == "__main__":
    root = tk.Tk()
    app = SystemAdminApp(root)
    root.mainloop()