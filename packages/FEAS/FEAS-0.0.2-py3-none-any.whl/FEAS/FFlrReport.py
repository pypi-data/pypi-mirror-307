import tkinter as tk
from tkinter import ttk
import mysql.connector
from datetime import datetime, timedelta
import threading


class FloorStatusApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FEAS - Floor and Floor Side Status Current")
        self.root.geometry("800x500+300+100")  # Fixed size, centered on the screen
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
        self.top_frame = tk.Frame(self.root,height=100,width=100)
        self.top_frame.place(relx=0.5, rely=0.05, anchor="center")
        self.heading_label = tk.Label(self.top_frame, text="FEAS - Floor and Floor Side Current Status",
                                      font=("Segoe UI", 16, "bold"))
        self.heading_label.pack()

        # Center Frame - Treeview for Floor Status List
        self.center_frame = tk.Frame(self.root, height=500, width=800)
        self.center_frame.place(relx=0.55, rely=0.6, anchor="center")

        # Treeview Setup
        self.tree = ttk.Treeview(self.center_frame, columns=("Floor ID", "Floor Side", "Fire", "Heat", "Smoke"),
                                 show="headings", height=15)

        # Treeview Headings
        self.tree.heading("Floor ID", text="Floor ID")
        self.tree.heading("Floor Side", text="Floor Side")
        self.tree.heading("Fire", text="Fire")
        self.tree.heading("Heat", text="Heat")
        self.tree.heading("Smoke", text="Smoke")

        # Treeview Column Widths
        self.tree.column("Floor ID", width=100, anchor="center")
        self.tree.column("Floor Side", width=150, anchor="center")
        self.tree.column("Fire", width=100, anchor="center")
        self.tree.column("Heat", width=100, anchor="center")
        self.tree.column("Smoke", width=100, anchor="center")

        # Scrollbar for Treeview
        self.scrollbar = ttk.Scrollbar(self.center_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)

        self.tree.place(x=10, y=10)
        self.scrollbar.place(x=670, y=10, height=310)


        # Bottom Frame - Exit Button
        self.bottom_frame = tk.Frame(self.root, height=100, width=500)
        self.bottom_frame.place(relx=0.5, rely=0.9, anchor="center")

        # Timer Label for Refresh Countdown
        self.timer_label = tk.Label(self.bottom_frame, text="", font=("Segoe UI", 10), fg="blue")
        self.timer_label.place(x=0, y=0)

        # Load initial data and start auto-refresh
        self.refresh_data()
        self.start_refresh_timer()




        self.exit_button = tk.Button(self.bottom_frame, text="Exit", command=self.close_app, fg="white", bg="red",
                                     width=12, height=2, font=("Segoe UI", 12, "bold"))
        self.exit_button.place(x=170, y=40)

    def refresh_data(self):
        """Retrieve and display floor status data from MySQL database with conditional formatting."""
        # Clear existing data in the Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Retrieve data from the database
        query = """
        SELECT tcmp_firedata.cfloor_id, tcmp_firedata.cFlrSide_ID, tcmp_firedata.cFire, tcmp_heatdata.cheat, tcmp_smokedata.csmoke
        FROM tcmp_firedata
        JOIN tcmp_heatdata ON tcmp_firedata.cfloor_id = tcmp_heatdata.cfloor_id AND tcmp_firedata.cFlrSide_Id = tcmp_heatdata.cFlrSide_Id
        JOIN tcmp_smokedata ON tcmp_firedata.cfloor_id = tcmp_smokedata.cfloor_id AND tcmp_firedata.cFlrSide_Id = tcmp_smokedata.cFlrSide_Id;
        """
        self.cursor.execute(query)
        records = self.cursor.fetchall()

        for record in records:
            cfloor_id, cFlrSide_ID, cFire, cHeat, cSmoke = record
            # Convert database values for display
            floor_side = self.get_floor_side(cFlrSide_ID)

            # Conditional styling for each column based on the values of cFire, cHeat, cSmoke
            row_style = {
                "Fire": "green" if cFire == '00' else "red",
                "Heat": "green" if cHeat == '00' else "red",
                "Smoke": "green" if cSmoke == '00' else "red"
            }

            # Insert data with styling based on conditions
            item = self.tree.insert("", "end", values=(cfloor_id, floor_side, cFire, cHeat, cSmoke))
            self.tree.item(item, tags=(
            f"Fire_{row_style['Fire']}", f"Heat_{row_style['Heat']}", f"Smoke_{row_style['Smoke']}"))

        # Define custom tags for conditional formatting
        self.tree.tag_configure("Fire_red", background="red", foreground="white")
        self.tree.tag_configure("Fire_green", background="green", foreground="white")
        self.tree.tag_configure("Heat_red", background="red", foreground="white")
        self.tree.tag_configure("Heat_green", background="green", foreground="white")
        self.tree.tag_configure("Smoke_red", background="red", foreground="white")
        self.tree.tag_configure("Smoke_green", background="green", foreground="white")

    @staticmethod
    def get_floor_side(cFlrSide_ID):
        """Map Floor Side ID to descriptive string."""
        floor_sides = {
            "01": "East",
            "02": "South",
            "03": "West",
            "04": "North"
        }
        return floor_sides.get(cFlrSide_ID, "Unknown")

    def start_refresh_timer(self):
        """Start a countdown timer for refreshing data every 10 seconds."""
        self.next_refresh = datetime.now() + timedelta(seconds=10)
        self.update_timer()

    def update_timer(self):
        """Update timer label and refresh data when countdown reaches zero."""
        remaining = (self.next_refresh - datetime.now()).seconds
        if remaining > 0:
            self.timer_label.config(text=f"Refreshing Floor data in {remaining} seconds...")
            self.root.after(1000, self.update_timer)  # Update every second
        else:
            self.refresh_data()
            self.start_refresh_timer()

    def close_app(self):
        """Close the database connection and exit the program."""
        self.cursor.close()
        self.conn.close()
        self.root.quit()


# Main Program Execution
if __name__ == "__main__":
    root = tk.Tk()
    app = FloorStatusApp(root)
    root.mainloop()
