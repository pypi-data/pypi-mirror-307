import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import time
from threading import Thread


class SystemBroadcastApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FEAS - System Messages Broadcasting")
        self.root.geometry("1000x700+300+100")  # Centered fixed-size window
        self.root.resizable(False, False)  # Disable maximize button

        # MySQL Connection
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="MeOnly@007",
            database="feas"
        )
        self.cursor = self.conn.cursor()

        # Top Frame - Heading
        self.top_frame = tk.Frame(self.root, height=80)
        self.top_frame.place(relx=0.5, rely=0.05, anchor="center")
        self.heading_label = tk.Label(self.top_frame, text="System Messages Broadcasting",
                                      font=("Segoe UI", 18, "bold"))
        self.heading_label.pack()

        # Second Frame (Left Centered Frame)
        self.left_center_frame = tk.Frame(self.root, width=450, height=300)
        self.left_center_frame.place(relx=0.25, rely=0.3, anchor="center")

        # Message Type Label and Dropdown
        self.msg_type_label = tk.Label(self.left_center_frame, text="Select Message Type:")
        self.msg_type_label.place(x=10, y=20)

        self.msg_type_var = tk.StringVar()
        self.msg_type_dropdown = ttk.Combobox(self.left_center_frame, textvariable=self.msg_type_var, width=35,
                                              state="readonly")
        self.msg_type_dropdown.place(x=150, y=20)

        self.load_message_types()  # Load dropdown options from database
        self.msg_type_dropdown.bind("<<ComboboxSelected>>", self.load_treeview_data)

        # Treeview for displaying selected message details
        self.tree_frame = tk.Frame(self.left_center_frame, width=500, height=400)
        self.tree_frame.place(x=18, y=80)

        self.msg_tree = ttk.Treeview(self.tree_frame, columns=("Message"), show="headings", height=7)
        self.msg_tree.heading("Message", text="System Messages")
        self.msg_tree.column("Message", width=400, anchor="center")
        self.msg_tree.bind("<Double-1>", self.on_treeview_double_click)

        # Scrollbar for Treeview
        self.scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.msg_tree.yview)
        self.msg_tree.configure(yscroll=self.scrollbar.set)
        self.msg_tree.pack(side="left")
        self.scrollbar.pack(side="right", fill="y")

        # Bottom Frame - Editing Selected Message
        self.bottom_center_frame = tk.Frame(self.root, width=750, height=110)
        self.bottom_center_frame.place(relx=0.5, rely=0.75, anchor="center")

        self.broadcast_label = tk.Label(self.bottom_center_frame, text="Broadcast Message:")
        self.broadcast_label.place(x=10, y=10)

        self.broadcast_entry = tk.Entry(self.bottom_center_frame, width=50)
        self.broadcast_entry.place(x=150, y=10)

        # Save and Exit Buttons
        self.broadcast_button = tk.Button(self.bottom_center_frame, text="Broadcast",
                                          command=self.start_broadcast,font=("Segoe UI", 12), bg="#0078D7", fg="white",
                                          activebackground="#005A9E", activeforeground="white", height=2, width=15)
        self.broadcast_button.place(x=150, y=50)

        self.exit_button = tk.Button(self.bottom_center_frame, text="Exit", font=("Segoe UI", 12), bg="#D83B01",
                                     fg="white", activebackground="#A52A2A", activeforeground="white",
                                     command=self.root.quit, height=2, width=15)
        self.exit_button.place(x=350, y=50)

        # Right Center Frame - Progress Information
        self.right_center_frame = tk.Frame(self.root, width=700, height=350)
        self.right_center_frame.place(relx=0.72, rely=0.3, anchor="center")

        self.progress_label = tk.Label(self.right_center_frame, text="Current Progress", font=("Segoe UI", 12, "bold"))
        self.progress_label.pack(anchor="n")

        self.progress_text = tk.Text(self.right_center_frame, height=12, width=65, state="disabled")
        self.progress_text.pack()

    def load_message_types(self):
        """Load message types from tcmp_flrmsgs into the dropdown menu."""
        self.cursor.execute("SELECT CONCAT(cFlrMsg_ID, '-', cFlrMsg_Desc) FROM tcmp_flrmsgs")
        rows = self.cursor.fetchall()
        message_types = [row[0] for row in rows]
        self.msg_type_dropdown["values"] = message_types

    def load_treeview_data(self, event):
        """Load messages in the treeview based on selected message type."""
        selected_type = self.msg_type_var.get()
        msg_id = selected_type.split("-")[0].strip()

        self.cursor.execute("SELECT cMsg FROM tcmp_msgdb WHERE cFlrMsg_ID = %s", (msg_id,))
        rows = self.cursor.fetchall()

        # Clear treeview
        for item in self.msg_tree.get_children():
            self.msg_tree.delete(item)

        # Insert new rows
        for row in rows:
            self.msg_tree.insert("", "end", values=(row[0],))

    def on_treeview_double_click(self, event):
        """Handle double click event to edit message."""
        selected_item = self.msg_tree.selection()[0]
        selected_msg = self.msg_tree.item(selected_item, "values")[0]
        self.broadcast_entry.delete(0, tk.END)
        self.broadcast_entry.insert(0, selected_msg)
        self.broadcast_button.config(state="normal")

    def start_broadcast(self):
        """Start broadcasting message in the progress information section."""
        message = self.broadcast_entry.get()
        if not message:
            messagebox.showerror("Error", "Broadcast message cannot be empty.")
            return

        self.progress_text.config(state="normal")
        self.progress_text.delete(1.0, tk.END)

        # Messages to broadcast in progress bar
        broadcast_steps = [
            "Broadcasting message to the managers and supervisors...",
            "Dispatching evacuation routes to team leaders...",
            "Broadcasting message to the Associates...",
            "Broadcasting message to the working stations...",
            "Broadcasting message to the big screen...",
            "Turning Red Light on All Exit gates...",
            "Dispatching to the emergency department...",
            "Initializing the Emergency Alarams...",
            "Creating log for the event..."
        ]

        # Threaded Broadcast Simulation
        def broadcast_simulation():
            for step in broadcast_steps:
                self.progress_text.insert(tk.END, f"{step}\n")
                self.progress_text.yview(tk.END)
                time.sleep(1)  # Simulate delay for each broadcast step
            self.progress_text.insert(tk.END, "Broadcast Successfully Completed.\n")
            self.progress_text.config(state="disabled")

        Thread(target=broadcast_simulation).start()


# Main Program
if __name__ == "__main__":
    root = tk.Tk()
    app = SystemBroadcastApp(root)
    root.mainloop()