from math import ceil
import random
from typing import List


def create_shuffled_array(
        items: List,
        expected_length: int = None,
        items_repeats: List[int] = None) -> List:
    """Creates list of shuffled 'items' elements

    :param items: source list
    :param expected_length: expected length of result list; if it greater that len(items), repeats items
    :param items_repeats: list of repeats number for each element
    :return:
    """
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