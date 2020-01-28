class Coordinates:

    levels = {2: 'PBL', 3: 'TRL', 4: 'TRM', 5: 'STL'}

    def __init__(self):
        self.lower_latitude = 0
        self.upper_latitude = 0
        self.lower_longitude = 0
        self.upper_longitude = 0
        self.vertical_distribution = 0

    def set_coordinates(self, low_lat, up_lat, low_long, up_long, v_dist):
        self.lower_latitude = low_lat
        self.upper_latitude = up_lat
        self.lower_longitude = low_long
        self.upper_longitude = up_long
        self.vertical_distribution = v_dist + 1