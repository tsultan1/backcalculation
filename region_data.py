import numpy as np


class Region():

    def __init__(self):
        self.boundaries = []

    def set_region_boundaries(self, boundaries):
        self.boundaries = boundaries
        self.get_region_boundaries()

    def get_region_boundaries(self):
        self.lower_lat = min(self.boundaries[0][1], self.boundaries[1][1])
        self.upper_lat = max(self.boundaries[0][1], self.boundaries[1][1])
        self.lower_long = min(self.boundaries[0][0], self.boundaries[1][0])
        self.upper_long = max(self.boundaries[0][0], self.boundaries[1][0])

    def get_longitude_region_indices(self, heatmap_longitude):
        indices = np.where(np.logical_and(heatmap_longitude >= self.lower_long, heatmap_longitude <= self.upper_long))[0]
        if heatmap_longitude[indices[0]] > self.lower_long:
            indices = np.insert(indices, 0, indices[0] - 1)
        if heatmap_longitude[indices[-1]] < self.upper_long:
            indices = np.append(indices, indices[-1] + 1)

        return indices

    def get_max_min_lat_values(self, heatmap_latitudes):
        index_range = (np.where(np.logical_and(heatmap_latitudes >= self.lower_lat, heatmap_latitudes <= self.upper_lat)))[0]
        min_index = np.min(index_range)
        max_index = np.max(index_range)
        return max_index, min_index
