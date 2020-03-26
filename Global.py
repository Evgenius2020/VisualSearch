import random
from math import ceil


def random_bool():
    return random.random() > 0.5


def get_counterbalanced_array(items, expected_length):
    res = []
    repeats = ceil(expected_length / len(items))
    for item in items:
        res.extend([item for _ in range(repeats)])
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


print(get_counterbalanced_array(range(1, 5), 5))
