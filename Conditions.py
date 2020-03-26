from random import random

from Global import Configuration as c, get_counterbalanced_array


class Condition:
    def __init__(self, name, blocks_number, switch_generator_function):
        self.name = name
        self.blocks_number = blocks_number
        self.switch_generator_function = switch_generator_function


CONJUNCTION_CONDITION = Condition(c.CONJUNCTION_CONDITION_BLOCKS_NUMBER, c.CONJUNCTION_CONDITION_BLOCKS_NUMBER,
                                  lambda length: [False for _ in range(length)])
SWITCH_CONDITION = Condition(c.SWITCH_CONDITION_NAME, c.SWITCH_CONDITION_BLOCKS_NUMBER,
                             lambda length: [True for _ in range(length)])
STREAK_CONDITION = Condition(c.STREAK_CONDITION_NAME, c.STREAK_CONDITION_BLOCKS_NUMBER,
                             lambda length: streak_switch_generator(length))
RANDOM_CONDITION = Condition(c.RANDOM_CONDITION_NAME, c.RANDOM_CONDITION_BLOCKS_NUMBER,
                             lambda length: get_counterbalanced_array([True, False], length))


def streak_switch_probability(streak_length):
    if streak_length <= 0:
        return 0
    if streak_length >= 8:
        return 1
    if streak_length >= 5:
        return 0.25
    return streak_length * (0.1 - 0.01 * streak_length)


def streak_switch_generator(length):
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
