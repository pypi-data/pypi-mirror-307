import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage


# OopCompanion:suppressRename


"""

        create a reusable, object-oriented Python module that can be used in any Tkinter-based application to display messages to the user with standardized headings, colors, pictures, and patterns, we'll structure the code into a class that can be easily instantiated and used across different modules.
        This module will feature:
        •	Standardized Message Display: Each message will have a consistent layout with a heading, body text, and optional image.
        •	Customizable Design: The colors, font styles, and patterns can be set to fit the application's theme.
        •	Ease of Integration: The class can be easily imported and used in any Tkinter-based application.


"""


class MsgHandling:
    def __init__(self, root, app_name="My Application",
                 heading_color="#333333",
                 message_color="#000000",
                 background_color="#FFFFFF",
                 heading_font=("Arial", 16, "bold"),
                 message_font=("Arial", 12),
                 icon_path=None):
        """
        Initialize the MessageDisplay with standardized settings.

        :param root: The root Tkinter window.
        :param app_name: Name of the application.
        :param heading_color: Color of the heading text.
        :param message_color: Color of the message text.
        :param background_color: Background color of the message box.
        :param heading_font: Font of the heading text.
        :param message_font: Font of the message text.
        :param icon_path: Path to the icon image to be displayed.
        """
        self.root = root
        self.app_name = app_name
        self.heading_color = heading_color
        self.message_color = message_color
        self.background_color = background_color
        self.heading_font = heading_font
        self.message_font = message_font
        # self.icon = PhotoImage(file=icon_path) if icon_path else None

    def show_info(self, heading, message):
        """Display an informational message."""
        self._display_message(heading, message, "info")

    def show_warning(self, heading, message):
        """Display a warning message."""
        self._display_message(heading, message, "warning")

    def show_error(self, heading, message):
        """Display an error message."""
        self._display_message(heading, message, "error")

    def _display_message(self, heading, message, msg_type):
        """Internal method to create and display the message box."""
        msg_box = tk.Toplevel(self.root)
        msg_box.title(f"{self.app_name} - {msg_type.capitalize()}")
        msg_box.configure(bg=self.background_color)

        # if self.icon:
        #    icon_label = tk.Label(msg_box, image=self.icon, bg=self.background_color)
        #    icon_label.pack(side="left", padx=10, pady=10)

        heading_label = tk.Label(msg_box, text=heading,
                                 fg=self.heading_color,
                                 bg=self.background_color,
                                 font=self.heading_font)
        heading_label.pack(pady=(10, 5))

        message_label = tk.Label(msg_box, text=message,
                                 fg=self.message_color,
                                 bg=self.background_color,
                                 font=self.message_font,
                                 wraplength=400, justify="left")
        message_label.pack(pady=(0, 10))

        btn = tk.Button(msg_box, text="OK", command=msg_box.destroy, padx=10, pady=5)
        btn.pack(pady=(0, 10))

        msg_box.transient(self.root)
        msg_box.grab_set()
        self.root.wait_window(msg_box)


# Usage example:
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    message_display = MsgHandling(root,
                                     app_name="Example App",
                                     heading_color="#2E8B57",
                                     message_color="#4F4F4F",
                                     background_color="#F0F0F0",
                                     heading_font=("Helvetica", 14, "bold"),
                                     message_font=("Helvetica", 10),
                                     icon_path="icon.png")  # Provide path to an icon if available

    # Example messages
    message_display.show_info("Welcome", "This is an informational message.")
    message_display.show_warning("Warning", "This is a warning message.")
    message_display.show_error("Error", "This is an error message.")

    root.mainloop()
"""

    Explanation:
        1.	MessageDisplay Class: This class encapsulates all the functionality needed to display messages with a standardized look.
        2.	Customization: When creating an instance of MessageDisplay, you can customize colors, fonts, and even add an icon. This allows the messages to align with the application's branding.
        3.	Methods:
            o	show_info: Displays an informational message.
            o	show_warning: Displays a warning message.
            o	show_error: Displays an error message.
        4.	Internal _display_message Method: Handles the layout and display of the message, ensuring consistency across different types of messages.
        5.	Usage Example: The script demonstrates how to use this module in a Tkinter application.
        Integration:
            •	You can import this module into any Tkinter application and use it to display standardized messages. Just instantiate the MessageDisplay class with your desired parameters and call the appropriate method when you need to display a message.
    This structure allows you to maintain a consistent look and feel across your application’s message dialogs, making the user experience more cohesive.


"""