import copy
import unittest

from pack.point.point import Point


class TestPoint(unittest.TestCase):

    def test_supported_types(self):
        self.assertEqual(Point.fields_types, [int, float])
        self.assertEqual(type(10) in Point.fields_types, True)
        self.assertEqual(type(10.11) in Point.fields_types, True)

    def test_validation(self):
        x = Point(1, 5)

        self.assertEqual(x._validate(10), 10)
        self.assertEqual(x._validate(10.0), 10.0)
        with self.assertRaises(TypeError):
            x._validate('10')
        with self.assertRaises(TypeError):
            _ = Point(x)

    def test_operators(self):
        x = Point(1, 5)
        y = Point(42, 17.7)
        z = Point()

        self.assertTrue(x)
        self.assertFalse(z)

        z = copy.copy(x)

        self.assertTrue(x != y)
        self.assertTrue(x == z)
        self.assertFalse(x == y)
        self.assertFalse(x != z)

        z = x + y

        self.assertTrue(z.x, x.x + y.x)
        self.assertTrue(z.y, x.y + y.y)

        z = y - x

        self.assertTrue(z.x, x.x - y.x)
        self.assertTrue(z.y, x.y - y.y)

        z = copy.copy(x)
        x += y

        self.assertEqual(x.x, 43)
        self.assertEqual(x.y, 22.7)

        x -= y

        self.assertEqual(x.x, z.x)
        self.assertEqual(x.y, z.y)

    def test_distance(self):
        a, b = Point(1.5, 7), Point(42, 7)

        self.assertEqual(a.distance(b), 40.5)

    def test_represent(self):
        x = Point(1, 5.5)

        self.assertEqual(str(x), '(1, 5.5)')
        self.assertEqual(repr(x), '<Point(1, 5.5)>')
