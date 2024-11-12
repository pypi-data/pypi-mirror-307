from FeasFrmCls import *
import mysql.connector
import database
from mysql.connector import Error

class FeasFloor:

    def __init__(self):
        # Initialize the main window
        self.ws = Tk()
        self.ws.attributes('-fullscreen', True)
        self.ws.title("FEAS - Fire Evacuation Automation System")
        self.ws.state('zoomed')

        """ Initialize menu color settings """
        self.mbckgrd = 'brown'
        self.mforgrd = 'white'
        self.mactbkgrd = 'white'
        self.mactfrgrd = 'black'
        self.mycolumn = []

        # Initialize Boolean variables
        self.minimap = BooleanVar()
        self.minimap.set(True)

        self.darkmode = BooleanVar()
        self.darkmode.set(False)

        # Create the menu bar
        self.menubar = Menu(self.ws)
        self.menubar.config(bg=self.mbckgrd, fg=self.mforgrd, activebackground="#EA9999",
                            activeforeground=self.mactfrgrd, border=5, borderwidth=15,
                            font=('Arial', 10, 'bold'))

        # Create individual menus
        self.create_file_menu()
        self.create_floors_menu()
        self.create_messages_menu()
        self.create_views_menu()
        self.create_help_menu()

        self.floor_ddlist()
        self.left_menu_bar()
        self.am_menu_bar()
        self.pa_menu_bar()
        self.aa_menu_bar()
        self.floor_ddlist()
        self.floor_selection()

        #myframe1 = FeasFrmCls.create_frame(self, self.ws, 125, 675, "white", "brown")
        #myframe2 = FeasFrmCls.create_frame(self, self.ws, 125, 675, 'brown', '#EEEEEE')
        #myframe3 = FeasFrmCls.create_frame(self, self.ws, 900, 250, 'green', '#EEEEEE')

        #myframe1.place(x=9, y=80)
        #myframe2.place(x=9, y=80)
        #myframe3.place(x=150, y=50)
        # Configure the window to use the menu bar
        self.ws.config(menu=self.menubar)

        # Start the Tkinter event loop
        self.ws.mainloop()

    def floor_ddlist(self):

        self.ddlist_Frame = FeasFrmCls.create_frame(self,  self.ws, 250, 100, "green", "transparent")
        self.ddlist_Frame.border_color = "white"
        self.ddlist_Frame.border_width = 2
        self.ddlist_Frame.radius = 20

        self.ddlist_Frame.place(x=1200, y=10)

    def create_file_menu(self):
        """Creates the 'File' menu."""
        mfiles = Menu(self.menubar, tearoff=0, bg=self.mbckgrd, fg=self.mforgrd,
                      activebackground=self.mactbkgrd, activeforeground=self.mactfrgrd)
        mfiles.add_command(label="Exit", command=self.ws.quit)
        self.menubar.add_cascade(label="File", menu=mfiles)


    def floor_selection(self):

        self.ddFloorLst = customtkinter.CTkComboBox(self.ddlist_Frame, values=self.mycolumn,
                                                   font=('Arial', 12, 'bold'),
                                                   justify=CENTER,
                                                   state="readonly",
                                                   bg_color="transparent",
                                                   fg_color="white",
                                                   width=180,
                                                   command=self.combobox_callMA
                                                   )
        # ddFloorLst.set("Floor 01")
        self.ddFloorLst.place(x=20, y=25)
        self.ddFloorLst.bind("<<ComboboxSelected>>", self.combobox_callMA)

        #mlblMsg_Summary.config += ddFloorLst.get() + " -  Floor Sides: "

    def combobox_callMA(event,self):
        mFlrSelected = self.ddFloorLst.get()
        mFlrSelected = mFlrSelected[-2:]
        mMgr_ID = " "
        query = ("select f.cFloor_id, f.cFloor_Desc, f.cFloor_Sides, f.cFloor_Manager, f.cFloor_PA, "
                 "       E.cEmp_login,E.cEmp_FName, E.cEmp_LName,E.cEmp_ContactNo, E.cEmpContactEmail, e.cEmp_Manager, e.cEmp_Joindate "
                 " From  tCmp_Floor f, tEmp_Main E "
                 " Where f.cfloor_manager = E.cEmp_ID "
                 "       AND f.cFloor_id = " + mFlrSelected + ";")
        try:
            conn = mysql.connector.connect(host="localhost", user="root", passwd="MeOnly@007", database="feas")

            mycursor = conn.cursor()
            mycursor.execute(query)
            myresult = mycursor.fetchall()
            mCount = mycursor.rowcount
            print(f"Total Rows: {mCount}")
            mycolumn = []

            #mMgr_ID = myresult[0][3]
            #mPA_ID = myresult[0][4]
            conn.close()

        except Exception as ex:
            print(ex)

    def left_menu_bar(self):

        left_Frame = FeasFrmCls.create_frame(self,  self.ws, 125, 675, "#3D8ACC", "transparent")
        left_Frame.border_color = "white"
        left_Frame.border_width = 3
        left_Frame.radius = 50

        left_Frame.place(x=8, y=90)


    def am_menu_bar(self):
        am_Frame = FeasFrmCls.create_frame(self, self.ws, 900, 200, "brown", "transparent")
        am_Frame.border_color = "black"
        am_Frame.border_width = 2
        am_Frame.radius = 20

        am_Frame.place(x=145, y=48)

    def pa_menu_bar(self):
        pa_Frame = FeasFrmCls.create_frame(self, self.ws, 900, 200, "brown", "transparent")
        pa_Frame.border_color = "black"
        pa_Frame.border_width = 2
        pa_Frame.radius = 20

        pa_Frame.place(x=145, y=260)

    def aa_menu_bar(self):
        aa_Frame = FeasFrmCls.create_frame(self, self.ws, 900, 300, "brown", "transparent")
        aa_Frame.border_color = "black"
        aa_Frame.border_width = 2
        aa_Frame.radius = 20

        aa_Frame.place(x=145, y=480)

    def create_floors_menu(self):
        """Creates the 'Floors' menu."""
        mfloors = Menu(self.menubar, tearoff=0, bg=self.mbckgrd, fg=self.mforgrd,
                       activebackground=self.mactbkgrd, activeforeground=self.mactfrgrd)
        mfloors.add_command(label="Floors", command=self.pfloors)
        mfloors.add_command(label="Floors", command=self.pfloors)
        mfloors.add_command(label="Floors", command=self.pfloors)
        self.menubar.add_cascade(label="Floors", menu=mfloors)

    def create_messages_menu(self):
        """Creates the 'Messages' menu."""
        mmsgs = Menu(self.menubar, tearoff=0, bg=self.mbckgrd, fg=self.mforgrd,
                     activebackground=self.mactbkgrd, activeforeground=self.mactfrgrd,
                     border=0, borderwidth=15, font=('Arial', 10, 'bold'))
        mmsgs.add_command(label="Emergency")
        mmsgs.add_separator()
        mmsgs.add_command(label="General")
        mmsgs.add_separator()
        mmsgs.add_command(label="Information")
        self.menubar.add_cascade(label="Messages", menu=mmsgs)

    def create_views_menu(self):
        """Creates the 'Views' menu."""
        mviews = Menu(self.menubar, tearoff=0, bg=self.mbckgrd, fg=self.mforgrd,
                      activebackground=self.mactbkgrd, activeforeground=self.mactfrgrd,
                      border=0, borderwidth=15, font=('Arial', 10, 'bold'))
        mviews.add_checkbutton(label="Show minimap", onvalue=1, offvalue=0, variable=self.minimap)
        mviews.add_checkbutton(label='Darkmode', onvalue=1, offvalue=0, variable=self.darkmode, command=self.pdarkmode)
        self.menubar.add_cascade(label='Views', menu=mviews)

    def create_help_menu(self):
        """Creates the 'Help' menu."""
        mhelps = Menu(self.menubar, tearoff=0, bg=self.mbckgrd, fg=self.mforgrd,
                      activebackground=self.mactbkgrd, activeforeground=self.mactfrgrd)
        mhelps.add_command(label="Help")
        mhelps.add_separator()
        mhelps.add_command(label="About", command=self.pabout)
        self.menubar.add_cascade(label='Help', menu=mhelps)

    def pabout(self):
        """Placeholder for the 'About' action."""
        pass

    def pfloors(self):
        """Placeholder for the 'Floors' action."""
        pass

    def pdarkmode(self):
        """Toggles dark mode on or off based on the state of the darkmode variable."""
        if self.darkmode.get():
            self.ws.config(background="black")
        else:
            self.ws.config(background="white")


if __name__ == "__main__":
    FeasFloor()
