from Backend.Bar import Bar
from Backend.CreateShuffledArray import create_shuffled_array


class Trial:
    def __init__(self, targets_number, target_is_presented, target_orientation_is_vertical):
        self.targets_number = targets_number
        self.target_is_presented = target_is_presented
        self.target_orientation_is_vertical = target_orientation_is_vertical

    def generate_bars_to_display(self):
        res = []

        # 4 grid sectors, 4 possible bar boxes each
        target_bar = lambda gs_id, bb_id: Bar(gs_id, bb_id, True, self.target_orientation_is_vertical)
        red_bar = lambda gs_id, bb_id: Bar(gs_id, bb_id, True, not self.target_orientation_is_vertical)
        green_bar = lambda gs_id, bb_id: Bar(gs_id, bb_id, False, self.target_orientation_is_vertical)

        if self.target_is_presented:
            bar_constructors = create_shuffled_array([target_bar, red_bar, green_bar, green_bar], self.targets_number)
        else:
            bar_constructors = create_shuffled_array([red_bar, red_bar, green_bar, green_bar], self.targets_number)

        bar_boxes_per_sector = self.targets_number // 4
        for grid_sector_id in range(4):
            bar_box_ids = create_shuffled_array([0, 1, 2, 3])
            for j in range(bar_boxes_per_sector):
                bar_box_id = bar_box_ids[j]
                res.append(bar_constructors[grid_sector_id * bar_boxes_per_sector + j](grid_sector_id, bar_box_id))

        return res
