import tkinter as tk
from tkinter import messagebox
import datetime


class MsgFormat:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the main Tkinter window since we don't need it

    def format_text(self, text, case='title', align='left', width=50, fill_char=' '):
        """
        Format text by changing case and alignment.

        :param text: The text to format
        :param case: 'upper', 'lower', 'title', or 'capitalize'
        :param align: 'left', 'right', or 'center'
        :param width: The width to align within
        :param fill_char: The character to fill the space with
        :return: Formatted text
        """
        if case == 'upper':
            text = text.upper()
        elif case == 'lower':
            text = text.lower()
        elif case == 'title':
            text = text.title()
        elif case == 'capitalize':
            text = text.capitalize()

        if align == 'left':
            formatted_text = text.ljust(width, fill_char)
        elif align == 'right':
            formatted_text = text.rjust(width, fill_char)
        elif align == 'center':
            formatted_text = text.center(width, fill_char)

        return formatted_text

    def format_number(self, number, precision=2, currency=False, thousand_sep=True):
        """
        Format a number with precision, currency, and thousand separators.

        :param number: The number to format
        :param precision: Number of decimal places
        :param currency: If True, formats as currency
        :param thousand_sep: If True, adds thousand separators
        :return: Formatted number as a string
        """
        if thousand_sep:
            formatted_number = f"{number:,.{precision}f}"
        else:
            formatted_number = f"{number:.{precision}f}"

        if currency:
            formatted_number = f"${formatted_number}"

        return formatted_number

    def format_date(self, date, format="%Y-%m-%d"):
        """
        Format a date.

        :param date: The date to format (as a datetime object)
        :param format: The format string
        :return: Formatted date as a string
        """
        if isinstance(date, datetime.date):
            return date.strftime(format)
        else:
            raise ValueError("Input must be a datetime.date or datetime.datetime object")

    def display_message(self, title, message):
        """
        Display a message using Tkinter messagebox.

        :param title: The title of the message box
        :param message: The message content
        """
        messagebox.showinfo(title, message)


# Example Usage
if __name__ == "__main__":
    formatter = MsgFormat()

    # Example of formatting text
    formatted_text = formatter.format_text("Hello, World!", case='upper', align='center', width=30)
    formatter.display_message("Formatted Text", formatted_text)

    # Example of formatting number
    formatted_number = formatter.format_number(1234567.89123, precision=2, currency=True)
    formatter.display_message("Formatted Number", formatted_number)

    # Example of formatting date
    today = datetime.date.today()
    formatted_date = formatter.format_date(today, format="%B %d, %Y")
    formatter.display_message("Formatted Date", formatted_date)
