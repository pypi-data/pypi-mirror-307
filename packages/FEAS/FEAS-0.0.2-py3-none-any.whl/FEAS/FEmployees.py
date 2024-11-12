import tkinter
import customtkinter
from FeasFrmCls import FeasFrmCls
#customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
#customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green



class FEmployees:
    def __init__(self, window):
        self.window = window
        #self.window = customtkinter.CTk()
        width = self.window.winfo_screenwidth()
        height = self.window.winfo_screenheight()

        self.window.title("FEAS - Messages Broadcast Control Portal" + "  w-" + str(width) + "   h-" + str(height))
        self.window.iconbitmap("fire-alarm.ico")
        #self.window._max_width = width
        #self.window._max_height = height

        #mydb = database.Database("localhost:3306", "root", "MeOnly@007", "feas")
        #mydb.create_connection()

        #self.window.attributes('-fullscreen', True)
        #self.window.state('zoomed')

        self.window = customtkinter.CTk()
        self.window.title("Employee Listing")
        self.window.state("zoomed")
        self.window._fg_color = "white"
        self.window._bg_color = "#C5C1C1"
        #self.window.geometry("900x1200")

        myframe1 = FeasFrmCls.create_frame(self, self.window, 125, 675, "white", "#C5C1C1")
        myframe2 = FeasFrmCls.create_frame(self, self.window, 125, 675, '#3D8ACC', '#C5C1C1')
        myframe3 = FeasFrmCls.create_frame(self, self.window, 900, 250, 'green', '#C5C1C1')

        myframe1.place(x=9, y=80)
        myframe2.place(x=11, y=82)
        myframe3.place(x=150, y=50)

        # Start the Tkinter event loop
#        self.window.mainloop()


    def run(self):
            self.window.mainloop()


if __name__ == "__main__":
    window = customtkinter.CTk()
    app = FEmployees(window)
    app.run()
