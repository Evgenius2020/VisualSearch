import unittest

from Conditions import streak_switch_probability
from Global import create_shuffled_array


class Tests(unittest.TestCase):
    def test_streak_switch_probability(self):
        right_probas = [0, 0, 0.09, 0.16, 0.21, 0.24, 0.25, 0.25, 0.25, 1, 1]
        for i in range(-1, 10):
            self.assertAlmostEqual(streak_switch_probability(i), right_probas[i + 1], 3)

    def test_create_shuffled_array(self):
        def check_shuffle(items, expected_entries):
            unique_elements = {el: None for el in items}
            actual_entries = {item: items.count(item) for item in unique_elements.keys()}
            self.assertDictEqual(actual_entries, expected_entries)

        check_shuffle(create_shuffled_array(range(1, 5), 25), {1: 7, 2: 7, 3: 7, 4: 7})
        check_shuffle(create_shuffled_array(range(1, 5), 24), {1: 6, 2: 6, 3: 6, 4: 6})
        check_shuffle(create_shuffled_array([1, 2, 3, 4], 10, [1, 2, 3, 4]), {1: 1, 2: 2, 3: 3, 4: 4})
        check_shuffle(create_shuffled_array([1, 2, 3, 4], 11, [1, 2, 3, 4]), {1: 2, 2: 4, 3: 6, 4: 8})

        if __name__ == '__main__':
            unittest.main()
