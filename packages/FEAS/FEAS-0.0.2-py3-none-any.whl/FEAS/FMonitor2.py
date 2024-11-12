import tkinter as tk
from tkinter import ttk
import random
import time
import threading


# Class to represent sensor data for Fire, Heat, and Smoke with auto-updates
class SensorData:
    def __init__(self, sensor_type, initial_data):
        self.sensor_type = sensor_type
        self.data = initial_data

    def update_data(self):
        # Simulate dynamic updates based on sensor type
        if self.sensor_type == "Fire":
            self.data = random.choice(["No fire detected", "Fire detected!", "Fire hazard near!"])
        elif self.sensor_type == "Heat":
            self.data = f"Temperature: {random.randint(65, 105)}°F"
        elif self.sensor_type == "Smoke":
            self.data = f"Smoke Level: {random.choice(['Low', 'Medium', 'High', 'Critical'])}"


# Logger Class to log sensor data
class SensorLogger:
    def __init__(self, filename="sensor_log.txt"):
        self.filename = filename

    def log_data(self, sensor_type, data):
        with open(self.filename, 'a') as log_file:
            log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {sensor_type}: {data}\n")


# Main GUI class using OOP
class SensorMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Warehouse Safety Monitor")
        self.root.geometry("800x600")
        self.root.config(bg="lightgray")

        # Create sensor objects with initial data
        self.fire_data = SensorData("Fire", "No fire detected")
        self.heat_data = SensorData("Heat", "Temperature: 75°F")
        self.smoke_data = SensorData("Smoke", "Smoke Level: Low")

        # Create logger
        self.logger = SensorLogger()

        # Set up the UI
        self.setup_ui()

        # Start the thread to simulate live sensor data updates
        self.running = True
        self.start_sensor_updates()

    def setup_ui(self):
        # Top frame for the heading
        self.top_frame = tk.Frame(self.root, height=100, bg="lightblue", borderwidth=2, relief="solid")
        self.top_frame.place(relx=0.5, rely=0.05, anchor="n", width=600, height=80)

        self.heading_label = tk.Label(self.top_frame, text="Warehouse Safety Monitoring System",
                                      font=("Arial", 18), bg="lightblue")
        self.heading_label.place(relx=0.5, rely=0.5, anchor="center")

        # Center frames for Fire, Heat, Smoke data
        self.fire_frame = tk.Frame(self.root, height=100, bg="lightcoral", borderwidth=2, relief="solid")
        self.fire_frame.place(relx=0.5, rely=0.3, anchor="center", width=600, height=100)

        self.heat_frame = tk.Frame(self.root, height=100, bg="lightgoldenrod", borderwidth=2, relief="solid")
        self.heat_frame.place(relx=0.5, rely=0.5, anchor="center", width=600, height=100)

        self.smoke_frame = tk.Frame(self.root, height=100, bg="lightgreen", borderwidth=2, relief="solid")
        self.smoke_frame.place(relx=0.5, rely=0.7, anchor="center", width=600, height=100)

        # Bottom frame for Exit button
        self.bottom_frame = tk.Frame(self.root, height=100, bg="lightgray", borderwidth=2, relief="solid")
        self.bottom_frame.place(relx=0.5, rely=0.9, anchor="center", width=600, height=80)

        self.exit_button = tk.Button(self.bottom_frame, text="Exit", font=("Arial", 14), command=self.stop_sensor_updates)
        self.exit_button.place(relx=0.5, rely=0.5, anchor="center")

        # Labels to display sensor data (initial state)
        self.fire_label = tk.Label(self.fire_frame, text=f"{self.fire_data.sensor_type}: {self.fire_data.data}",
                                   font=("Arial", 14), bg="lightcoral")
        self.fire_label.place(relx=0.5, rely=0.5, anchor="center")

        self.heat_label = tk.Label(self.heat_frame, text=f"{self.heat_data.sensor_type}: {self.heat_data.data}",
                                   font=("Arial", 14), bg="lightgoldenrod")
        self.heat_label.place(relx=0.5, rely=0.5, anchor="center")

        self.smoke_label = tk.Label(self.smoke_frame, text=f"{self.smoke_data.sensor_type}: {self.smoke_data.data}",
                                    font=("Arial", 14), bg="lightgreen")
        self.smoke_label.place(relx=0.5, rely=0.5, anchor="center")

    def update_sensor_data(self):
        # Update sensor data and refresh UI
        self.fire_data.update_data()
        self.heat_data.update_data()
        self.smoke_data.update_data()

        # Update labels with new data
        self.fire_label.config(text=f"{self.fire_data.sensor_type}: {self.fire_data.data}")
        self.heat_label.config(text=f"{self.heat_data.sensor_type}: {self.heat_data.data}")
        self.smoke_label.config(text=f"{self.smoke_data.sensor_type}: {self.smoke_data.data}")

        # Log sensor data
        self.logger.log_data(self.fire_data.sensor_type, self.fire_data.data)
        self.logger.log_data(self.heat_data.sensor_type, self.heat_data.data)
        self.logger.log_data(self.smoke_data.sensor_type, self.smoke_data.data)

    def start_sensor_updates(self):
        # Start a thread to update sensor data every 5 seconds
        self.update_thread = threading.Thread(target=self.run_sensor_updates)
        self.update_thread.daemon = True  # Ensure thread exits when the main program does
        self.update_thread.start()

    def run_sensor_updates(self):
        while self.running:
            self.update_sensor_data()
            time.sleep(5)  # Update every 5 seconds

    def stop_sensor_updates(self):
        self.running = False  # Stop the update loop
        self.root.quit()


# Main execution
if __name__ == "__main__":
    root = tk.Tk()

    # Initialize the application
    app = SensorMonitorApp(root)

    # Start the Tkinter event loop
    root.mainloop()
