import unittest

from Backend.block import Block
from Backend.conditions import streak_switch_probability
import Backend.conditions as cond
from Backend.utils import create_shuffled_array
from Configuration import Configuration as c


class Tests(unittest.TestCase):
    def test_streak_switch_probability(self):
        right_probas = [0, 0, 0.09, 0.16, 0.21, 0.24, 0.25, 0.25, 0.25, 1, 1]
        for i in range(-1, 10):
            self.assertAlmostEqual(streak_switch_probability(i), right_probas[i + 1], 3)

    def check_entries(self, items, expected_entries):
        unique_elements = {el: None for el in items}
        actual_entries = {item: items.count(item) for item in unique_elements.keys()}
        self.assertDictEqual(actual_entries, expected_entries)

    def test_create_shuffled_array(self):
        self.check_entries(create_shuffled_array(range(1, 5), 25), {1: 7, 2: 7, 3: 7, 4: 7})
        self.check_entries(create_shuffled_array(range(1, 5), 24), {1: 6, 2: 6, 3: 6, 4: 6})
        self.check_entries(create_shuffled_array([1, 2, 3, 4], 10, [1, 2, 3, 4]), {1: 1, 2: 2, 3: 3, 4: 4})
        self.check_entries(create_shuffled_array([1, 2, 3, 4], items_repeats=[1, 2, 3, 4]), {1: 1, 2: 2, 3: 3, 4: 4})
        self.check_entries(create_shuffled_array([1, 2, 3, 4], 11, [1, 2, 3, 4]), {1: 2, 2: 4, 3: 6, 4: 8})
        self.check_entries(create_shuffled_array([1, 2, 3]), {1: 1, 2: 1, 3: 1})

    def test_conditions_switch_generators(self):
        switches = cond.conjunction_condition().switch_generator_function(10000)
        self.check_entries(switches, {False: 10000})

        switches = cond.switch_condition().switch_generator_function(10000)
        self.check_entries(switches, {True: 10000})

        switch_cond_length = 10000
        switches = cond.streak_condition().switch_generator_function(switch_cond_length)
        streak_size = 1
        streaks = {}
        for i in range(switch_cond_length):
            if switches[i]:
                if streak_size not in streaks:
                    streaks[streak_size] = 0
                streaks[streak_size] += 1
                streak_size = 0
            streak_size += 1
        self.assertLessEqual(len(streaks.keys()), 8)

        switches = cond.random_condition().switch_generator_function(10000)
        self.check_entries(switches, {True: 5000, False: 5000})

    def test_block_generation(self):
        c.TRIALS_PER_BLOCK = 100  # must be divided by 4
        tpb = c.TRIALS_PER_BLOCK

        conj_block = Block(cond.conjunction_condition())
        self.assertEqual(len(conj_block.trials), c.TRIALS_PER_BLOCK)
        self.check_entries([trial.target_is_presented for trial in conj_block.trials], {True: tpb / 2, False: tpb / 2})
        self.check_entries([trial.targets_number for trial in conj_block.trials],
                           {4: tpb / 4, 8: tpb / 4, 12: tpb / 4, 16: tpb / 4})
        start_orientation_is_vertical = conj_block.trials[0].target_orientation_is_vertical
        orientations = [trial.target_orientation_is_vertical for trial in conj_block.trials]
        self.assertListEqual(orientations, [start_orientation_is_vertical] * len(conj_block.trials))

        switch_block = Block(cond.switch_condition())
        orientations = [trial.target_orientation_is_vertical for trial in switch_block.trials]
        self.check_entries(orientations, {True: tpb / 2, False: tpb / 2})

        if __name__ == '__main__':
            unittest.main()
