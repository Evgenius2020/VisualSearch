from random import random


class Bar:
    def __init__(self, grid_sector_id, bar_box_id, color_is_red, orientation_is_vertical):
        self.grid_sector_id = grid_sector_id
        self.bar_box_id = bar_box_id
        self.color_is_red = color_is_red
        self.orientation_is_vertical = orientation_is_vertical
        self.shift = (random(), random())
