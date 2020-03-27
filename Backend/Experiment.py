from Backend.Block import Block
import Backend.Conditions as cond
from Backend.Global import create_shuffled_array


class Experiment:
    def __init__(self):
        conditions = [cond.CONJUNCTION_CONDITION, cond.SWITCH_CONDITION, cond.STREAK_CONDITION, cond.RANDOM_CONDITION]
        conditions_repeats = [condition.blocks_number for condition in conditions]
        conditions = create_shuffled_array(conditions, items_repeats=conditions_repeats)
        self.blocks = [Block(condition) for condition in conditions]
