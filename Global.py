import random
from math import ceil


def random_bool():
    return random.random() > 0.5


def create_shuffled_array(items, expected_length, items_repeats=None):
    if items_repeats is None:
        items_repeats = [1] * len(items)

    if len(items) != len(items_repeats):
        raise IndexError("items and items_repeats have different length")

    res = []
    for i in range(len(items)):
        res.extend([items[i]] * items_repeats[i])
    res *= ceil(expected_length / sum(items_repeats))
    random.shuffle(res)

    return res


class Configuration:
    CONJUNCTION_CONDITION_NAME = "CONJUNCTION"
    SWITCH_CONDITION_NAME = "SWITCH"
    STREAK_CONDITION_NAME = "STREAK"
    RANDOM_CONDITION_NAME = "RANDOM"

    CONJUNCTION_CONDITION_BLOCKS_NUMBER = 3
    SWITCH_CONDITION_BLOCKS_NUMBER = 3
    STREAK_CONDITION_BLOCKS_NUMBER = 8
    RANDOM_CONDITION_BLOCKS_NUMBER = 3

    TRIALS_PER_BLOCK = 100
