from random import random

from Backend.Block import Block
import Backend.Conditions as cond
from Backend.CreateShuffledArray import create_shuffled_array
from Configuration import Configuration


class Experiment:
    def __init__(self):
        conditions = [cond.CONJUNCTION_CONDITION, cond.SWITCH_CONDITION, cond.STREAK_CONDITION, cond.RANDOM_CONDITION]
        conditions_repeats = [condition.blocks_number for condition in conditions]
        conditions = create_shuffled_array(conditions, items_repeats=conditions_repeats)
        self.blocks = [Block(condition) for condition in conditions]
        self.__current_block__ = 0
        self.__current_trial__ = 0
        self.__is_end__ = False
        if random() > 0.5:
            Configuration.KEYBOARD_KEY_FOR_PRESENTED = Configuration.KEYBOARD_KEY_1.upper()
            Configuration.KEYBOARD_KEY_FOR_ABSENT = Configuration.KEYBOARD_KEY_2.upper()
        else:
            Configuration.KEYBOARD_KEY_FOR_PRESENTED = Configuration.KEYBOARD_KEY_2.upper()
            Configuration.KEYBOARD_KEY_FOR_ABSENT = Configuration.KEYBOARD_KEY_1.upper()

    def get_current_trial(self):
        if self.__is_end__:
            return None
        return self.blocks[self.__current_block__].trials[self.__current_trial__]

    def go_next_trial(self):
        if self.__is_end__:
            return
        
        self.__current_trial__ += 1
        if self.__current_trial__ == Configuration.TRIALS_PER_BLOCK:
            self.__current_trial__ = 0
            self.__current_block__ += 1
            if self.__current_block__ == len(self.blocks):
                self.__is_end__ = True
