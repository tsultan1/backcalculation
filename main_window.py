from tkinter import *
from first_page import FirstPage
from second_page import SecondPage
from third_page import ThirdPage
from fourth_page import FourthPage
from fifth_page import FifthPage
from final_page import FinalPage
from data_management import Data
from coordinates import Coordinates
from heatmap import Heatmap
import pandas as pd
import gc

class MainWindow(Tk):

    def __init__(self):
        Tk.__init__(self)
        container = self.create_main_container()
        self.set_window_properties()
        self.data = Data(pd.DataFrame())
        self.coordinates = Coordinates()
        self.heatmap = Heatmap()
        self.initialize_pages(container)
        self.show_frame(FirstPage)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        self.quit()

    def initialize_pages(self, container):
        self.frames = {}
        for F in (FirstPage, SecondPage, ThirdPage, FourthPage, FifthPage, FinalPage):
            if F in [FirstPage, SecondPage, ThirdPage]:
                frame = F(container, self)
            elif F == FourthPage:
                frame = F(container, self, self.data, self.coordinates)
            else:
                frame = F(container, self, self.data, self.coordinates, self.heatmap)
            self.configure_button_commands(frame)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def configure_button_commands(self, frame):
        if isinstance(frame, FirstPage):
            frame.start_button.configure(command=lambda: self.show_frame(SecondPage))
        elif isinstance(frame, SecondPage):
            frame.back_button.configure(command=lambda: self.show_frame(FirstPage))
            frame.next_button.configure(command=lambda: self.show_frame(ThirdPage))
        elif isinstance(frame, ThirdPage):
            frame.back_button.configure(command=lambda: self.show_frame(SecondPage))
            frame.next_button.configure(command=lambda: self.show_frame(FourthPage))
        elif isinstance(frame, FourthPage):
            frame.back_button.configure(command=lambda: self.show_frame(ThirdPage))
            frame.next_button.configure(command=lambda: self.show_frame(FifthPage))
        elif isinstance(frame, FifthPage):
            frame.back_button.configure(command=lambda: self.show_frame(FourthPage))
            frame.next_button.configure(command=lambda: self.call_final_page_so2_functions(FinalPage))
        elif isinstance(frame, FinalPage):
            frame.back_button.configure(command=lambda: self.handle_fifth_page_back_button(FifthPage))

    def create_main_container(self):
        container = Frame(self)
        container.pack(side=TOP, fill=BOTH, expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        return container

    def set_window_properties(self):
        self.lift()
        self.title('')
        self.attributes('-topmost', True)
        self.wm_geometry("1025x563+150+100")

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def call_final_page_so2_functions(self, cont):
        self.frames[cont].display_so2_plot()
        self.show_frame(cont)

    def handle_fifth_page_back_button(self, back_frame):
        frame = self.frames[back_frame]
        for child in frame.winfo_children():
            if isinstance(child, Frame):
                child.destroy()
            elif isinstance(child, Label) and ('Value' in child['text']):
                child.destroy()
        frame.next_button.config(state=DISABLED)
        self.show_frame(back_frame)
