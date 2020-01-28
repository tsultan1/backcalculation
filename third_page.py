from tkinter import *
from background_image import BackgroundImage
from common_buttons import CommonButtons
import os
from convert_to_csv import ConvertFile


class ThirdPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        BackgroundImage('images' + os.sep + 'third_page_img.png', self)
        self.back_button = CommonButtons.create_back_button(self)
        self.next_button = CommonButtons.create_next_button(self)
        title_top = Label(self, text='Convert Text File (.txt) to Comma-Separated Values File (.csv)')
        title_top.config(font=("Courier", 20))
        title_top.pack()
        title_top.place(relx=0.5, rely=0.1, anchor=CENTER)

        convert_button = Button(self, text='Convert Text File', fg='brown', command=lambda: self.browse_button(controller))
        convert_button.config(height=2, width=13)
        convert_button.pack()
        convert_button.place(relx=0.5, rely=0.5, anchor=CENTER)

        w = Label(self, text="If you already have a .csv file, skip and hit next")
        w.pack()
        w.place(relx=0.5, rely=0.6,anchor = CENTER)

    def browse_button(self, controller):
        converter = ConvertFile(self, controller, self.back_button, self.next_button)
        converter.file_conversion()
        converter.close_window()
