from tkinter import *
from background_image import BackgroundImage
from common_buttons import CommonButtons
import os
from data_color_map import DataColorMap
from canvas_events import CanvasEvents
import threading


class FifthPage(Frame):

    def __init__(self, parent, controller, data, coordinates, heatmap):
        Frame.__init__(self, parent)
        self.data = data
        self.coordinates = coordinates
        self.heatmap = heatmap
        self.setup_page()
        self.back_button = CommonButtons.create_back_button(self)
        self.next_button = CommonButtons.create_next_button(self)
        self.next_button.config(state=DISABLED)

    def setup_page(self):
        BackgroundImage('images' + os.sep + 'fifth_page_img.png', self)
        label = Label(self, text='Heat Map', )
        label.config(font=("Courier", 25))
        label.pack()
        label.place(relx=0.12, rely=0.1, anchor=CENTER)
        heatmap_button = Button(self, text='Display Heatmap', command=self.generate_heatmap)
        heatmap_button.config(height=2, width=15)
        heatmap_button.pack()
        heatmap_button.place(relx=0.12, rely=0.4, anchor=CENTER)

    def generate_heatmap(self):
        if not self.data.data_matrix.all():
            self.data.setup_data_matrix(self.coordinates)
            self.data.fill_so2_log_values()
            self.data.display_data_matrix_values(self, self.coordinates)

        color_map = DataColorMap(self.coordinates)
        color_map.fill_color_map(self.coordinates, self.data.data_matrix)
        color_map.setup_color_count()

        self.heatmap.initialize_heatmap_properties(color_map.get_log_colors(), self.coordinates, self.next_button)
        self.heatmap.create_heatmap()

        heatmap_canvas = CanvasEvents(self)
        thread = threading.Thread(target=lambda: heatmap_canvas.display_heat_map(self.heatmap))
        thread.start()