from random import random
from typing import List

from Backend.conditions import Condition
from Backend.utils import create_shuffled_array
from Backend.trial import Trial
from Configuration import Configuration as c


class Block:
    condition: Condition
    trials: List[Trial]

    def __init__(self, condition: Condition):
        orientation_is_vertical = random() > 0.5
        switches = condition.switch_generator_function(c.TRIALS_PER_BLOCK)
        targets_number = create_shuffled_array([4, 8, 12, 16], c.TRIALS_PER_BLOCK)
        target_is_presented = create_shuffled_array([True, False], c.TRIALS_PER_BLOCK)
        target_orientations = []
        trials = []
        for i in range(c.TRIALS_PER_BLOCK):
            if switches[i]:
                orientation_is_vertical = not orientation_is_vertical
            target_orientations.append(orientation_is_vertical)
            trials.append(Trial(targets_number[i],
                                target_is_presented[i],
                                target_orientations[i]))

        self.condition = condition
        self.trials = trials
