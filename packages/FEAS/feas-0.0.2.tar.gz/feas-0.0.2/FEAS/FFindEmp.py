import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector


class EmployeeFinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Feas - Finding Employee")
        self.root.geometry("900x600+300+100")  # Fixed size and centered on the screen
        self.root.resizable(False, False)  # Disable resizing and maximize button

        # MySQL Connection
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
        self.heading_label = tk.Label(self.top_frame, text="Feas - Finding Employee", font=("Segoe UI", 18, "bold"))
        self.heading_label.pack()

        # Center Frame - Search Box and Treeview
        self.center_frame = tk.Frame(self.root, height=300, width=900)
        self.center_frame.place(relx=0.5, rely=0.4, anchor="center")

        # Search Entry Box
        self.search_label = tk.Label(self.center_frame, text="Employee First Name:")
        self.search_label.place(x=10, y=10)

        self.search_entry = tk.Entry(self.center_frame, width=30)
        self.search_entry.place(x=150, y=10)
        self.search_entry.bind("<KeyRelease>", self.update_treeview)

        # Treeview Setup
        self.tree = ttk.Treeview(self.center_frame, columns=(
            "ID", "Login", "First Name", "Last Name", "Join Date", "Manager",
            "Contact No", "Email", "Emergency 1", "Emergency 2"
        ), show="headings", height=10)

        # Treeview Headings
        columns = [
            ("ID", 80), ("Login", 100), ("First Name", 100), ("Last Name", 100), ("Join Date", 100),
            ("Manager", 100), ("Contact No", 100), ("Email", 150), ("Emergency 1", 100), ("Emergency 2", 100)
        ]

        for col_name, col_width in columns:
            self.tree.heading(col_name, text=col_name)
            self.tree.column(col_name, width=col_width, anchor="center")

        # Scrollbar for Treeview
        self.scrollbar = ttk.Scrollbar(self.center_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)

        self.tree.place(x=10, y=50)
        self.scrollbar.place(x=860, y=50, height=225)

        # Bottom Frame - Exit Button
        self.bottom_frame = tk.Frame(self.root, height=50, width=800)
        self.bottom_frame.place(relx=0.5, rely=0.85, anchor="center")

        self.exit_button = tk.Button(self.bottom_frame, text="Exit", command=self.close_app, fg="white", bg="red",
                                     width=10)
        self.exit_button.place(x=350, y=10)

    def update_treeview(self, event):
        """Filter and display employee information as user types in the search entry."""
        search_term = self.search_entry.get()
        self.cursor.execute(
            "SELECT cEmp_ID, cEmp_Login, cEmp_FName, cEmp_LName, cEmp_JoinDate, cEmp_Manager, "
            "cEmp_ContactNo, cEmpContactEmail, cEmp_Emergency1, cEmp_Emergency2 "
            "FROM tEmp_Main WHERE cEmp_FName LIKE %s", (f"{search_term}%",)
        )
        records = self.cursor.fetchall()

        # Clear current tree view entries
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Insert filtered data into the tree view
        for record in records:
            self.tree.insert("", "end", values=record)

    def close_app(self):
        """Close the database connection and exit the program."""
        self.cursor.close()
        self.conn.close()
        self.root.quit()


# Main Program Execution
if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeFinderApp(root)
    root.mainloop()