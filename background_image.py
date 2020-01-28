from tkinter import *

class BackgroundImage(Frame):

    def __init__(self, file_name, parent):
        Frame.__init__(self, parent)
        graphic = PhotoImage(file=file_name)
        self.set_background_properties(graphic, parent)

    def set_background_properties(self, graphic, parent):
        background_image = Label(parent, image=graphic)
        background_image.image = graphic
        background_image.pack(fill=BOTH, expand=YES)
        background_image.place(relx=.5, rely=.5, anchor=CENTER)