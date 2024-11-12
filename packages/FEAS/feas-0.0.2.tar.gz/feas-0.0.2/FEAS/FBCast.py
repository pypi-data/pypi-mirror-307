import tkinter as tk
import customtkinter as ctk
import mysql.connector
import pyttsx3
import time
import threading


# Database connection setup
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="MeOnly@007",
        database="feas"
    )


# Text-to-Speech setup
def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


# Main Application Class
class MessageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FEAS Application - Message Display System")
        self.root.geometry("600x400")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("dark-blue")

        self.label_heading = ctk.CTkLabel(self.root, text="System Messages", font=("Arial", 20, "bold"),
                                       text_color='brown',fg_color='#E6DDDD')
        self.label_heading.place(x=220, y=10)

        # Center the frame on the screen
        self.frame = ctk.CTkFrame(self.root, width=500, height=200, corner_radius=10,fg_color='darkgray')
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Label for displaying the message
        self.label = ctk.CTkLabel(self.frame, text="", font=("Arial", 16, "bold"),
                                  text_color="darkblue",wraplength=400,justify="center")
        self.label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Exit button
        self.exit_button = tk.Button(root, text="Exit", font=("Segoe UI", 12), bg="#D83B01", fg="white",
                                     activebackground="#A52A2A", activeforeground="white", command=self.root.quit,
                                     height=2, width=15)
        self.exit_button.place(x=300, y=400)

        # MySQL connection
        self.conn = connect_to_db()

        # Start background thread to update message
        self.run_message_loop()

    def run_message_loop(self):
        self.message_thread = threading.Thread(target=self.display_messages, daemon=True)
        self.message_thread.start()

    def display_messages(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT cmsg FROM tcmp_msgdb where cFlrMsg_id = '02'")
        messages = [row[0] for row in cursor.fetchall()]

        while True:
            for message in messages:
                # Display the message in the frame
                self.label.configure(text=message)

                # Convert message to voice
                threading.Thread(target=speak_text, args=(message,), daemon=True).start()

                # Wait for 15 seconds before showing the next message
                time.sleep(15)

if __name__ == "__main__":
    root = ctk.CTk()
    app = MessageApp(root)
    root.mainloop()
