from random import random
from typing import Optional, List

import configuration
from backend.block import Block
import backend.block as block
from backend.trial import Trial
from backend.utils import create_shuffled_list


class Experiment:
    """
    Main data entity. Contains all experiment values (expect trial results).

    :param subject_name: Name of subject.

    :ivar subject_name: Name of subject.
    :ivar keyboard_key_for_presented: Keyboard key that associated with 'target presented' response.
    :ivar keyboard_key_for_absent: Keyboard key that associated with 'target absent' response.
    :ivar blocks: Generated set of blocks with specified (in configuration.py) condition counterbalance.
    :ivar current_block_id: Index of current block.
    :ivar current_trial_id: Index of current trial.
    :ivar is_block_passed: Completeness of block. Block is complete if its last trial has passed.
    :ivar is_experiment_end: Completeness of experiment. Experiment is complete if its last block has passed.
    """
    subject_name: str
    keyboard_key_for_presented: str
    keyboard_key_for_absent: str
    blocks: List[Block]
    current_block_id: int
    current_trial_id: int
    is_block_passed: bool
    is_experiment_end: bool

    def __init__(self,
                 subject_name: str):
        self.subject_name = subject_name
        # Randomized keyboard bindings.
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
        # Random conditions sequence.
        block_generators = create_shuffled_list(block_generators, items_repeats=conditions_repeats)
        self.blocks = [block_generator() for block_generator in block_generators]
        self.current_block_id = 0
        self.current_trial_id = 0
        self.is_block_passed = False
        self.is_experiment_end = False

    def get_current_trial(self) -> Optional[Trial]:
        """
        Get current trial.

        :return: Current trial or 'None' if experiment is complete.
        """
        if self.is_experiment_end:
            return None
        return self.blocks[self.current_block_id].trials[self.current_trial_id]

    def go_next_trial(self) -> None:
        """
        Go to next trial.
        """
        if self.is_experiment_end:
            return

        self.current_trial_id += 1
        if self.current_trial_id == configuration.TRIALS_PER_BLOCK:
            self.current_trial_id = 0
            self.current_block_id += 1
            self.is_block_passed = True
            if self.current_block_id == len(self.blocks):
                self.is_experiment_end = True
