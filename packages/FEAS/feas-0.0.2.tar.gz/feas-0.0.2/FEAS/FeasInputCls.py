import tkinter
import tkinter as tk


class FeasInputCls:
    def __init__(self, root, default_text="", font=("Arial", 12), fg="black", bg="white", width=20, show=None):
        self.entry = tk.Entry(root, font=font, fg=fg, bg=bg, width=width, show=show)
        self.entry.insert(0, default_text)  # Set default text if provided

    def get_value(self):
        """Returns the current value in the entry field."""
        return self.entry.get()

    def set_value(self, text):
        """Sets a new value in the entry field."""
        self.entry.delete(0, tk.END)
        self.entry.insert(0, text)

    def clear(self):
        """Clears the text in the entry field."""
        self.entry.delete(0, tk.END)


    def place(self, **kwargs):
        """Places the entry widget with optional layout options."""
        self.entry.place(**kwargs)

    def configure(self, **kwargs):
        """Allows dynamic configuration of the entry field."""
        self.entry.config(**kwargs)

    def print_values(self):
        """Method to print values from the input fields."""
        print("Text Input 1:", self.text_input1.get_value())
        print("Text Input 2:", self.text_input2.get_value())

    def lbl_factory(self, frm, text, font=('Arial', 12),fg="brown", bg="white", padx=5, pady=5)-> tkinter.Label:
        self.lbl = tkinter.label(frm, text, font=font, fg=fg, bg=bg, padx=padx, pady=pady)
        return self.lbl

    def place(self, **kwargs):
        self.label.place(**kwargs)

#    def configure(self, **kwargs):


        """
        # TextInputFactory Class: A reusable class for creating input fields (Tkinter Entry widgets) with customizable options such as default text, font, colors, and password masking.
        # Methods:
        # get_value(): Retrieves the current value from the entry field.
        # set_value(): Sets a new value in the entry field.
        # clear(): Clears the content of the entry field.
        # pack(), grid(), place(): Standard Tkinter layout methods.
        # configure(): Dynamically configure the entry widget properties.
        # How to Use:
        # Instantiate TextInputFactory to create text input fields.
        # Use get_value() to fetch the current value, set_value() to update the input, and clear() to reset the field.
        
        
        # Example of usage in another class
        
                # Using TextInputFactory to create input fields
        #        self.text_input1 = TextInputFactory(self.root, default_text="Enter your name")
        #        self.text_input1.pack(pady=10)
        
        #        self.text_input2 = TextInputFactory(self.root, default_text="Password", show="*")
        #        self.text_input2.pack(pady=10)
        
                # Button to print the values of the input fields
        #        self.print_button = tk.Button(self.root, text="Print Values", command=self.print_values)
        #        self.print_button.pack(pady=10)
        
        """
