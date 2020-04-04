from math import ceil
import random
from typing import List


def create_shuffled_list(
        items: list,
        expected_length: int = None,
        items_repeats: List[int] = None) -> list:
    """
    Creates list of shuffled 'items' elements with specified number of repeats.

    :param items: Source list of elements.
    :param expected_length: Expected length of result list.
        If 'expected_length' greater that len(items), repeats 'items' to reach this value.
    :param items_repeats: List of repeats number for each element.

    :raises: :class:`IndexError`: 'Items' and 'items_repeats' have different length.

    :return: List of shuffled elements from 'item'.
    """
    if items_repeats is None:
        items_repeats = [1] * len(items)
    if expected_length is None:
        expected_length = sum(items_repeats)

    if len(items) != len(items_repeats):
        raise IndexError("'Items' and 'items_repeats' have different length.")

    res = []
    for i in range(len(items)):
        res.extend([items[i]] * items_repeats[i])
    res *= ceil(expected_length / sum(items_repeats))
    random.shuffle(res)

    return res
