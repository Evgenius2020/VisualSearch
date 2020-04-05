from random import random
from typing import List, Callable

from backend.utils import create_shuffled_list
from backend.trial import Trial
import configuration


class Block:
    """
    Contains random generated set of trials.
    Trials generation algorithm depends on rotations generator of experiment condition.
    Initial target orientation is random and changes from trial to trial by rotations generator output.

    :param condition_name: Name of condition.
    :param rotations_generator: Function that returns list of bool (True = 'rotate') values with specified length.
    :param trials_number: Number of trials to generate.

    :ivar condition_name: Name of condition.
    :ivar trials: Generated set of trials.
    """
    condition_name: str
    trials: List[Trial]

    def __init__(self,
                 condition_name: str,
                 rotations_generator: Callable[[int], List[bool]],
                 trials_number: int = configuration.TRIALS_PER_BLOCK):
        orientation_is_vertical = random() > 0.5
        switches = rotations_generator(trials_number)
        targets_number = create_shuffled_list([4, 8, 12, 16], trials_number)
        target_is_presented = create_shuffled_list([True, False], trials_number)
        target_orientations = []
        trials = []
        for i in range(trials_number):
            if switches[i]:
                orientation_is_vertical = not orientation_is_vertical
            target_orientations.append(orientation_is_vertical)
            trials.append(Trial(targets_number[i],
                                target_is_presented[i],
                                target_orientations[i]))

        self.condition_name = condition_name
        self.trials = trials


def conjunction_condition_block() -> Block:
    """
    Create block with 'conjunction' condition, when target orientation is constant.

    :return: 'Conjunction' condition block.
    """
    return Block(configuration.CONJUNCTION_CONDITION_NAME,
                 conjunction_rotations_generator)


def switch_condition_block() -> Block:
    """
    Create block with 'switch' condition, when target orientation changes every trial.

    :return: 'Switch' condition block.
    """
    return Block(configuration.SWITCH_CONDITION_NAME,
                 switch_rotations_generator)


def streak_condition_block() -> Block:
    """
    Create block with 'streak' condition, when rotation probability is low and
    target orientation repeats continuously in 1-8 trials.

    :return: 'Streak' condition block.
    """
    return Block(configuration.STREAK_CONDITION_NAME,
                 streak_rotations_generator)


def random_condition_block() -> Block:
    """
    Create block with 'random' condition, when rotation is random.

    :return: 'Random' condition block.
    """
    return Block(configuration.RANDOM_CONDITION_NAME,
                 random_rotations_generator)


def conjunction_rotations_generator(length: int) -> List[bool]:
    """
    Generate rotations list for 'conjunction' block (no rotations).

    :param length: Length of rotation list to generate.

    :return: 'Conjunction' rotations list.
    """
    return [False for _ in range(length)]


def switch_rotations_generator(length: int) -> List[bool]:
    """
    Generate rotations list for 'switch' block (rotation always).

    :param length: Length of rotation list to generate.

    :return: 'Switch' rotations list.
    """
    return [True for _ in range(length)]


def streak_rotation_probability(streak_length: int) -> float:
    """
    Get rotation probability which depends on 'no rotation' streak length.
    Formula taken from section '2.3. Procedure'.

    :param: 'No rotation' streak length.

    :return: Rotation probability in the [0.0; 1.0] range.
    """
    if streak_length <= 0:
        return 0
    if streak_length >= 8:
        return 1
    if streak_length >= 5:
        return 0.25
    return streak_length * (0.1 - 0.01 * streak_length)


def streak_rotations_generator(length: int) -> List[bool]:
    """
    Generate rotations list for 'streak' block (steaks of 'no rotation').

    :param length: Length of rotation list to generate.

    :return: "Switch' rotations list.
    """
    result = []
    streak_length = 1
    for _ in range(length):
        if random() > streak_rotation_probability(streak_length):
            result.append(False)
            streak_length += 1
        else:
            result.append(True)
            streak_length = 1
    return result


def random_rotations_generator(length: int) -> List[bool]:
    """
    Generate rotations list for 'random' block (rotation by random).

    :param length: Length of rotation list to generate.

    :return: 'Random' rotations list.
    """
    return create_shuffled_list([True, False], length)
