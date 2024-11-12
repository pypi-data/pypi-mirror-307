import tkinter as tk
from tkinter import messagebox, ttk
import customtkinter as ctk
from functools import partial
import subprocess

# Step 1: Create the login window using OOP principles
class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FEAS- System Login")
        self.geometry("400x300")
        self.configure(bg='#dfe6e9')
        self.resizable(False, False)

        # Label and Entry for Username
        self.username_label = tk.Label(self, text="Username:", bg='#dfe6e9', font=("Arial", 12))
        self.username_label.place(x=50, y=80)
        self.username_entry = tk.Entry(self, width=30)
        self.username_entry.place(x=150, y=80)

        # Label and Entry for Password
        self.password_label = tk.Label(self, text="Password:", bg='#dfe6e9', font=("Arial", 12))
        self.password_label.place(x=50, y=130)
        self.password_entry = tk.Entry(self, show='*', width=30)
        self.password_entry.place(x=150, y=130)

        # Login Button
        self.login_button = tk.Button(self, text="Login", command=self.validate_login, width=10, bg='#0984e3', fg='white')
        self.login_button.place(x=160, y=200)

    def validate_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Example validation (you can replace this with a database query)
        if username == "admin" and password == "password123":
            self.destroy()
            MainMenuWindow()  # Launch the main menu if credentials are correct
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")


# Step 2: Create the Main Menu window using OOP principles
class MainMenuWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FEAS - Fire Evacuation Automation System")
        self.geometry("1024x768")
        self.state('zoomed')  # Full screen
        self.configure(bg='#dfe6e9')

        # Main Heading
        self.main_heading = tk.Label(self, text="FEAS - Fire Evacuation Automation System", font=("Arial", 26, "bold"), fg='#A52A2A',bg='#dfe6e9')
        self.main_heading.place(relx=0.5, rely=0.05, anchor='center')

        # Section 1: Top-left
        self.create_section("House Keeping", 0.05, 0.15, ["Company Setup", "Fire Exits", "Admin Users","DB Structure"], self.run_program1)

        # Section 2: Top-right
        self.create_section("Floor Informtion", 0.55, 0.15, ["Floors Status", "Floor Details"], self.run_program2)

        # Section 3: Bottom-left
        self.create_section("Fire Evacution", 0.05, 0.55, ["Messages Broadcasting",
                                                           "General Broadcasting", "Sensor Monitor",
                                                           "System Message Types",
                                                           "Exit Procedures"], self.run_program3)

        # Section 4: Bottom-right
        self.create_section("Logs and Reports", 0.55, 0.55, ["Find Employee", "Exit Inspection/Status Report"], self.run_program4)

        # Exit Button
        self.exit_button = tk.Button(self, text="Exit", command=self.quit_application, font=("Segoe UI", 12),
                                     bg="#D83B01", fg="white", activebackground="#A52A2A", activeforeground="white",
                                     height=2, width=15)
        self.exit_button.place(relx=0.45, rely=0.9, anchor='center')

        self.mainloop()

    def create_section(self, title, relx, rely, options, command):
        """ Helper function to create sections with headings and dropdown menus """
        section_frame = tk.Frame(self, width=450, height=250, relief="raised", bd=3, bg='#b2bec3')
        section_frame.place(relx=relx, rely=rely)

        section_label = tk.Label(section_frame, text=title, font=("Arial", 14, "bold"), bg='#b2bec3')
        section_label.place(relx=0.5, rely=0.1, anchor='center')

        # Create a combobox
        dropdown = ttk.Combobox(section_frame, values=options, state="readonly", width=30)
        dropdown.place(relx=0.5, rely=0.5, anchor='center')
        dropdown.bind("<<ComboboxSelected>>", lambda event: command(dropdown.get()))

    def run_program1(self, program_name):
        if program_name == "Company Setup":
            subprocess.run(["python", "FCompany.py"])
        elif program_name == "Fire Exits":
            subprocess.run(["python", "FListExits.py"])
        elif program_name == "Admin Users":
            subprocess.run(["python", "FSysAdmin.py"])
        elif program_name == "Admin Users":
            subprocess.run(["python", "FSysAdmin.py"])
        elif program_name == "DB Structure":
            subprocess.run(["python", "FDBStructure.py"])

    def run_program2(self, program_name):
        if program_name == "Floors Status":
            subprocess.run(["python", "FFlrReport.py"])
        elif program_name == "Floor Details":
            subprocess.run(["python", "FFlrDetail2.py"])

    def run_program3(self, program_name):
        if program_name == "Messages Broadcasting":
            subprocess.run(["python", "FBCasting.py"])
        elif program_name == "General Broadcasting":
            subprocess.run(["python", "FBCast.py"])
        elif program_name == "System Message Types":
            subprocess.run(["python", "FMsgType.py"])
        elif program_name == "Sensor Monitor":
            subprocess.run(["python", "FSensorMon.py"])
        elif program_name == "Exit Procedures":
            subprocess.run(["python", "FExitProc.py"])

    def run_program4(self, program_name):
        if program_name == "Find Employee":
            subprocess.run(["python", "FFindEmp.py"])
        elif program_name == "Exit Inspection/Status Report":
            subprocess.run(["python", "FExitRep.py"])
        elif program_name == "System Message Types":
            subprocess.run(["python", "FMsgType.py"])
        elif program_name == "Sensor Monitor":
            subprocess.run(["python", "FSensorMon.py"])

    def quit_application(self):
        self.destroy()


# Step 3: Execute the program, starting with the login window
if __name__ == "__main__":
    login_window = LoginWindow()
    login_window.mainloop()
