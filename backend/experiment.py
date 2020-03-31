from random import random
from typing import Optional, List

import configuration
from backend.block import Block
import backend.block as block
from backend.trial import Trial
from backend.utils import create_shuffled_array


class Experiment:
    subject_name: str
    keyboard_key_for_presented: str
    keyboard_key_for_absent: str
    blocks: List[Block]
    current_block_id: int
    current_trial_id: int

    def __init__(self, subject_name: str):
        self.subject_name = subject_name
        if random() > 0.5:
            self.keyboard_key_for_presented = configuration.KEYBOARD_KEY_1.upper()
            self.keyboard_key_for_absent = configuration.KEYBOARD_KEY_2.upper()
        else:
            self.keyboard_key_for_presented = configuration.KEYBOARD_KEY_2.upper()
            self.keyboard_key_for_absent = configuration.KEYBOARD_KEY_1.upper()

        block_generators = [block.conjunction_condition_block,
                            block.switch_condition_block,
                            block.streak_condition_block,
                            block.random_condition_block]
        conditions_repeats = [configuration.CONJUNCTION_CONDITION_BLOCKS_NUMBER,
                              configuration.SWITCH_CONDITION_BLOCKS_NUMBER,
                              configuration.STREAK_CONDITION_BLOCKS_NUMBER,
                              configuration.RANDOM_CONDITION_BLOCKS_NUMBER]
        block_generators = create_shuffled_array(block_generators, items_repeats=conditions_repeats)
        self.blocks = [block_generator() for block_generator in block_generators]
        self.current_block_id = 0
        self.current_trial_id = 0
        self.__is_end__ = False

    def get_current_trial(self) -> Optional[Trial]:
        if self.__is_end__:
            return None
        return self.blocks[self.current_block_id].trials[self.current_trial_id]

    def go_next_trial(self) -> None:
        if self.__is_end__:
            return

        self.current_trial_id += 1
        if self.current_trial_id == configuration.TRIALS_PER_BLOCK:
            self.current_trial_id = 0
            self.current_block_id += 1
            if self.current_block_id == len(self.blocks):
                self.__is_end__ = True
