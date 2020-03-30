from dataclasses import dataclass
from random import random
from typing import List, Callable

from backend.utils import create_shuffled_array
import configuration


@dataclass
class Condition:
    name: str
    blocks_number: int
    switch_generator_function: Callable[[int], List[bool]]


def conjunction_condition() -> Condition:
    return Condition(configuration.CONJUNCTION_CONDITION_NAME,
                     configuration.CONJUNCTION_CONDITION_BLOCKS_NUMBER,
                     lambda length: [False for _ in range(length)])


def switch_condition() -> Condition:
    return Condition(configuration.SWITCH_CONDITION_NAME,
                     configuration.SWITCH_CONDITION_BLOCKS_NUMBER,
                     lambda length: [True for _ in range(length)])


def streak_condition() -> Condition:
    return Condition(configuration.STREAK_CONDITION_NAME,
                     configuration.STREAK_CONDITION_BLOCKS_NUMBER,
                     lambda length: streak_switch_generator(length))


def random_condition() -> Condition:
    return Condition(configuration.RANDOM_CONDITION_NAME,
                     configuration.RANDOM_CONDITION_BLOCKS_NUMBER,
                     lambda length: create_shuffled_array([True, False], length))


def streak_switch_probability(streak_length: int) -> float:
    if streak_length <= 0:
        return 0
    if streak_length >= 8:
        return 1
    if streak_length >= 5:
        return 0.25
    return streak_length * (0.1 - 0.01 * streak_length)


def streak_switch_generator(length: int) -> List[bool]:
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
