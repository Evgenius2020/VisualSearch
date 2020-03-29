from Backend.Bar import Bar
from Backend.CreateShuffledArray import create_shuffled_array


class Trial:
    def __init__(self, targets_number, target_is_presented, target_orientation_is_vertical):
        if targets_number / 4 != targets_number // 4:
            raise ValueError("'targets_number' should be divisible by 4")
        self.targets_number = targets_number
        self.target_is_presented = target_is_presented
        self.target_orientation_is_vertical = target_orientation_is_vertical
        self.bars_to_display = self.__generate_bars_to_display__()

    def __generate_bars_to_display__(self):
        bars = []

        target_bar = lambda gs_id, bb_id: Bar(gs_id, bb_id, True, self.target_orientation_is_vertical)
        red_bar = lambda gs_id, bb_id: Bar(gs_id, bb_id, True, not self.target_orientation_is_vertical)
        green_bar = lambda gs_id, bb_id: Bar(gs_id, bb_id, False, self.target_orientation_is_vertical)

        if self.target_is_presented:
            bar_constructors = create_shuffled_array([target_bar, red_bar, green_bar],
                                                     items_repeats=[1, self.targets_number // 2 - 1,
                                                                    self.targets_number // 2])
        else:
            bar_constructors = create_shuffled_array([red_bar, green_bar],
                                                     items_repeats=[self.targets_number // 2, self.targets_number // 2])

        # 4 grid sectors, 4 possible bar boxes each
        bar_boxes_per_sector = self.targets_number // 4
        for grid_sector_id in range(4):
            bar_box_ids = create_shuffled_array([0, 1, 2, 3])
            for j in range(bar_boxes_per_sector):
                bar_box_id = bar_box_ids[j]
                bars.append(bar_constructors[grid_sector_id * bar_boxes_per_sector + j](grid_sector_id, bar_box_id))

        return bars
