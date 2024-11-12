import tkinter as tk
import time
from tkinter import messagebox
import customtkinter as ctk
import random
from datetime import datetime

# Mocking machine learning prediction and sensor data
def mock_predict_event():
    """Simulates machine learning prediction based on sensor data."""
    events = ['Normal', 'Fire', 'Smoke', 'Heat']
    locations = ['South', 'North', 'East', 'West', 'Southeast', 'Southwest', 'Northeast', 'Northwest']
    event = random.choice(events)
    location = random.choice(locations)
    return event, location

def get_mock_data():
    """Generates mock sensor data for fire, heat, smoke and temperature."""
    fire = random.uniform(0, 1)  # Mock fire sensor value
    smoke = random.uniform(0, 1)  # Mock smoke sensor value
    heat = random.uniform(0, 100)  # Mock heat sensor value
    temp = random.uniform(20, 50)  # Mock temperature (Celsius)
    return fire, smoke, heat, temp

# Logging function for emergency events
def log_event(event_type, location):
    with open('emergency_log.txt', 'a') as f:
        log_entry = f"{datetime.now()} - Event: {event_type}, Location: {location}\n"
        f.write(log_entry)

# Step 1: Create the main application window
class SensorMonitorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FEAS- Fire, Heat, and Smoke Monitoring System")
        self.geometry("1024x768")
        self.configure(bg='#dfe6e9')
        self.state('zoomed')  # Full screen

        # Main heading at the top
        self.heading = tk.Label(self, text="FEAS - Live Fire, Heat, and Smoke Monitoring", font=("Arial", 20, "bold"), fg='brown', bg='#dfe6e9')
        self.heading.place(relx=0.5, rely=0.05, anchor='center')

        # Vertical Frames for Fire, Heat, Smoke, and Temperature Data
        self.fire_frame = self.create_frame("Fire Sensor Data", 0.2)
        self.heat_frame = self.create_frame("Heat Sensor Data", 0.5)
        self.smoke_frame = self.create_frame("Smoke Sensor Data", 0.8)

        # Create Exit Button
        self.exit_button = tk.Button(self, text="Exit", command=self.quit_application, width=15, height=2,
                                     bg='#e74c3c', fg='white',font=("Segoe UI", 12, "bold"))
        self.exit_button.place(relx=0.5, rely=0.9, anchor='center')

        # Refresh Data every 10 seconds
        self.refresh_data()

    def create_frame(self, title, relx):

        """Helper function to create frames with headings."""
        frame = tk.Frame(self, width=300, height=500, relief="raised", bd=3, bg='#b2bec3')
        frame.place(relx=relx, rely=0.5, anchor='center')

        label = tk.Label(frame, text=title, font=("Arial", 14, "bold"), bg='#b2bec3')
        label.place(relx=0.5, rely=0.1, anchor='center')

        # Value label where data will be updated
        value_label = tk.Label(frame, text="Waiting for data...", font=("Arial", 12), bg='#b2bec3')
        value_label.place(relx=0.5, rely=0.5, anchor='center')

        return value_label

    def refresh_data(self):
        """Fetch and display updated sensor data every 10 seconds."""
        fire, smoke, heat, temp = get_mock_data()

        # Update sensor data on frames
        self.fire_frame.config(text=f"Fire Intensity: {fire:.2f}")
        self.heat_frame.config(text=f"Heat Level: {heat:.2f} \nTemperature: {temp:.2f}°C")
        self.smoke_frame.config(text=f"Smoke Intensity: {smoke:.2f} °C")

        # Machine Learning model prediction
        event, location = mock_predict_event()

        if event != 'Normal':
            self.handle_emergency(event, location)

        # Refresh data every 10 seconds
        self.after(10000, self.refresh_data)

    def handle_emergency(self, event_type, location):
        """Handles emergency situations by alerting the user and logging the event."""
        # Create an emergency message
        alert_msg = f"Emergency detected! Event: {event_type}, Location: {location}"
        messagebox.showwarning("Emergency Alert", alert_msg)

        # Log the event
        log_event(event_type, location)

        # Placeholder for live camera feed logic (to be implemented)
        print(f"Displaying camera feed for {location}...")

    def quit_application(self):
        """Exit the application."""
        self.destroy()

# Step 2: Execute the program
if __name__ == "__main__":
    app = SensorMonitorApp()
    app.mainloop()
