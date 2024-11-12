import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector


class CompanyInfoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Company Information Setup")
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

        # Variable Tracking
        self.initial_values = {}  # Store initial values for comparison
        self.is_modified = False  # Track if data has been modified

        # Top Frame (Heading)
        self.top_frame = tk.Frame(self.root, height=100)
        self.top_frame.place(relx=0.5, rely=0.1, anchor="center")
        self.heading_label = tk.Label(self.top_frame, text="Company Information", font=("Segoe UI", 18, "bold"))
        self.heading_label.pack()

        # Center Frame (Form)
        self.center_frame = tk.Frame(self.root)
        self.center_frame.place(relx=0.5, rely=0.4, anchor="center")

        # Bottom Frame (Buttons)
        self.bottom_frame = tk.Frame(self.root, height=50)
        self.bottom_frame.place(relx=0.5, rely=0.8, anchor="center")
        self.save_button = tk.Button(self.bottom_frame, text="Save", command=self.save_data, state="disabled", width=10)
        self.save_button.grid(row=0, column=0, padx=10)
        self.exit_button = tk.Button(self.bottom_frame, text="Exit", command=self.root.quit, width=10)
        self.exit_button.grid(row=0, column=2, padx=10)

        # Form Fields
        self.country_var = tk.StringVar()
        self.province_var = tk.StringVar()
        self.city_var = tk.StringVar()

        self.setup_form()
        self.populate_form()

    def setup_form(self):
        # Labels and dropdowns
        tk.Label(self.center_frame, text="Country:", anchor="w").grid(row=0, column=0, sticky="w")
        self.country_combo = ttk.Combobox(self.center_frame, textvariable=self.country_var, state="readonly")
        self.country_combo.grid(row=0, column=1, sticky="e", padx=5, pady=5)
        self.country_combo.bind("<<ComboboxSelected>>", self.update_provinces)

        tk.Label(self.center_frame, text="Province:", anchor="w").grid(row=1, column=0, sticky="w")
        self.province_combo = ttk.Combobox(self.center_frame, textvariable=self.province_var, state="readonly")
        self.province_combo.grid(row=1, column=1, sticky="e", padx=5, pady=5)
        self.province_combo.bind("<<ComboboxSelected>>", self.update_cities)

        tk.Label(self.center_frame, text="City:", anchor="w").grid(row=2, column=0, sticky="w")
        self.city_combo = ttk.Combobox(self.center_frame, textvariable=self.city_var, state="readonly")
        self.city_combo.grid(row=2, column=1, sticky="e", padx=5, pady=5)

        # Other form fields can go here, following the same pattern

    def populate_form(self):
        # Populate country dropdown from tcmp_loc table
        self.cursor.execute("SELECT DISTINCT cloc_country FROM tcmp_loc")
        countries = [row[0] for row in self.cursor.fetchall()]
        self.country_combo['values'] = countries

        # Retrieve initial data and fill the form (assuming single record)
        self.cursor.execute("SELECT * FROM tcmp_loc LIMIT 1")
        data = self.cursor.fetchone()
        if data:
            self.initial_values = {
                'country': data[0],
                'province': data[1],
                'city': data[2]
                # Add other fields as needed
            }
            # Set initial form values
            self.country_var.set(self.initial_values['country'])
            self.update_provinces(initial_load=True)
            self.province_var.set(self.initial_values['province'])
            self.update_cities(initial_load=True)
            self.city_var.set(self.initial_values['city'])

    def update_provinces(self, event=None, initial_load=False):
        # Update province dropdown based on selected country
        country = self.country_var.get()
        self.cursor.execute("SELECT DISTINCT cProv_Desc FROM tcmp_province WHERE cCnt_ID=%s", (country,))
        provinces = [row[0] for row in self.cursor.fetchall()]
        self.province_combo['values'] = provinces
        if initial_load:
            self.province_var.set(self.initial_values['province'])

    def update_cities(self, event=None, initial_load=False):
        # Update city dropdown based on selected province
        province = self.province_var.get()
        self.cursor.execute("SELECT cCity_Name FROM tcmp_city WHERE cProv_id=%s", (province,))
        cities = [row[0] for row in self.cursor.fetchall()]
        self.city_combo['values'] = cities
        if initial_load:
            self.city_var.set(self.initial_values['city'])

    def edit_data(self):
        # Enable editing if required
        self.is_modified = True
        self.save_button.config(state="normal")

    def save_data(self):
        # Save changes to the database
        country = self.country_var.get()
        province = self.province_var.get()
        city = self.city_var.get()

        # Sample SQL Update Query
        update_query = """
            UPDATE tcmp_loc SET 
                cloc_country = %s, 
                cProv_Desc = %s, 
                cCity_Name = %s
            WHERE cloc_country = %s
        """
        self.cursor.execute(update_query, (country, province, city, self.initial_values['country']))
        self.conn.commit()

        # Update initial values and disable Save button
        self.initial_values.update({'country': country, 'province': province, 'city': city})
        self.save_button.config(state="disabled")

        # Show confirmation message
        messagebox.showinfo("Saved", "Data Saved...")

    def close_app(self):
        # Close the database connection before exiting
        self.cursor.close()
        self.conn.close()
        self.root.quit()


# Main Program
if __name__ == "__main__":
    root = tk.Tk()
    app = CompanyInfoApp(root)
    root.mainloop()
