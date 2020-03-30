from random import random

from Backend.Block import Block
import Backend.Conditions as cond
from Backend.CreateShuffledArray import create_shuffled_array
from Configuration import Configuration


class Experiment:
    def __init__(self, subject_name):
        conditions = [cond.conjunction_condition(),
                      cond.switch_condition(),
                      cond.streak_condition(),
                      cond.random_condition()]
        conditions_repeats = [condition.blocks_number for condition in conditions]
        conditions = create_shuffled_array(conditions, items_repeats=conditions_repeats)
        self.blocks = [Block(condition) for condition in conditions]
        self.current_block_id = 0
        self.current_trial_id = 0
        self.__is_end__ = False

        self.subject_name = subject_name
        if random() > 0.5:
            self.keyboard_key_for_presented = Configuration.KEYBOARD_KEY_1.upper()
            self.keyboard_key_for_absent = Configuration.KEYBOARD_KEY_2.upper()
        else:
            self.keyboard_key_for_presented = Configuration.KEYBOARD_KEY_2.upper()
            self.keyboard_key_for_absent = Configuration.KEYBOARD_KEY_1.upper()

    def get_current_trial(self):
        if self.__is_end__:
            return None
        return self.blocks[self.current_block_id].trials[self.current_trial_id]

    def go_next_trial(self):
        if self.__is_end__:
            return

        self.current_trial_id += 1
        if self.current_trial_id == Configuration.TRIALS_PER_BLOCK:
            self.current_trial_id = 0
            self.current_block_id += 1
            if self.current_block_id == len(self.blocks):
                self.__is_end__ = True
