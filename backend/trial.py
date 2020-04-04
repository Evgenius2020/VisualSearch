from dataclasses import dataclass
from random import random
from typing import List, Tuple

from backend.utils import create_shuffled_list


@dataclass
class Bar:
    """
    Rendering parameters of trial bar.
    Bars are located in specified sectors of the screen grid, in specified bar boxes of these sectors.
    Grid sectors and bar boxing mappings are described below.

    # Mappings:
    # Grid sectors:         Bar boxes:
    #   0 0 1 1               0 1 0 1
    #   0 0 1 1               2 3 2 3
    #   2 2 3 3               0 1 0 1
    #   2 2 3 3               2 3 2 3

    :param grid_sector_id: Number of screen grid sector (0-3).
    :param bar_box_id: Number of screen grid sector bar box (0-3).
    :param color_is_red: Bar will be red if 'True', or green if 'False'.
    :param orientation_is_vertical: Bar will be vertical if 'True', or horizontal if 'False'.
    :param shift: Random shift tuple (x; y); values belongs [0.0, 1.0) range.
    """
    grid_sector_id: int
    bar_box_id: int
    color_is_red: bool
    orientation_is_vertical: bool
    shift: Tuple[float, float]


class Trial:
    """
    Values that defines experiment trial.
    Each trial contains 4, 8, 12 or 16 (divisible by 4) bars on screen.
    Bars are red or green (1:1 ratio).
    Target red bar can be presented on screen, or not.
    Bars orientations depends on target bar orientation.
    Red (non-target) bars have a different orientation than the target bar.
    Green bars have the same orientation as the target bar.

    :param targets_number: Number of targets.
    :param target_is_presented: Presence of the target on screen.
    :param target_orientation_is_vertical: Orientation of the target. 'True' if vertical, 'False' if horizontal.

    :raises: :class:`ValueError`: 'Targets_number' isn't divisible by 4.
    
    :ivar targets_number: Number of targets.
    :ivar target_is_presented: Presence of the target on screen.
    :ivar target_orientation_is_vertical: Orientation of the target. 'True' if vertical, 'False' if horizontal.
    :ivar bars_to_display: Generated set of bars to display.
    """
    targets_number: int
    target_is_presented: bool
    target_orientation_is_vertical: bool
    bars_to_display: List[Bar]

    def __init__(self,
                 targets_number: int,
                 target_is_presented: bool,
                 target_orientation_is_vertical: bool):
        if targets_number / 4 != targets_number // 4:
            raise ValueError("'Targets_number' must be divisible by 4.")

        bars = []

        tov = target_orientation_is_vertical
        target_bar = lambda gs_id, bb_id, sh: Bar(gs_id, bb_id, True, tov, sh)
        red_bar = lambda gs_id, bb_id, sh: Bar(gs_id, bb_id, True, not tov, sh)
        green_bar = lambda gs_id, bb_id, sh: Bar(gs_id, bb_id, False, tov, sh)

        if target_is_presented:
            bar_constructors = create_shuffled_list([target_bar, red_bar, green_bar],
                                                    items_repeats=[1,
                                                                   targets_number // 2 - 1,
                                                                   targets_number // 2])
        else:
            bar_constructors = create_shuffled_list([red_bar, green_bar],
                                                    items_repeats=[targets_number // 2,
                                                                   targets_number // 2])

        # Bars divided between sectors in 1:1:1:1 ratio.
        bar_boxes_per_sector = targets_number // 4
        for grid_sector_id in range(4):
            bar_box_ids = create_shuffled_list([0, 1, 2, 3])
            for j in range(bar_boxes_per_sector):
                bar_box_id = bar_box_ids[j]
                # Random (x; y) shift.
                shift = (random(), random())
                bars.append(
                    bar_constructors[grid_sector_id * bar_boxes_per_sector + j](
                        grid_sector_id,
                        bar_box_id,
                        shift))

        self.targets_number = targets_number
        self.target_is_presented = target_is_presented
        self.target_orientation_is_vertical = target_orientation_is_vertical
        self.bars_to_display = bars
