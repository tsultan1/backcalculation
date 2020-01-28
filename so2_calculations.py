import numpy as np


class SO2Calculations:

    def __init__(self, heatmap, original_so2_data):
        self.so2_columns = []
        self.data = np.array(original_so2_data)
        self.bounds = heatmap.bounds
        self.region = heatmap.region_24_hours

    def calculate_so2_columns(self):
        self.so2_columns = []
        if self.region.boundaries:
            heatmap_longitudes, heatmap_latitudes = self.get_lat_long_values()
            region_longitude_indices = self.region.get_longitude_region_indices(heatmap_longitudes)
            max_lat_index, min_lat_index = self.region.get_max_min_lat_values(heatmap_latitudes)

            interval_size = (heatmap_longitudes[region_longitude_indices[1]] - heatmap_longitudes[region_longitude_indices[0]])
            interval_24_size = (self.region.upper_long - self.region.lower_long)/25

            long_24_hours = np.arange(self.region.lower_long, self.region.upper_long, interval_24_size)
            if long_24_hours.shape[0] == 26:
                long_24_hours = long_24_hours[:-1]
            elif long_24_hours.shape[0] == 24:
                long_24_hours = np.append(long_24_hours, long_24_hours[-1] + interval_24_size)

            self.calculate_so2_column_sums(interval_24_size, long_24_hours, max_lat_index, min_lat_index, heatmap_longitudes)

    def calculate_so2_column_sums(self, interval_size, long_24_hours, max_lat_index, min_lat_index, x_long_values):
        for i in range(1, long_24_hours.shape[0]):
            left = x_long_values[np.where(x_long_values <= long_24_hours[i - 1])][-1]
            right = x_long_values[np.where(x_long_values <= long_24_hours[i])][-1]
            #print(left, right)
            sum_so2 = 0
            if left == right:
                #sum_so2 = self.get_so2_for_interval(long_24_hours[i], long_24_hours[i - 1], left, interval_size,
                #                                    x_long_values, min_lat_index, max_lat_index)
                index = np.where(x_long_values == left)[0][0]
                columns = self.data[index, min_lat_index:max_lat_index]
                nonzero_columns = columns[np.where(columns >= 0)]
                sum_so2 = sum(nonzero_columns)
            elif not left == right and right - left <= interval_size:
                sum_so2_left = self.get_so2_for_interval(right, long_24_hours[i - 1], left, interval_size,
                                                         x_long_values, min_lat_index, max_lat_index)

                sum_so2_right = self.get_so2_for_interval(long_24_hours[i], right, right, interval_size,
                                                          x_long_values, min_lat_index, max_lat_index)
                sum_so2 = sum_so2_left + sum_so2_right
            else:
                sum_so2 += self.get_so2_for_interval(long_24_hours[i], right, right, interval_size,
                                                     x_long_values, min_lat_index, max_lat_index)
                while right - interval_size > long_24_hours[i - 1]:
                    sum_so2 += self.get_so2_for_interval(interval_size, 0, (right - interval_size), interval_size,
                                                         x_long_values, min_lat_index, max_lat_index)
                    right -= interval_size
                sum_so2 += self.get_so2_for_interval(right, long_24_hours[i - 1], right, interval_size,
                                                     x_long_values, min_lat_index, max_lat_index)
            self.so2_columns.append(sum_so2)

    def get_so2_for_interval(self, right_side, left_side, side, interval_size, x_long_values, min_lat_index, max_lat_index):
        factor = (right_side - left_side)/interval_size
        index = np.where(x_long_values == side)[0][0]
        columns = self.data[index, min_lat_index:max_lat_index]
        nonzero_columns = columns[np.where(columns > 0)]
        return factor * sum(nonzero_columns)

    def get_lat_long_values(self):
        long_values = np.arange(self.bounds.lower_longitude, self.bounds.upper_longitude,
                               (self.bounds.upper_longitude - self.bounds.lower_longitude) / (len(self.data) - 1))
        lat_values = np.arange(self.bounds.lower_latitude, self.bounds.upper_latitude,
                              (self.bounds.upper_latitude - self.bounds.lower_latitude) / (len(self.data[0]) - 1))
        return long_values, lat_values




