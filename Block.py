from random import random

from Global import Configuration as c, get_counterbalanced_array

from Conditions import Condition


class Trial:
    def __init__(self, targets_number, target_presence, target_orientation):
        self.targets_number = targets_number
        self.target_presence = target_presence
        self.orientation_is_vertical = target_orientation


class Block:
    def __init__(self, condition: Condition):
        orientation_is_vertical = random() > 0.5
        switches = condition.switch_generator_function(c.TRIALS_PER_BLOCK)
        targets_number = get_counterbalanced_array([4, 8, 12, 16], c.TRIALS_PER_BLOCK)
        target_presence = get_counterbalanced_array([True, False], c.TRIALS_PER_BLOCK)
        target_orientations = []
        trials = []
        for i in range(c.TRIALS_PER_BLOCK):
            if switches[i]:
                orientation_is_vertical = not orientation_is_vertical
            target_orientations.append(orientation_is_vertical)
            trials.append(Trial(targets_number[i], target_presence[i], target_orientations[i]))

        self.trials = trials