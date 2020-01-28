import pandas as pd
from tkinter.filedialog import asksaveasfilename, askopenfilename
from tkinter import *
import time, threading
import os
from window_management import Window


class ConvertFile():

    def __init__(self, parent, controller, back, next):
        self.win = Window()
        self.controller = controller
        self.parent = parent
        self.setup_window_properties()
        self.data = pd.DataFrame()
        self.back_button = back
        self.next_button = next

    def setup_window_properties(self):
        self.win.root.attributes('-topmost', True)
        self.controller.attributes('-topmost', False)

    def file_conversion(self):
        filename = askopenfilename()
        if filename:
            processing_label = self.setup_processing_label()
            self.disable_buttons()
            self.handle_thread_processing(filename)
            self.save_csv_file(filename)
            processing_label.configure(text='.csv file created!')
            self.enable_buttons()

    def save_csv_file(self, filename):
        initial_file = os.path.basename(filename).rstrip('.txt') + '.csv'
        output_file = asksaveasfilename(initialdir="/", initialfile=initial_file,
                                        filetypes=[('CSV', '.csv'), ('Save as', '*')])
        if output_file:
            self.data.to_csv(output_file, header=True, index=False)

    def handle_thread_processing(self, filename):
        thread = threading.Thread(target=lambda: self.fill_data_frame(filename))
        thread.start()
        while thread.is_alive():
            self.controller.update()
            time.sleep(0.001)

    def disable_buttons(self):
        self.next_button.config(state=DISABLED)
        self.back_button.config(state=DISABLED)

    def enable_buttons(self):
        self.next_button.config(state=NORMAL)
        self.back_button.config(state=NORMAL)

    def setup_processing_label(self):
        processing_label = Label(self.parent, text='Please wait. Converting to .csv file', fg='black')
        processing_label.config(height=2, width=25)
        processing_label.pack()
        processing_label.place(relx=0.5, rely=0.4, anchor=CENTER)
        return processing_label

    def fill_data_frame(self, filename):
        self.data = pd.read_table(filename, dtype=float, delimiter='\t', skiprows=52, header=0,
                                  usecols=[1, 3, 35, 36, 37, 38])

    def close_window(self):
        self.win.root.destroy()