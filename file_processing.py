import pandas as pd
from tkinter import *
import time, threading
from window_management import Window
from data_management import Data
from queue import Queue


class FileProcessing():

    def __init__(self, parent, controller, back, next, launch, data):
        self.controller = controller
        self.parent = parent
        self.back_button = back
        self.next_button = next
        self.launch_button = launch
        self.data = data

    def get_data(self):
        win = Window()
        win.root.attributes('-topmost', True)
        self.controller.attributes('-topmost', False)
        file_path = win.create_file_chooser()
        if file_path:
            processing_label = self.setup_processing_label(self.parent)
            self.disable_buttons()
            self.handle_thread_processing(file_path, self.controller)
            processing_label.configure(text='File loaded')
            self.enable_buttons()
            win.root.destroy()
        else:
            self.back_button.config(state=NORMAL)

    def fill_data_frame(self, file_path, queue):
        data = pd.read_csv(file_path, low_memory=False)
        queue.put(data.values)

    def handle_thread_processing(self, filename, controller):
        queue = Queue()
        thread = threading.Thread(target=lambda: self.fill_data_frame(filename, queue))
        thread.start()
        while thread.is_alive():
            controller.update()
            time.sleep(0.001)
        self.data.data_matrix = queue.get()

    def setup_processing_label(self, parent):
        processing_label = Label(parent, text='Loading data from .csv file', fg='black', bg='#BDC3C7')
        processing_label.config(height=2, width=20)
        processing_label.pack()
        processing_label.place(relx=0.12, rely=0.4, anchor=CENTER)
        return processing_label

    def disable_buttons(self):
        self.next_button.config(state=DISABLED)
        self.back_button.config(state=DISABLED)

    def enable_buttons(self):
        self.back_button.config(state=NORMAL)
        self.launch_button.config(state=NORMAL)