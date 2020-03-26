import unittest

from Conditions import streak_switch_probability


class Tests(unittest.TestCase):
    def test_streak_switch_probability(self):
        right_probas = [0, 0, 0.09, 0.16, 0.21, 0.24, 0.25, 0.25, 0.25, 1, 1]
        for i in range(-1, 10):
            self.assertAlmostEqual(streak_switch_probability(i), right_probas[i + 1], 3)


if __name__ == '__main__':
    unittest.main()
