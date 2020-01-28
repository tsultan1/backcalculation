from tkinter import *
from background_image import BackgroundImage
from common_buttons import CommonButtons
import os
from file_processing import FileProcessing
from window_management import Window


class FourthPage(Frame):

    def __init__(self, parent, controller, data, coordinates):
        Frame.__init__(self, parent)
        self.setup_frame(controller)
        self.back_button = CommonButtons.create_back_button(self)
        self.next_button = CommonButtons.create_next_button(self)
        self.next_button.config(state=DISABLED)
        self.launch_button = self.create_launch_button()
        self.data = data
        self.coordinates = coordinates
        self.file_processor = FileProcessing(self, controller, self.back_button, self.next_button,
                                                              self.launch_button, self.data)

    def setup_frame(self, controller):
        BackgroundImage('images' + os.sep + 'fourth_page_img.png', self)
        label = Label(self, text='Load Data and Enter Coordinate Boundaries', )
        label.config(font=("Courier", 25))
        label.pack()
        label.place(relx=0.5, rely=0.1, anchor=CENTER)
        self.create_browse_button(controller)

    def create_browse_button(self, controller):
        browse_button = Button(self, text='Choose .csv file', fg='brown',
                               command=lambda: self.file_processor.get_data())
        browse_button.config(height=2, width=15)
        browse_button.pack()
        browse_button.place(relx=0.12, rely=0.4, anchor=CENTER)

    def create_launch_button(self):
        launch_button = Button(self, text='Choose region boundaries', fg='brown', command=self.display_coordinate_window)
        launch_button.config(height=2, width=20)
        launch_button.pack()
        launch_button.place(relx=0.12, rely=0.5, anchor=CENTER)
        launch_button.config(state=DISABLED)
        return launch_button

    def display_coordinate_window(self):
        self.data = self.file_processor.data
        self.next_button.config(state=DISABLED)
        coordinate_frame = Frame(master=self, width=400, height=450)
        coordinate_frame.pack()
        coordinate_frame.place(relx=0.6, rely=0.55, anchor=CENTER)
        Window.create_coordinate_window(coordinate_frame, self.coordinates, self.next_button)
