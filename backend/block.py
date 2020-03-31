from random import random
from typing import List, Callable

from backend.utils import create_shuffled_array
from backend.trial import Trial
import configuration


class Block:
    condition_name: str
    trials: List[Trial]

    def __init__(self,
                 condition_name: str,
                 rotations_generator: Callable[[int], List[bool]]):
        orientation_is_vertical = random() > 0.5
        switches = rotations_generator(configuration.TRIALS_PER_BLOCK)
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

        self.condition_name = condition_name
        self.trials = trials


def conjunction_condition_block() -> Block:
    return Block(configuration.CONJUNCTION_CONDITION_NAME,
                 conjunction_rotations_generator)


def switch_condition_block() -> Block:
    return Block(configuration.SWITCH_CONDITION_NAME,
                 switch_rotations_generator)


def streak_condition_block() -> Block:
    return Block(configuration.STREAK_CONDITION_NAME,
                 streak_rotations_generator)


def random_condition_block() -> Block:
    return Block(configuration.RANDOM_CONDITION_NAME,
                 random_rotations_generator)


def conjunction_rotations_generator(length: int) -> List[bool]:
    return [False for _ in range(length)]


def switch_rotations_generator(length: int) -> List[bool]:
    return [True for _ in range(length)]


def streak_switch_probability(streak_length: int) -> float:
    if streak_length <= 0:
        return 0
    if streak_length >= 8:
        return 1
    if streak_length >= 5:
        return 0.25
    return streak_length * (0.1 - 0.01 * streak_length)


def streak_rotations_generator(length: int) -> List[bool]:
    result = []
    streak_length = 1
    for _ in range(length):
        if random() > streak_switch_probability(streak_length):
            result.append(False)
            streak_length += 1
        else:
            result.append(True)
            streak_length = 1
    return result


def random_rotations_generator(length: int) -> List[bool]:
    return create_shuffled_array([True, False], length)
