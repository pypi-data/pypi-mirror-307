import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector


class SystemMessagesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FEAS- System Messages Type")
        self.root.geometry("800x600+300+100")  # Centered screen with fixed dimensions
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
        self.top_frame = tk.Frame(self.root, height=100)
        self.top_frame.place(relx=0.5, rely=0.05, anchor="center")
        self.heading_label = tk.Label(self.top_frame, text="System Messages Type", font=("Segoe UI", 18, "bold"))
        self.heading_label.pack()

        # Center Frame - Treeview for Messages List
        self.center_frame = tk.Frame(self.root)
        self.center_frame.place(relx=0.5, rely=0.4, anchor="center")

        # Treeview Setup
        self.msg_tree = ttk.Treeview(self.center_frame, columns=("ID", "Description"), show="headings", height=15)
        self.msg_tree.heading("ID", text="Message ID")
        self.msg_tree.heading("Description", text="Floor Message Type")
        self.msg_tree.column("ID", width=150, anchor="center")
        self.msg_tree.column("Description", width=250, anchor="center")
        self.msg_tree.bind("<Double-1>", self.on_treeview_double_click)

        # Scrollbar for Treeview
        self.scrollbar = ttk.Scrollbar(self.center_frame, orient="vertical", command=self.msg_tree.yview)
        self.msg_tree.configure(yscroll=self.scrollbar.set)

        self.msg_tree.pack(side="left")
        self.scrollbar.pack(side="right", fill="y")

        # Bottom Frame - Add, Save, and Exit Buttons
        self.bottom_frame = tk.Frame(self.root, height=600,width=600)
        self.bottom_frame.place(relx=0.5, rely=0.85, anchor="center")

        # Editable Fields in Bottom Frame
        self.id_label = tk.Label(self.bottom_frame, text="Message ID:", anchor="w")
        self.id_label.place(x=150, y=100)
        self.id_entry = tk.Entry(self.bottom_frame)
        self.id_entry.place(x=270, y=100, width=120)

        self.desc_label = tk.Label(self.bottom_frame, text="Floor Message Type:", anchor="w")
        self.desc_label.place(x=150, y=120)
        self.desc_entry = tk.Entry(self.bottom_frame)
        self.desc_entry.place(x=270, y=120, width=220)

        # Load Initial Data
        self.load_data()


        self.save_button = tk.Button(self.bottom_frame,text="Save", font=("Segoe UI", 12), bg="#0078D7", fg="white",
                                     activebackground="#005A9E", activeforeground="white", command=self.save_data,
                                     height=2, width=15)
        self.save_button.place(x=100, y=200)

        self.exit_button = tk.Button(self.bottom_frame, text="Exit", font=("Segoe UI", 12), bg="#D83B01", fg="white",
                                activebackground="#A52A2A", activeforeground="white", command=self.root.quit,
                                height=2, width=15)
        self.exit_button.place(x=280, y=200)


    def load_data(self):
        """Load system messages from the database and display in the treeview."""
        for row in self.msg_tree.get_children():
            self.msg_tree.delete(row)

        self.cursor.execute("SELECT cFlrMsg_ID, cFlrMsg_Desc FROM tcmp_flrmsgs")
        for row in self.cursor.fetchall():
            self.msg_tree.insert("", "end", values=row)

    def on_treeview_double_click(self, event):
        """Fill in the entry fields with the selected item for editing."""
        selected_item = self.msg_tree.selection()[0]
        msg_id, msg_desc = self.msg_tree.item(selected_item, "values")
        self.id_entry.delete(0, tk.END)
        self.id_entry.insert(0, msg_id)
        self.desc_entry.delete(0, tk.END)
        self.desc_entry.insert(0, msg_desc)
        self.save_button.config(state="normal")

    def save_data(self):
        """Save or update data in the database."""
        msg_id = self.id_entry.get()
        msg_desc = self.desc_entry.get()

        if not msg_id or not msg_desc:
            messagebox.showerror("Error", "Both fields are required.")
            return

        # Check if the ID already exists
        self.cursor.execute("SELECT cFlrMsg_ID FROM tcmp_flrmsgs WHERE cFlrMsg_ID = %s", (msg_id,))
        exists = self.cursor.fetchone()

        if exists:
            # Update existing record
            self.cursor.execute("UPDATE tcmp_flrmsgs SET cFlrMsg_Desc = %s WHERE cFlrMsg_ID = %s", (msg_desc, msg_id))
            self.conn.commit()
            messagebox.showinfo("Updated", "Data Updated...")
        else:
            # Insert new record
            self.cursor.execute("INSERT INTO tcmp_flrmsgs (cFlrMsg_ID, cFlrMsg_Desc) VALUES (%s, %s)",
                                (msg_id, msg_desc))
            self.conn.commit()
            messagebox.showinfo("Saved", "Data Saved...")

        self.load_data()
        self.save_button.config(state="disabled")

    def close_app(self):
        """Close the database connection and quit the application."""
        self.cursor.close()
        self.conn.close()
        self.root.quit()


# Main Program
if __name__ == "__main__":
    root = tk.Tk()
    app = SystemMessagesApp(root)
    root.mainloop()
