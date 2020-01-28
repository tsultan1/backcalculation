from tkinter import *
from background_image import BackgroundImage
import os
from common_buttons import CommonButtons
from data_color_map import DataColorMap
from so2_calculations import SO2Calculations
from canvas_events import CanvasEvents


class FinalPage(Frame):

    def __init__(self, parent, controller, data, coordinates, heatmap):
        Frame.__init__(self, parent)
        self.setup_properties()
        self.back_button = CommonButtons.create_back_button(self)
        self.data = data
        self.coordinates = coordinates
        self.heatmap = heatmap

    def setup_properties(self):
        BackgroundImage('images' + os.sep + 'final_page_img.png', self)
        label = Label(self, text='SO2 Calculations', )
        label.config(font=("Courier", 25))
        label.pack()
        label.place(relx=0.2, rely=0.05, anchor=CENTER)

    def display_so2_plot(self):
        heatmap_canvas = CanvasEvents(self)

        color_map = DataColorMap(self.coordinates)
        color_map.fill_color_map(self.coordinates, self.data.data_matrix)
        color_map.setup_color_count()

        so2_data = SO2Calculations(self.heatmap, color_map.get_original_so2_colors())
        heatmap_canvas.plot_so2_columns(so2_data)
