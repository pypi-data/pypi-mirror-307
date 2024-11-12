import customtkinter
import tkinter as tk


class FeasLblCls:
    def __init__(self, root, text, font=("Arial", 12), fg="black", bg="white", padx=5, pady=5):
        self.label = tk.Label(
            root, text=text,
            font=font,
            fg=fg,
            bg=bg,
            padx=padx,
            pady=pady
        )

    def place(self, **kwargs):
        self.label.place(**kwargs)


"""
# usage
#self.label2 = LabelFactory(self.root, text="Tkinter Label Factory", font=("Arial", 14), bg="yellow")
#        self.label2.place(pady=10)

        # Dynamically configure a label
#        self.label2.configure(text="Updated Label Text", fg="red")
        

"""