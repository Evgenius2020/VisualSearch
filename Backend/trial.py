from dataclasses import dataclass
from random import random
from typing import List, Tuple

from Backend.utils import create_shuffled_array


@dataclass
class Bar:
    grid_sector_id: int
    bar_box_id: int
    color_is_red: bool
    orientation_is_vertical: bool
    shift: Tuple[float, float]


class Trial:
    targets_number: int
    target_is_presented: bool
    target_orientation_is_vertical: bool
    bars_to_display: List[Bar]

    def __init__(self,
                 targets_number: int,
                 target_is_presented: bool,
                 target_orientation_is_vertical: bool):
        if targets_number / 4 != targets_number // 4:
            raise ValueError("'targets_number' should be divisible by 4")
        self.targets_number = targets_number
        self.target_is_presented = target_is_presented
        self.target_orientation_is_vertical = target_orientation_is_vertical
        self.bars_to_display = self.__generate_bars_to_display__()

    def __generate_bars_to_display__(self) -> List[Bar]:
        bars = []

        tov = self.target_orientation_is_vertical
        target_bar = lambda gs_id, bb_id, sh: Bar(gs_id, bb_id, True, tov, sh)
        red_bar = lambda gs_id, bb_id, sh: Bar(gs_id, bb_id, True, not tov, sh)
        green_bar = lambda gs_id, bb_id, sh: Bar(gs_id, bb_id, False, tov, sh)

        if self.target_is_presented:
            bar_constructors = create_shuffled_array([target_bar, red_bar, green_bar],
                                                     items_repeats=[1,
                                                                    self.targets_number // 2 - 1,
                                                                    self.targets_number // 2])
        else:
            bar_constructors = create_shuffled_array([red_bar, green_bar],
                                                     items_repeats=[self.targets_number // 2,
                                                                    self.targets_number // 2])

        # 4 grid sectors, 4 possible bar boxes each
        bar_boxes_per_sector = self.targets_number // 4
        for grid_sector_id in range(4):
            bar_box_ids = create_shuffled_array([0, 1, 2, 3])
            for j in range(bar_boxes_per_sector):
                bar_box_id = bar_box_ids[j]
                shift = (random(), random())
                bars.append(
                    bar_constructors[grid_sector_id * bar_boxes_per_sector + j](
                        grid_sector_id,
                        bar_box_id,
                        shift))

        return bars
