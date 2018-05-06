import copy
import unittest

from pack.car.car import Car, OutOfFuel, TooMuchFuel
from pack.point.point import Point


class TestCar(unittest.TestCase):

    car = Car(50, 0.7, Point(2, 21.11), 'Zpa')

    def test_init(self):
        self.assertEqual(self.car.fuel_amount, 0)
        self.assertEqual(self.car.fuel_capacity, 50)
        self.assertEqual(self.car.fuel_consumption, 0.7)
        self.assertEqual(repr(self.car.location), '<Point(2, 21.11)>')
        self.assertEqual(self.car.model, 'Zpa')

        with self.assertRaises(TypeError):
            _ = Car('50', 0.7, Point(2, 21.11), 'Zpa')
        with self.assertRaises(TypeError):
            _ = Car(50, 0.7, 7, 'Zpa')
        with self.assertRaises(TypeError):
            _ = Car(50, 0.7, 'point', 'Zpa')

    def test_car_copy(self):
        car_copy = copy.copy(self.car)

        self.assertFalse(id(self.car) == id(car_copy))
        self.assertFalse(id(self.car.location) == id(car_copy.location))

        self.assertEqual(car_copy.fuel_amount, 0)
        self.assertEqual(car_copy.fuel_capacity, 50)
        self.assertEqual(car_copy.fuel_consumption, 0.7)
        self.assertEqual(repr(car_copy.location), '<Point(2, 21.11)>')
        self.assertEqual(car_copy.model, 'Zpa')

    def test_representation(self):
        self.assertEqual(str(self.car),
                         'Car Zpa [fuel:50/0, location:(2, 21.11)]')

    def test_compute_fuel_needed(self):
        self.assertEqual(self.car.compute_fuel_needed(Point(12, 21.11)), 7)
        self.assertEqual(self.car.compute_fuel_needed(Point(2, 31.11)), 7)

    def test_car_refill(self):
        car_ = Car(50, 0.7, Point(2, 21.11), 'Zpa')

        self.assertFalse(car_.fuel_amount)

        car_.refill(10)

        self.assertTrue(car_.fuel_amount)
        self.assertEqual(car_.fuel_amount, 10)

        with self.assertRaises(TooMuchFuel):
            car_.refill(50)

    def test_car_drive(self):
        car_ = Car(50, 0.7, Point(2, 21.11), 'Zpa')
        destination = Point(22, 21.11)

        with self.assertRaises(OutOfFuel):
            car_.drive(destination)

        car_.refill(25)
        car_.drive(destination)

        self.assertEqual(repr(car_.location), '<Point(22, 21.11)>')
        self.assertEqual(car_.fuel_amount, 11.0)

        with self.assertRaises(TypeError):
            car_.drive(4, 5, 6)
        with self.assertRaises(TypeError):
            car_.drive(4, destination)
        with self.assertRaises(TypeError):
            car_.drive(destination, destination)
        with self.assertRaises(TypeError):
            car_.drive(10)
        with self.assertRaises(TypeError):
            car_.drive()
        with self.assertRaises(TypeError):
            car_.drive('coordinates')
