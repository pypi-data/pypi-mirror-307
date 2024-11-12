import tkinter as tk
from tkinter import ttk
import mysql.connector


class FloorInformationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FEAS- Floor Information")
        self.root.geometry("1000x600+250+100")  # Fixed size and centered on the screen
        self.root.resizable(False, False)  # Disable resizing and maximize button

        # Database Connection
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="MeOnly@007",
            database="feas"
        )
        self.cursor = self.conn.cursor()

        # Top Frame - Heading
        self.top_frame = tk.Frame(self.root, height=100, width=200)
        self.top_frame.place(relx=0.5, rely=0.05, anchor="center")
        self.heading_label = tk.Label(self.top_frame, text="FEAS- Floor Information", font=("Segoe UI", 16, "bold"))
        self.heading_label.pack()

        # Center Frame - Main Program Frame
        self.center_frame = tk.Frame(self.root, height=400, width=900)
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Floor Dropdown Label
        self.floor_label = tk.Label(self.center_frame, text="Select Floor:", font=("Segoe UI", 10))
        self.floor_label.place(x=10, y=20)

        # Floor Dropdown List
        self.floor_var = tk.StringVar()
        self.floor_dropdown = ttk.Combobox(self.center_frame, textvariable=self.floor_var, width=20)
        self.floor_dropdown.place(x=100, y=10)
        self.load_floor_options()
        self.floor_dropdown.bind("<<ComboboxSelected>>", self.update_floor_info)

        # Frame 1: Floor AA Information
        self.frame1 = tk.Frame(self.center_frame, width=300, height=200, bg="brown")
        self.frame1.place(x=20, y=50)
        self.frame1_label = tk.Label(self.frame1, text="Employees on Floor", font=("Segoe UI", 12, "bold"), bg="brown",
                                     fg="white")
        self.frame1_label.place(relx=0.5, rely=0.1, anchor="center")

        # Labels to display employee count per side
        self.south_label = tk.Label(self.frame1, text="Employees on South:", bg="brown", fg="white", anchor="w")
        self.south_label.place(x=10, y=50)
        self.north_label = tk.Label(self.frame1, text="Employees on North:", bg="brown", fg="white", anchor="w")
        self.north_label.place(x=10, y=80)
        self.east_label = tk.Label(self.frame1, text="Employees on East:", bg="brown", fg="white", anchor="w")
        self.east_label.place(x=10, y=110)
        self.west_label = tk.Label(self.frame1, text="Employees on West:", bg="brown", fg="white", anchor="w")
        self.west_label.place(x=10, y=140)

        # Frame 2: Floor Manager Information
        self.frame2 = tk.Frame(self.center_frame, width=300, height=200)
        self.frame2.place(x=350, y=50)
        self.frame2_label = tk.Label(self.frame2, text="Floor Manager", font=("Segoe UI", 12, "bold"))
        self.frame2_label.place(relx=0.5, rely=0.1, anchor="center")
        self.manager_info_label = tk.Label(self.frame2, text="", anchor="w", justify="left")
        self.manager_info_label.place(x=10, y=50)

        # Frame 3: Floor Supervisor Information
        self.frame3 = tk.Frame(self.center_frame, width=300, height=200)
        self.frame3.place(x=680, y=50)
        self.frame3_label = tk.Label(self.frame3, text="Floor Supervisor", font=("Segoe UI", 12, "bold"))
        self.frame3_label.place(relx=0.5, rely=0.1, anchor="center")
        self.supervisor_info_label = tk.Label(self.frame3, text="", anchor="w", justify="left")
        self.supervisor_info_label.place(x=10, y=50)

        # Bottom Frame - Exit Button
        self.bottom_frame = tk.Frame(self.root, height=100, width=200)
        self.bottom_frame.place(relx=0.5, rely=0.75, anchor="center")
        self.exit_button = tk.Button(self.bottom_frame, text="Exit", command=self.close_app, fg="white", bg="red",
                                     width=12, height=2, font=("Segoe UI", 12, "bold"))
        self.exit_button.pack()

    def load_floor_options(self):
        """Load floor options from the database for the dropdown."""
        self.cursor.execute("SELECT cFloor_ID FROM tcmp_floor")
        floors = self.cursor.fetchall()
        self.floor_dropdown['values'] = [floor[0] for floor in floors]

    def update_floor_info(self, event=None):
        """Update the display with selected floor information."""
        floor_id = self.floor_var.get()

        # Update Frame 1 - Employee Count per Side
        for side_id, side_label in [(2, self.south_label), (4, self.north_label), (1, self.east_label),
                                    (3, self.west_label)]:
            count = self.get_employee_count(floor_id, side_id)
            side_label.config(text=f"Employees on {side_label.cget('text').split()[-1]}: {count}")

        # Update Frame 2 - Floor Manager Information
        manager_info = self.get_manager_info(floor_id)
        manager_text = "\n".join([f"{label}: {value}" for label, value in zip(
            ["Floor ID", "Floor Manager ID", "Login", "First Name", "Last Name", "Join Date", "Manager", "Contact No",
             "Email"],
            manager_info)]) if manager_info else "No manager found for this floor."
        self.manager_info_label.config(text=manager_text)

        # Update Frame 3 - Floor Supervisor Information
        supervisor_info = self.get_supervisor_info(floor_id)
        supervisor_text = "\n".join([f"{label}: {value}" for label, value in zip(
            ["Floor ID", "Supervisor ID", "Login", "First Name", "Last Name", "Join Date", "Manager", "Contact No",
             "Email"],
            supervisor_info)]) if supervisor_info else "No supervisor found for this floor."
        self.supervisor_info_label.config(text=supervisor_text)

    def get_employee_count(self, floor_id, side_id):
        """Fetch employee count based on floor ID and floor side ID."""
        query = """
        SELECT COUNT(*) FROM tcmp_stations
        WHERE cFloor_ID = %s AND cFlrSide_ID = %s AND cStn_status = 0 AND cEmp_id IS NOT NULL
        """
        self.cursor.execute(query, (floor_id, side_id))
        result = self.cursor.fetchone()
        return result[0] if result else 0

    def get_manager_info(self, floor_id):
        """Fetch manager information for a specific floor."""
        query = """
        SELECT b.cFloor_ID, b.cFloor_manager, a.cEmp_login, a.cEmp_FName, a.cEmp_LName, a.cEmp_JoinDate, 
               a.cEmp_manager, a.cEmp_ContactNo, a.cEmpContactEmail
        FROM tcmp_floor b, temp_main a
        WHERE b.cFloor_manager = a.cEmp_ID AND b.cFloor_ID = %s
        """
        self.cursor.execute(query, (floor_id,))
        return self.cursor.fetchone()

    def get_supervisor_info(self, floor_id):
        """Fetch supervisor information for a specific floor."""
        query = """
        SELECT b.cFloor_ID, b.cFloor_PA, a.cEmp_login, a.cEmp_FName, a.cEmp_LName, a.cEmp_JoinDate, 
               a.cEmp_manager, a.cEmp_ContactNo, a.cEmpContactEmail
        FROM tcmp_floor b, temp_main a
        WHERE b.cFloor_PA = a.cEmp_ID AND b.cFloor_ID = %s
        """
        self.cursor.execute(query, (floor_id,))
        return self.cursor.fetchone()

    def close_app(self):
        """Close the application and database connection."""
        self.cursor.close()
        self.conn.close()
        self.root.quit()


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = FloorInformationApp(root)
    root.mainloop()
