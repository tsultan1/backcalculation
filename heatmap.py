import matplotlib.pyplot as pyplot
from region_data import Region
from tkinter import *

class Heatmap:

    def __init__(self, data = None, bounds = None, button = None):
        self.fig, self.ax = pyplot.subplots(figsize=(6, 5), dpi=100)
        self.heatmap_data = data
        self.bounds = bounds
        self.region_24_hours = Region()
        self.next_button = button

    def initialize_heatmap_properties(self, data, bounds, button):
        self.heatmap_data = data
        self.bounds = bounds
        self.next_button = button

    def set_button(self, button):
        self.next_button = button

    def create_heatmap(self):
        im = self.ax.imshow(self.heatmap_data, cmap='jet', origin=[0, 0], aspect='auto',
                            vmin=0, vmax=max(self.heatmap_data.flatten()),
                            extent=[self.bounds.lower_longitude, self.bounds.upper_longitude,
                                    self.bounds.lower_latitude, self.bounds.upper_latitude])

        pyplot.xticks(rotation=70)
        color_bar = pyplot.colorbar(im)
        color_bar.set_label('SO2 (Dobson Units)', rotation=270, labelpad=10)
        title = 'Collection Amount of SO2 at level: ' + self.bounds.levels[self.bounds.vertical_distribution]
        pyplot.title(title)
        pyplot.xlabel('Longitude')
        pyplot.ylabel('Latitude')
        pyplot.margins(0.1)
        pyplot.subplots_adjust(bottom=0.2)

    def onselect(self, eclick, erelease):
        self.region_24_hours.set_region_boundaries([(eclick.xdata, eclick.ydata), (erelease.xdata, erelease.ydata)])
        self.next_button.config(state=NORMAL)
