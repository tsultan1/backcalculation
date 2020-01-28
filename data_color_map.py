import math
import numpy as np
from data_management import Data

'''
data array is 3D array containing two dimensions of rows and columns.
Each block, starting from from row 0, col 0 (pertaining to bottom left of grid),
has 7 pieces of additional data.
0: x0 - bottom left longitude coord of single block
1: y0 - bottom left latitude coord of single block
2: x1 - top right longitude of single block
3: y1 - top right latitude of single block
4: ln_color - intitalized to zero. To be determined by natural log of SO2 amount
5: SO2 Amount - SO2 value from worksheet  
6: Empty/Filled - Intialized to zero. Changed to one if single block is filled with SO2 derived color
'''


class DataColorMap:

    width = 24.0 / 87.0  # resolution of 1 degree longitude = 87km
    height = 13.0 / 111.0  # resolution of 1 degree latitude  = 111 km

    def __init__(self, coords):
        self.rows = int(math.ceil((coords.upper_latitude - coords.lower_latitude) / DataColorMap.height)) + 1
        self.cols = int(math.ceil((coords.upper_longitude - coords.lower_longitude) / DataColorMap.width)) + 1
        self.color_map_data = np.zeros((self.rows, self.cols, 7))

    def fill_color_map(self, coords, data_matrix):
        y0 = coords.lower_latitude
        for row in range(len(self.color_map_data)):
            x0 = coords.lower_longitude
            y1 = y0 + DataColorMap.height
            for col in range(len(self.color_map_data[0])):
                x1 = x0 + DataColorMap.width
                self.color_map_data[row, col] = [x0, y0, x1, y1, 0, 0, int(0)]
                data_subset = self.subset_data_matrix_by_grid_block(data_matrix, x0, x1, y0, y1)
                data_len = len(data_subset)
                self.set_color_map_values(col, data_len, data_subset, row)
                x0 = x1
            y0 = y1

    def set_color_map_values(self, col, data_len, data_subset, row):
        if data_len == 1:
            self.color_map_data[row, col, 4] = data_subset[0, Data.so2_log_col]
            self.color_map_data[row, col, 5] = data_subset[0, Data.so2_col]
            self.color_map_data[row, col, 6] = 1
        elif data_len > 1:
            avg_log_so2, avg_so2 = self.calculate_average_so2_values(data_len, data_subset)
            self.color_map_data[row, col, 4] = avg_log_so2
            self.color_map_data[row, col, 5] = avg_so2
            self.color_map_data[row, col, 6] = 1

    def calculate_average_so2_values(self, data_len, data_subset):
        avg_log_so2 = 0
        avg_so2 = 0
        for i in range(data_len):
            avg_log_so2 += data_subset[i, Data.so2_log_col]
            avg_so2 += data_subset[i, Data.so2_col]
        avg_log_so2 /= data_len
        avg_so2 /= data_len
        return avg_log_so2, avg_so2

    def subset_data_matrix_by_grid_block(self, data_matrix, x0, x1, y0, y1):
        data_subset = data_matrix[data_matrix[:, 1] > x0]
        data_subset = data_subset[data_subset[:, 1] < x1]
        data_subset = data_subset[data_subset[:, 0] > y0]
        data_subset = data_subset[data_subset[:, 0] < y1]
        return data_subset

    def get_log_colors(self, col=5):
        colors = np.zeros((self.rows, self.cols))
        for y in range(len(self.color_map_data)):
            for x in range(len(self.color_map_data[0])):
                colors[y, x] = self.color_map_data[y, x, col]
        return colors

    def get_original_so2_colors(self):
        return self.get_log_colors(5)

    def setup_color_count(self):
        color_count_log = []
        color_count_so2 = []
        max_row_index = len(self.color_map_data)
        max_col_index = len(self.color_map_data[0])
        for row in range(max_row_index):
            for col in range(max_col_index):
                self.average_missing_values(col, color_count_log, color_count_so2, max_col_index, max_row_index, row)

    def average_missing_values(self, col, color_count_log, color_count_so2, max_col_index, max_row_index, row):
        if self.color_map_data[row, col, 6] == 0:
            self.get_row_above(col, color_count_log, color_count_so2, max_col_index, max_row_index, row)
            self.get_row_below(col, color_count_log, color_count_so2, max_col_index, row)
            self.get_column_right(col, color_count_log, color_count_so2, max_col_index, row)
            self.get_column_left(col, color_count_log, color_count_so2, row)

            self.color_map_data[row, col, 4] = np.average(color_count_log)
            self.color_map_data[row, col, 5] = np.average(color_count_so2)
            del color_count_log[0:]
            del color_count_so2[0:]

    def get_row_below(self, col, color_count_log, color_count_so2, max_col_index, row):
        if row - 1 >= 0:
            color_count_log.append(int(self.color_map_data[row - 1, col, 4]))
            color_count_so2.append(int(self.color_map_data[row - 1, col, 5]))
            self.get_column_right(col, color_count_log, color_count_so2, max_col_index, row - 1)
            self.get_column_left(col, color_count_log, color_count_so2, row - 1)

    def get_row_above(self, col, color_count_log, color_count_so2, max_col_index, max_row_index, row):
        if row + 1 < max_row_index:
            color_count_log.append(int(self.color_map_data[row + 1, col, 4]))
            color_count_so2.append(int(self.color_map_data[row + 1, col, 5]))
            self.get_column_right(col, color_count_log, color_count_so2, max_col_index, row + 1)
            self.get_column_left(col, color_count_log, color_count_so2, row + 1)

    def get_column_left(self, col, color_count_log, color_count_so2, row):
        if col - 1 >= 0:
            color_count_log.append(int(self.color_map_data[row, col - 1, 4]))
            color_count_so2.append(int(self.color_map_data[row, col - 1, 5]))

    def get_column_right(self, col, color_count_log, color_count_so2, max_col_index, row):
        if col + 1 < max_col_index:
            color_count_log.append(int(self.color_map_data[row, col + 1, 4]))
            color_count_so2.append(int(self.color_map_data[row, col + 1, 5]))