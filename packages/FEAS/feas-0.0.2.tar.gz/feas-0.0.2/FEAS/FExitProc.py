import tkinter as tk
from tkinter import ttk


# Class for each floor's evacuation details
class Floor:
    def __init__(self, number, manager, supervisors, exit_strategy):
        self.number = number
        self.manager = manager
        self.supervisors = supervisors
        self.exit_strategy = exit_strategy


# Class to represent the emergency scenario
class Emergency:
    def __init__(self, reason):
        self.reason = reason


# Main Evacuation Plan Controller
class EvacuationPlan:
    def __init__(self, root, emergency_file):
        self.root = root
        self.root.title("FEAS - Fire Evacuation Plan")
        self.root.geometry("800x600")
        self.emergency_file = emergency_file
        self.floors = []
        self.emergency = None

        # Set up the main frames and widgets using .place() function
        self.setup_main_window()

        # Read the emergency details from the file
        self.load_emergency_plan()

    def setup_main_window(self):
        # Top Frame for Emergency Reason
        self.top_frame = tk.Frame(self.root, height=100, bg="white", borderwidth=2, relief="solid")
        self.top_frame.place(relx=0.5, y=20, anchor="n", width=760, height=80)

        self.emergency_label = tk.Label(
            self.top_frame, text="Emergency Situation", font=("Arial", 18), bg="white")
        self.emergency_label.place(relx=0.5, rely=0.5, anchor="center")

        # Frames for each floor
        self.floor_frames = []
        for i in range(4):
            frame = tk.Frame(self.root, borderwidth=2, relief="solid", bg="white")
            frame.place(x=20, y=120 + i * 110, width=760, height=100)
            self.floor_frames.append(frame)
        # Exit button
    #    self.exit_button = tk.Button(root, text="Exit", font=("Segoe UI", 12), bg="#D83B01", fg="white",
    #                                 activebackground="#A52A2A", activeforeground="white", command=self.root.quit,
    #                                 height=2, width=15)
    #    self.exit_button.place(x=300, y=800)

    def load_emergency_plan(self):
        # Load emergency and floor data from the text file
        try:
            with open(self.emergency_file, 'r') as file:
                lines = file.readlines()

                # First line contains the emergency reason
                self.emergency = Emergency(lines[0].strip())
                self.emergency_label.config(text=f"Emergency: {self.emergency.reason}")

                # Remaining lines contain floor info
                for i in range(1, len(lines), 4):  # Assuming 4 lines per floor
                    floor_number = lines[i].strip()
                    manager = lines[i + 1].strip()
                    supervisors = lines[i + 2].strip()
                    exit_strategy = lines[i + 3].strip()

                    # Create a Floor object and store it
                    floor = Floor(floor_number, manager, supervisors, exit_strategy)
                    self.floors.append(floor)

                # Display floor plans in the UI
                self.update_floor_ui()

        except FileNotFoundError:
            print(f"Error: File '{self.emergency_file}' not found.")

    def update_floor_ui(self):
        # Loop through each floor and update the respective frame
        for i, floor in enumerate(self.floors):
            if i < len(self.floor_frames):
                frame = self.floor_frames[i]
                for widget in frame.winfo_children():
                    widget.destroy()  # Clear previous content

                floor_label = tk.Label(frame, text=f"Floor {floor.number}", font=("Arial", 14), bg="white")
                floor_label.place(x=10, y=10)

                manager_label = tk.Label(frame, text=f"Manager: {floor.manager}", bg="white")
                manager_label.place(x=10, y=40)

                supervisors_label = tk.Label(frame, text=f"Supervisors: {floor.supervisors}", bg="white")
                supervisors_label.place(x=250, y=40)

                exit_strategy_label = tk.Label(frame, text=f"Exit Strategy: {floor.exit_strategy}", bg="white")
                exit_strategy_label.place(x=500, y=40)


# Main execution
if __name__ == "__main__":
    root = tk.Tk()

    # Path to the text file that holds evacuation details
    emergency_file = "evacuation_plan.txt"  # Make sure this file exists

    # Initialize the Evacuation Plan GUI
    app = EvacuationPlan(root, emergency_file)

    # Start the Tkinter event loop
    root.mainloop()
