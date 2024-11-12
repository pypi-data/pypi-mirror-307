import tkinter as tk
from tkinter import messagebox
import mysql.connector


class CompanyProfileApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Company Profile")
        self.root.geometry("800x500")
        self.root.resizable(False, False)

        # Center the window on the screen
        window_width, window_height = 800, 500
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_coordinate = (screen_width // 2) - (window_width // 2)
        y_coordinate = (screen_height // 2) - (window_height // 2)
        self.root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

        # Establish database connection
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="MeOnly@007",
            database="feas"
        )
        self.db_cursor = self.db_connection.cursor(dictionary=True)

        self.create_widgets()

    def create_widgets(self):
        # Top Frame with Heading
        top_frame = tk.Frame(self.root, bg="#4F81BD", height=60)
        top_frame.place(x=0, y=0, width=800, height=60)

        heading_label = tk.Label(top_frame, text="Company Profile", font=("Arial", 18, "bold"), bg="#4F81BD",
                                 fg="white")
        heading_label.place(relx=0.5, rely=0.5, anchor="center")

        # Main Form Frame
        form_frame = tk.Frame(self.root, bg="white")
        form_frame.place(x=100, y=80, width=600, height=300)

        # Left and Right Subframes in Form Frame
        left_frame = tk.Frame(form_frame, bg="white")
        left_frame.place(x=0, y=0, width=300, height=300)

        right_frame = tk.Frame(form_frame, bg="white")
        right_frame.place(x=300, y=0, width=300, height=300)

        # Retrieve tcmp_loc data
        self.retrieve_tcmp_loc_data()

        # Labels and Input Fields for tcmp_loc Columns
        self.fields = [
            ("Location:", "cLoc_ID"),
            ("Location Name:", "cLoc_Name"),
            ("Location Add 1:", "cLoc_Add1"),
            ("Location Add 2:", "cLoc_Add2"),
            ("Location City:", "cLoc_City"),
            ("Location Zip Code:", "cLoc_zip"),
            ("Province:", "cLoc_Porv"),
            ("Country:", "cLoc_Country"),
            ("Phone:", "cLoc_Phone"),
            ("Email:", "cLoc_Email")
        ]

        self.input_vars = {}

        for i, (label_text, column_name) in enumerate(self.fields):
            # Left Frame: Labels
            label = tk.Label(left_frame, text=label_text, font=("Arial", 10), bg="white", anchor="w")
            label.place(x=10, y=i * 30)

            # Right Frame: Entry Fields
            entry_var = tk.StringVar(value=self.tcmp_loc_data.get(column_name, ""))
            entry = tk.Entry(right_frame, textvariable=entry_var)
            entry.place(x=10, y=i * 30, width=200)
            self.input_vars[column_name] = entry_var

        # Bottom Frame with Buttons
        bottom_frame = tk.Frame(self.root, bg="white")
        bottom_frame.place(x=0, y=400, width=800, height=100)

        self.update_button = tk.Button(bottom_frame, text="Update",font=("Segoe UI", 12, "bold"), bg="blue", fg="white",
                                     activebackground="blue", activeforeground="white", command=self.update_data,
                                     height=2, width=15)
        self.update_button.place(relx=0.4, y=20, width=80, height=30)

        self.exit_button = tk.Button(bottom_frame, text="Exit", font=("Segoe UI", 12, "bold"), bg="#D83B01", fg="white",
                                     activebackground="#A52A2A", activeforeground="white", command=self.root.quit,
                                     height=2, width=15)
        self.exit_button.place(relx=0.55, y=20, width=80, height=30)

        # Enable the update button when any data is changed
        for var in self.input_vars.values():
            var.trace("w", self.enable_update)

    def retrieve_tcmp_loc_data(self):
        """Retrieve data from the tcmp_loc table."""
        query = "SELECT * FROM tcmp_loc LIMIT 1"  # Adjust query as needed
        self.db_cursor.execute(query)
        self.tcmp_loc_data = self.db_cursor.fetchone()

    def enable_update(self, *args):
        self.update_button["state"] = "normal"

    def update_data(self):
        # Prepare data to update
        update_data = {col: var.get() for col, var in self.input_vars.items()}
        query = """
            UPDATE tcmp_loc 
            SET cLoc_Name = %s, cLoc_Add1 = %s, cLoc_Add2 = %s, cLoc_City = %s, cLoc_zip = %s, cLoc_Porv = %s, 
                cLoc_Country = %s, cLoc_Phone = %s, cLoc_Email = %s
            WHERE cLoc_ID = %s
        """
        values = (
            update_data["cLoc_Name"],
            update_data["cLoc_Add1"],
            update_data["cLoc_Add2"],
            update_data["cLoc_City"],
            update_data["cLoc_zip"],
            update_data["cLoc_Porv"],
            update_data["cLoc_Country"],
            update_data["cLoc_Phone"],
            update_data["cLoc_Email"],
            update_data["cLoc_ID"]
        )

        try:
            self.db_cursor.execute(query, values)
            self.db_connection.commit()
            messagebox.showinfo("Success", "Data updated successfully!")
            self.update_button["state"] = "disabled"
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = CompanyProfileApp(root)
    root.mainloop()
