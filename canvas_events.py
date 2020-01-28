import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *
from persistent_rectangle_selector import PersistentRectangleSelector
import numpy as np

class CanvasEvents():

    def __init__(self, parent):
        self.frame = parent

    def display_heat_map(self, heat_map):
        heatmap_frame = Frame(self.frame)
        heatmap_frame.pack()
        heatmap_frame.place(relx=0.55, rely=0.5, anchor=CENTER)
        canvas = FigureCanvasTkAgg(heat_map.fig, master=heatmap_frame)
        self.span = PersistentRectangleSelector(heat_map.ax, heat_map.onselect, drawtype='box', useblit=False,
                                           rectprops=dict(facecolor='white', edgecolor='white', linewidth=1,
                                            alpha=1, fill=False))
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0)
        canvas.get_tk_widget().focus_set()
        instruct = Label(heatmap_frame, text='Select 24 hours region and click Next')
        instruct.grid(row=0, column=0, pady=(10, 0))

    def plot_so2_columns(self, so2_data):
        so2_data.calculate_so2_columns()

        plot_frame = Frame(self.frame)
        plot_frame.pack()
        plot_frame.place(relx=0.3, rely=0.5, anchor=CENTER)

        x_axis = list(np.arange(1, 25, 1))
        print(x_axis, so2_data.so2_columns)
        plot_figure = Figure(figsize=(5,4), dpi=100)
        ax = plot_figure.add_subplot(111)
        ax.plot(x_axis, list(so2_data.so2_columns[::-1]), '.')
        ax.set_title('SO2 column amounts per 24 hours')
        ax.set_xlabel('Time (hours)')
        ax.set_ylabel('SO2 (Dobson Units)')
        canvas = FigureCanvasTkAgg(plot_figure, master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()
        canvas.get_tk_widget().focus_set()
