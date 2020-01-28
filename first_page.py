from tkinter import *
from background_image import BackgroundImage
import os

class FirstPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        BackgroundImage('images' + os.sep + 'first_page_img.png', self)
        self.create_start_button()

    def create_start_button(self):
        self.start_button = Button(self, text='Start', fg='brown')
        self.start_button.config(height=2, width=10)
        self.start_button.pack()
        self.start_button.place(x=750, y=300)
        self.start_button.place(relx=0.1, rely=0, anchor=CENTER)