import tkinter as tk
from tkinter import messagebox


class FeasMsgCls:
    def __init__(self, root=None):
        """
        Initialize the message box class.
        Args:
            root: Tkinter root or any other Tkinter widget (Optional)
        """
        self.root = root if root else tk.Tk()
        self.root.withdraw()  # Hide the main window

    def info(self, title, message):
        """
        Display an informational message.
        Args:
            title: Title of the info dialog box
            message: Informational message
        """
        messagebox.showinfo(title, message)

    def warning(self, title, message):
        """
        Display a warning message.
        Args:
            title: Title of the warning dialog box
            message: Warning message
        """
        messagebox.showwarning(title, message)

    def error(self, title, message):
        """
        Display an error message.
        Args:
            title: Title of the error dialog box
            message: Error message
        """
        title = "FEAS Application - " + title
        messagebox.showerror(title, message)

    def confirm(self, title, message):
        """
        Display a confirmation dialog with Yes/No options.
        Args:
            title: Title of the confirmation dialog
            message: Confirmation message
        Returns:
            bool: True if 'Yes' is clicked, False if 'No' is clicked
        """
        return messagebox.askyesno(title, message)


# Example usage in a separate application
#if __name__ == "__main__":
#    # Initialize the root for Tkinter
#    root = tk.Tk()
#    root.withdraw()  # Hide the main window

    # Create an instance of the MessageBox class
#    msg_box = (FeasMsgCls(root))

    # Example usage
#    msg_box.info("Information", "This is an informational message.")
#    msg_box.warning("Warning", "This is a warning message.")
#    msg_box.error("Error", "An error has occurred!")

#    response = msg_box.confirm("Confirmation", "Are you sure you want to proceed?")
#    if response:
#        msg_box.info("Confirmed", "You selected 'Yes'.")
#    else:
#        msg_box.info("Cancelled", "You selected 'No'.")

    # Close the root window
#    root.quit()