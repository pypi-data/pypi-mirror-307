import tkinter as tk
from tkinter import messagebox
import os
import requests

class ErrHandling2:
    def __init__(self, root):
        self.root = root
        self.root.title("Error Handling Demo")
        self.root.geometry("400x300")

        # UI Elements
        self.create_widgets()

    def create_widgets(self):
        # File Operation Example
        tk.Button(self.root, text="Read Non-existent File", command=self.read_file).pack(pady=10)

        # Division by Zero Example
        tk.Button(self.root, text="Divide by Zero", command=self.divide_by_zero).pack(pady=10)

        # Network Request Example
        tk.Button(self.root, text="Make Network Request", command=self.make_network_request).pack(pady=10)

        # Input Validation Example
        tk.Label(self.root, text="Enter an integer:").pack(pady=5)
        self.integer_input = tk.Entry(self.root)
        self.integer_input.pack(pady=5)
        tk.Button(self.root, text="Validate Input", command=self.validate_input).pack(pady=10)

    def read_file(self):
        try:
            # Attempting to read a non-existent file
            with open("non_existent_file.txt", "r") as file:
                content = file.read()
            messagebox.showinfo("Success", "File read successfully!")
        except FileNotFoundError:
            messagebox.showerror("File Error", "File not found! Please check the file path.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    def divide_by_zero(self):
        try:
            # Attempting to divide by zero
            result = 10 / 0
            messagebox.showinfo("Success", f"Result: {result}")
        except ZeroDivisionError:
            messagebox.showerror("Math Error", "Cannot divide by zero!")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    def make_network_request(self):
        try:
            # Attempting to make a network request
            response = requests.get("https://httpbin.org/status/404")
            response.raise_for_status()
            messagebox.showinfo("Success", "Network request was successful!")
        except requests.exceptions.HTTPError as http_err:
            messagebox.showerror("Network Error", f"HTTP error occurred: {http_err}")
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Network Error", "Failed to connect to the server. Check your network connection.")
        except requests.exceptions.Timeout:
            messagebox.showerror("Network Error", "The request timed out.")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Network Error", f"An unexpected error occurred: {str(e)}")

    def validate_input(self):
        try:
            # Attempting to validate input as an integer
            user_input = self.integer_input.get()
            user_number = int(user_input)
            messagebox.showinfo("Success", f"Valid input: {user_number}")
        except ValueError:
            messagebox.showerror("Input Error", "Invalid input! Please enter a valid integer.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ErrHandling2(root)
    root.mainloop()
