import matplotlib
matplotlib.use('TkAgg')
from tkinter.filedialog import askopenfilename
from tkinter import *

class Window:

    def __init__(self):
        self.root = Tk()
        self.root.withdraw()
        self.root.geometry('0x0+0+0')

    def create_file_chooser(self):
        self.bring_to_front()
        ftypes = [('CSV files', '*.csv')]
        file_path = askopenfilename(title = 'Select CSV file', filetypes = ftypes)
        return file_path

    def bring_to_front(self):
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()

    def create_coordinate_window(parent, coordinates, next):
        Label(parent, text='Enter volcanic plume coordinates').grid(row=0, columnspan=2, pady=(20, 5))
        Label(parent, text='Lower Latitude: ').grid(row=1, column=0, padx=(35, 0), pady=(15, 5))
        lower_lat = Entry(parent)
        lower_lat.grid(row=1, column=1, padx=(10, 10), pady=(15, 5))
        Label(parent, text='Upper Latitude: ').grid(row=2, column=0, padx=(33, 0), pady=(5, 5))
        upper_lat = Entry(parent)
        upper_lat.grid(row=2, column=1, padx=(10, 10), pady=(5, 5))
        Label(parent, text='Lower Longitude: ').grid(row=3, column=0, padx=(29, 0), pady=(5, 5))
        lower_long = Entry(parent)
        lower_long.grid(row=3, column=1, padx=(10, 10), pady=(5, 5))
        Label(parent, text='Upper Longitude: ').grid(row=4, column=0, padx=(29, 0), pady=(5, 5))
        upper_long = Entry(parent)
        upper_long.grid(row=4, column=1, padx=(10, 10), pady=(5, 5))
        Label(parent, text='Vertical Distribution: ').grid(row=5, column=0, padx=(10, 0), pady=(5, 0))
        vert_dist = Entry(parent)
        vert_dist.grid(row=5, column=1, padx=(10, 10), pady=(5, 0))
        Label(parent, text='(PBL = 1, TRL = 2, TRM = 3, STL = 4)').grid(row=6, column=1, padx=(45, 10))
        error_label = Label(parent, text='', fg='red')
        error_label.grid(row=9, columnspan=2, pady=(5, 5))
        Button(parent, text='Enter Coordinates', width=15, fg='blue',
               command = lambda: Window.get_input_coordinates(lower_lat, upper_lat,
                            lower_long, upper_long, vert_dist, coordinates, error_label, next)).grid(row=8,
                            column=1, padx=(0,10), pady=(20, 20))

    def get_input_coordinates(low_lat, up_lat, low_long, up_long, v_dist, coordinates, error_label, next):
        try:
            lower_lat = float(low_lat.get()) / 1.0
            upper_lat = float(up_lat.get()) / 1.0
            lower_long = float(low_long.get()) / 1.0
            upper_long = float(up_long.get()) / 1.0
            vert_dist = int(v_dist.get())
            valid = True
        except:
            valid = False

        valid = valid and lower_lat > -90 and 90 > upper_lat > lower_lat
        valid = valid and lower_long > -180 and 180 > upper_long > lower_long
        valid = valid and 1 <= vert_dist <= 4
        if valid:
            error_label.config(text='Valid coordinates! Click Next.', fg='blue')
            next.config(state=NORMAL)
            coordinates.set_coordinates(lower_lat, upper_lat, lower_long, upper_long, vert_dist)
            low_lat.config(state=DISABLED)
            up_lat.config(state=DISABLED)
            low_long.config(state=DISABLED)
            up_long.config(state=DISABLED)
            v_dist.config(state=DISABLED)
        else:
            Window.coordinate_error_handling(error_label, low_lat, up_lat, low_long, up_long, v_dist)

    def coordinate_error_handling(error_label, low_lat, up_lat, low_long, up_long, v_dist):
        error_text = 'Invalid value(s).\n Latitude values must be between -90 and 90.\n Longitude must be between -180 and 180.\n' \
                    'Lower latitude must be less than upper latitude.\n Lower longitude must be less than upper longitude.\n ' \
                     'Vertical distribution must be a value of 1 - 4'
        error_label.config(text = error_text)
        low_lat.delete(0, END)
        up_lat.delete(0, END)
        low_long.delete(0, END)
        up_long.delete(0, END)
        v_dist.delete(0, END)

    def handle_cancel_button(self, file_path, close = False):
        self.close_window()

    def close_window(self):
        self.root.destroy()
