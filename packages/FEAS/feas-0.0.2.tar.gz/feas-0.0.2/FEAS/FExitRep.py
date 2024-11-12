import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import mysql.connector


class FireExitInspectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FEAS - Fire Exits Inspection and Status")
        self.root.geometry("800x500+300+100")  # Fixed size and centered on the screen
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
        self.top_frame = tk.Frame(self.root, height=50, width=100)
        self.top_frame.place(relx=0.5, rely=0.05, anchor="center")
        self.heading_label = tk.Label(self.top_frame, text="FEAS - Fire Exits Inspection and Status",
                                      font=("Segoe UI", 16, "bold"))
        self.heading_label.pack()

        # Center Frame - Treeview for Exit Inspection Data
        self.center_frame = tk.Frame(self.root, height=400, width=700)
        self.center_frame.place(relx=0.6, rely=0.6, anchor="center")

        # Treeview Setup
        self.tree = ttk.Treeview(self.center_frame, columns=("Exit No", "Location", "Status", "Inspection Date"),
                                 show="headings", height=12)

        # Treeview Headings
        self.tree.heading("Exit No", text="Exit No")
        self.tree.heading("Location", text="Location")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Inspection Date", text="Inspection Date")

        # Treeview Column Widths
        self.tree.column("Exit No", width=100, anchor="center")
        self.tree.column("Location", width=150, anchor="center")
        self.tree.column("Status", width=100, anchor="center")
        self.tree.column("Inspection Date", width=150, anchor="center")

        # Scrollbar for Treeview
        self.scrollbar = ttk.Scrollbar(self.center_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)

        self.tree.place(x=10, y=10)
        self.scrollbar.place(x=700, y=10, height=260)

        # Load data into the Treeview
        self.load_data()

        # Bottom Frame - Exit Button
        self.bottom_frame = tk.Frame(self.root, height=200, width=750)
        self.bottom_frame.place(relx=0.6, rely=1, anchor="center")
        self.legend_label = tk.Label(self.bottom_frame,
                                     text="Legends - Red line indicates inactive Exit and expired or soon expired Inspection Date.",
                                     font=("Segoe UI", 10, "bold"))
        self.legend_label.place(x=0, y=0)

        self.exit_button = tk.Button(self.bottom_frame, text="Exit", command=self.close_app, fg="white", bg="red",
                                     width=10)
        self.exit_button.place(x=250, y=40)

    def load_data(self):
        """Load and filter exit inspection data, highlight inactive or soon-to-expire records."""
        current_date = datetime.now()
        one_month_from_now = current_date + timedelta(days=30)

        # Query for fire exit inspection data
        self.cursor.execute("SELECT cExitNo, cFlrSide_ID, is_Active, cInspt_date FROM tcmp_fcexits")
        records = self.cursor.fetchall()

        # Clear current tree view entries
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Mapping for location and status values
        location_mapping = {"01": "East", "02": "South", "03": "West", "04": "North"}
        status_mapping = {1: "Active", 0: "Not Active"}

        # Insert and highlight data in the tree view
        for record in records:
            cExitNo, cFlrSide_ID, is_Active, cInspt_date = record

            # Convert data
            location = location_mapping.get(cFlrSide_ID, "Unknown")
            status = status_mapping.get(is_Active, "Unknown")
            inspection_date = cInspt_date.strftime('%Y-%m-%d')

            # Determine background and foreground color
            bg_color = "white"
            fg_color = "black"

            if is_Active == 0 or cInspt_date < current_date.date() or (
                    cInspt_Date <= one_month_from_now and cInspt_date >= current_date.date()):
                bg_color = "red"
                fg_color = "white"

            # Insert data with style
            self.tree.insert("", "end", values=(cExitNo, location, status, inspection_date), tags=("highlight",))
            self.tree.tag_configure("highlight", background=bg_color, foreground=fg_color)

    def close_app(self):
        """Close the database connection and exit the program."""
        self.cursor.close()
        self.conn.close()
        self.root.quit()


# Main Program Execution
if __name__ == "__main__":
    root = tk.Tk()
    app = FireExitInspectionApp(root)
    root.mainloop()