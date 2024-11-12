from tkinter import *
import customtkinter

class FeasFrmCls():


    def create_frame(self,
                     pwindow,
                     pwidth,
                     pheight,
                     pfgcolor,
                     pbgcolor,
                     pbrdcolor = "black",
                     pbrdwidth = 2,
                     pradius=10

                    ) -> customtkinter.CTkFrame:

        # ======================== Create Left Frame flFrame - Frame Left vertical Menu Frame =========
        mwidth = pwidth
        mheight = pheight
        mfgcolor = pfgcolor
        mbgcolor = pbgcolor
        mbrdcolor = pbrdcolor
        mbrdwidth = pbrdwidth
        mradius = pradius


        self.mfrm_name = customtkinter.CTkFrame(master=pwindow,
                                                corner_radius=mradius,
                                                fg_color=mfgcolor, #"#3D8ACC",
                                                border_color=pbrdcolor, border_width=pbrdwidth,
                                                bg_color=mbgcolor, #"#C5C1C1",  # "#EEEEEE",
                                                width=mwidth, #125,
                                                height=mheight) #, #675,
                                                #borderwidth=5, relief="ridge"
                                              #)
        return self.mfrm_name

    # create_label(window, "fcFram02", 'AA on North: ', "brown", "#C5C1C1")


    def create_button(frm, text, command=None, width=150, height=40, corner_radius=10,
                      font=("Arial", 12)) -> customtkinter.CTkButton:
        """Create and return a custom button."""
        mbutton = customtkinter.CTkButton(master=frm, text=text, command=command, width=width, height=height,
                                corner_radius=corner_radius, font=font)
        return mbutton

    def create_text_field(self, placeholder_text="", width=200, height=30, corner_radius=8, font=("Arial", 12))-> customtkinter.CTkEntry:
        """Create and return a custom text field."""
        text_field = customtkinter.CTkEntry(self, placeholder_text=placeholder_text, width=width, height=height, corner_radius=corner_radius, font=font)
        return text_field


