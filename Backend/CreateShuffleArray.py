from math import ceil
import random


def create_shuffled_array(items, expected_length=None, items_repeats=None):
    if items_repeats is None:
        items_repeats = [1] * len(items)
    if expected_length is None:
        expected_length = sum(items_repeats)

    if len(items) != len(items_repeats):
        raise IndexError("items and items_repeats have different length")

    res = []
    for i in range(len(items)):
        res.extend([items[i]] * items_repeats[i])
    res *= ceil(expected_length / sum(items_repeats))
    random.shuffle(res)

    return res
