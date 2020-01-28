from tkinter import *
from background_image import BackgroundImage
from common_buttons import CommonButtons
import os


class SecondPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        BackgroundImage('images' + os.sep + 'second_page_img.png', self)
        self.back_button = CommonButtons.create_back_button(self)
        self.next_button = CommonButtons.create_next_button(self)
        with open('content_files' + os.sep + 'second_page_text.txt', 'r') as f:
            Label(self, text = f.read()).pack()

        














