import math
from tkinter import *


class Data:

    latitude_col = 0
    longitude_col = 1
    so2_col = 2
    so2_log_col = so2_col + 1

    def __init__(self, data):
        self.data_matrix = data.values

    def setup_data_matrix(self, coords):
        self.data_matrix = self.data_matrix[coords.lower_latitude <= self.data_matrix[:, Data.latitude_col]]
        self.data_matrix = self.data_matrix[self.data_matrix[:, Data.latitude_col] <= coords.upper_latitude]
        self.data_matrix = self.data_matrix[self.data_matrix[:, Data.longitude_col] >= coords.lower_longitude]
        self.data_matrix = self.data_matrix[self.data_matrix[:, Data.longitude_col] <= coords.upper_longitude]
        self.data_matrix = self.data_matrix[:, [Data.latitude_col, Data.longitude_col, coords.vertical_distribution, coords.vertical_distribution]]

    def fill_so2_log_values(self):
        for i in range(len(self.data_matrix[:, Data.so2_col])):
            if self.data_matrix[i, Data.so2_col] < 0:
                self.data_matrix[i, Data.so2_col] = 0
                self.data_matrix[i, Data.so2_log_col] = 0
            else:
                self.data_matrix[i, Data.so2_log_col] = math.log1p(self.data_matrix[i, Data.so2_col])

    def display_data_matrix_values(self, frame, coords):
        min_logso2_label = Label(frame, text='Minimum ln(SO2) Value: ' + '{0:.2f}'.format(min(self.data_matrix[:, Data.so2_log_col])),
                                 fg='black', bg='#AFEEEE')
        min_logso2_label.pack()
        min_logso2_label.place(relx=0.12, rely=0.5, anchor=CENTER)
        max_logso2_label = Label(frame, text='Maximum ln(SO2) Value: ' + '{0:.2f}'.format(max(self.data_matrix[:, Data.so2_log_col])),
                              fg='black', bg='#AFEEEE')
        max_logso2_label.pack()
        max_logso2_label.place(relx=0.12, rely=0.55, anchor=CENTER)
        min_so2_label = Label(frame, text='Minimum SO2 Value: ' + '{0:.2f}'.format(min(self.data_matrix[:, Data.so2_col])),
                              fg='black', bg='#AFEEEE')
        min_so2_label.pack()
        min_so2_label.place(relx=0.12, rely=0.6, anchor=CENTER)
        max_so2_label = Label(frame, text='Maximum SO2 Value: ' + '{0:.2f}'.format(max(self.data_matrix[:, Data.so2_col])),
                              fg='black', bg='#AFEEEE')
        max_so2_label.pack()
        max_so2_label.place(relx=0.12, rely=0.65, anchor=CENTER)
