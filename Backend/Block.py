from random import random

from Backend.CreateShuffledArray import create_shuffled_array
from Backend.Trial import Trial
from Configuration import Configuration as c
from Backend.Conditions import Condition


class Block:
    def __init__(self, condition: Condition):
        self.condition = condition
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
            trials.append(Trial(targets_number[i], target_is_presented[i], target_orientations[i]))

        self.trials = trials
