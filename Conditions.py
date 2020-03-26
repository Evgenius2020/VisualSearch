from random import random

TRIALS_PER_BLOCK = 100
MAX_STREAK_LENGTH = 8


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


def streak_switch_probability(streak_length):
    if streak_length <= 0:
        return 0
    if streak_length >= MAX_STREAK_LENGTH:
        return 1
    if streak_length >= 5:
        return 0.25
    return streak_length * (0.1 - 0.01 * streak_length)


class Condition:
    def __init__(self, name, blocks_number, switch_generator_function):
        self.name = name
        self.blocks_number = blocks_number
        self.switch_generator_function = switch_generator_function


CONJUNCTION_CONDITION = Condition("CONJUNCTION", 3, lambda length: [False for _ in range(length)])
SWITCH_CONDITION = Condition("SWITCH", 3, lambda length: [True for _ in range(length)])
STREAK_CONDITION = Condition("STREAK", 3, lambda length: streak_switch_generator(length))
RANDOM_CONDITION = Condition("RANDOM", 8, lambda length: [random() > 0.5 for _ in range(length)])