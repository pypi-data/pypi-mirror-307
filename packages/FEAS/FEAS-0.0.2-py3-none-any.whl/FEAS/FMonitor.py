import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import time
import threading


# Create a class for the application
class FMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("FEAS Application - Fire/Heat/Smoke Monitoring System")
        self.root.geometry("840x400")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")


        self.root.resizable(False, False)
        self.root.eval('tk::PlaceWindow . center')  # Place window in the center of the screen
        #self.root.overrideredirect(True)  # Disable close, resize, max button

        # Create a frame for the application
        self.frame = ctk.CTkFrame(self.root, width=800, height=400, corner_radius=10)
        self.frame.pack(fill="both", expand=True)

        self.create_frames()


        # Labels to show data
        self.label_heading = ctk.CTkLabel(self.root, text="System Warnings", font=("Arial", 20, "bold"),
                                       text_color='brown',fg_color='#E6DDDD')
        self.label_heading.place(x=350, y=10)

        self.label_heat = ctk.CTkLabel(self.frame_heat, text="Heat Data", font=("Arial", 16, "bold"),text_color='yellow')
        self.label_heat.place(x=80, y=10)

        self.label_smoke = ctk.CTkLabel(self.frame_smoke, text="Smoke Data", font=("Arial", 16, "bold"),text_color='yellow')
        self.label_smoke.place(x=80, y=10)

        self.label_fire = ctk.CTkLabel(self.frame_fire, text="Fire Data", font=("Arial", 16, "bold"),text_color='yellow')
        self.label_fire.place(x=80, y=10)

        # Create Text fields to display file contents
        self.heat_display = ctk.CTkLabel(self.frame_heat, text="", anchor="nw", justify="left", font=("Arial", 14),text_color='white')
        self.heat_display.place(x=20, y=50)

        self.smoke_display = ctk.CTkLabel(self.frame_smoke, text="", anchor="nw", justify="left", font=("Arial", 14),text_color='white')
        self.smoke_display.place(x=20, y=50)

        self.fire_display = ctk.CTkLabel(self.frame_fire, text="", anchor="nw", justify="left", font=("Arial", 14),text_color='white')
        self.fire_display.place(x=20, y=50)

        # Exit button
        self.exit_button = ctk.CTkButton(root, text="Exit", command=self.root.quit)
        self.exit_button.place(x=375, y=360)

        # Start background thread to monitor files
        self.run_monitor()

    def display_data(self, data, label, title):
        label.configure(text=data, font=("Arial", 14),text_color='white')
        label.configure(text=title, font=("Arial", 16),text_color='white')

    def create_frames(self):
        # Create Frames to show data from the files
        self.frame_heat = ctk.CTkFrame(self.root, width=250, height=300, corner_radius=10, fg_color="#3D85C6")
        self.frame_heat.place(x=50, y=50)

        self.frame_smoke = ctk.CTkFrame(self.root, width=250, height=300, corner_radius=1, fg_color="#3D85C6")
        self.frame_smoke.place(x=320, y=50)

        self.frame_fire = ctk.CTkFrame(self.root, width=250, height=300, corner_radius=10, fg_color="#3D85C6")
        self.frame_fire.place(x=580, y=50)

    def run_monitor(self):
        self.monitor_thread = threading.Thread(target=self.monitor_files, daemon=True)
        self.monitor_thread.start()

    def monitor_files(self):
        while True:
            self.check_files()
            time.sleep(5)

    def check_files(self):
        # Read and display data from the files
        heat_data = self.read_file("heat_data.txt")
        smoke_data = self.read_file("smoke_data.txt")
        fire_data = self.read_file("fire_data.txt")

        # Display data in frames
        self.display_data(heat_data, self.heat_display, "Heat Data")
        self.display_data(smoke_data, self.smoke_display, "Smoke Data")
        self.display_data(fire_data, self.fire_display, "Fire Data")

    def read_file(self, filename):
        with open(filename, 'r') as file:
            return [line.strip() for line in file.readlines()]

    def display_data(self, data, label_widget, heading):
        # Count consecutive '1's in the data
        consecutive_ones = 0
        text_display = ""
        for line in data:
            if line == '1':
                consecutive_ones += 1
            else:
                consecutive_ones = 0

            # If 3 consecutive '1's are found, change the text color to red
            if consecutive_ones >= 3:
                label_widget.configure(text_color="#E06666")
                text_display += f"{line} ◄\n"
                self.alert_warning(heading)
            else:
                label_widget.configure(text_color="white")
                text_display += f"{line}\n"

        label_widget.configure(text=text_display)

    def alert_warning(self, heading):
        messagebox.showwarning("FEAS Application - Warning", f"warning is Consistent,  '1' number is repeated 3 times found in {heading}!")


if __name__ == "__main__":
    root = ctk.CTk()
    app = FMonitor(root)
    root.mainloop()
