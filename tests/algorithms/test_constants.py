import unittest

from src.algorithms.constants import Result, Points
from src.config import Config


class TestResult(unittest.TestCase):
    def test_opposite_1(self):
        self.assertEqual(Result.White.opposite(), Result.Black)
        self.assertEqual(Result.Draw.opposite(), Result.Draw)
        self.assertEqual(Result.Black.opposite(), Result.White)
        self.assertEqual(Result.Playing.opposite(), Result.Playing)

    def test_opposite_2(self):
        for x in Result:
            self.assertEqual(x.opposite().opposite(), x)

    def test_get_points(self):
        self.assertEqual(Result.White.get_points(), Config.WIN_POINTS)
        self.assertEqual(Result.Draw.get_points(), Config.DRAW_POINTS)
        self.assertEqual(Result.Black.get_points(), Config.LOSE_POINTS)
        self.assertEqual(Result.Playing.get_points(), 0)


class TestPoints(unittest.TestCase):
    def test_constructor(self):
        p = Points(3)
        self.assertEqual(p.big, 0)
        self.assertEqual(p.small, (0, 0, 0))

    def test_adding_points(self):
        p = Points(2)
        p.big += 5
        p.add_small_points((2, 5))
        p.add_small_points((-1, -2))
        self.assertEqual(p.big, 5)
        self.assertEqual(p.small, (1, 3))


if __name__ == '__main__':
    unittest.main()
