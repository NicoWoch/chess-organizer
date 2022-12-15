import unittest

from src.algorithms.elo import elo_rating


class MyTestCase(unittest.TestCase):
    def assert_almost_equal(self, ratings1, ratings2):
        for r1, r2 in zip(ratings1, ratings2):
            if not r2 - 1 < r1 < r2 + 1:
                self.fail(f'{ratings1} should almost equal {ratings2}')

    def test_1(self):
        self.assert_almost_equal(elo_rating(1200, 1500, 1, k=30), (1225.5, 1474.5))

    def test_2(self):
        self.assert_almost_equal(elo_rating(1310, 1840, 0, k=15), (1309.3, 1840.7))

    def test_3(self):
        self.assert_almost_equal(elo_rating(1770, 2040, 0.5, k=15), (1774.9, 2035.1))

    def test_4(self):
        self.assert_almost_equal(elo_rating(1840, 1990, 1), (1854.1, 1975.9))

    def test_5(self):
        self.assert_almost_equal(elo_rating(1270, 1850, 0.5), (1279.3, 1840.7))


if __name__ == '__main__':
    unittest.main()
