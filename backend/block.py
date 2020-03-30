from random import random
from typing import List

from backend.conditions import Condition
from backend.utils import create_shuffled_array
from backend.trial import Trial
import configuration


class Block:
    condition: Condition
    trials: List[Trial]

    def __init__(self, condition: Condition):
        orientation_is_vertical = random() > 0.5
        switches = condition.switch_generator_function(configuration.TRIALS_PER_BLOCK)
        targets_number = create_shuffled_array([4, 8, 12, 16], configuration.TRIALS_PER_BLOCK)
        target_is_presented = create_shuffled_array([True, False], configuration.TRIALS_PER_BLOCK)
        target_orientations = []
        trials = []
        for i in range(configuration.TRIALS_PER_BLOCK):
            if switches[i]:
                orientation_is_vertical = not orientation_is_vertical
            target_orientations.append(orientation_is_vertical)
            trials.append(Trial(targets_number[i],
                                target_is_presented[i],
                                target_orientations[i]))

        self.condition = condition
        self.trials = trials
