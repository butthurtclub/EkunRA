import copy
from pack.point.point import Point


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class OutOfFuel(Error):
    """Exception raised in case of run out of fuel.

    Attributes:
        message -- explanation or specific details of the error
    """

    def __init__(self, message=None):
        if message is not None:
            self.message = message
        else:
            self.message = 'Out of fuel.'


class TooMuchFuel(Error):
    """Exception raised in case of overloading of fuel while refilling.

    Attributes:
        message -- explanation or specific details of the error
    """

    def __init__(self, message=None):
        if message is not None:
            self.message = message
        else:
            self.message = f'Fuel amount to refill is bigger than ' \
                           f'fuel tank capacity.'


class Car:
    """Class representing car prototype and its behavior"""

    def _validate_numeric(self, num):
        """
        Checks if number of correct Type.

        :param num: Number to validate
        :type num: Any
        :raise TypeError: In case argument is not int or float
        :return: Validated number
        :rtype: int or float
        """

        types_allowed = [int, float]

        if type(num) not in types_allowed:
            raise TypeError

        return num

    def _validate_location_point(self, point):
        """
        Checks if location data of correct Type.

        :param point: location data to validate
        :type point: Any
        :raise TypeError: In case argument is not Point class object

        :return: Validated number
        :rtype: Point
        """

        if not isinstance(point, Point):
            raise TypeError

        return point

    def __init__(self, f_capacity: float = 50, f_consumption: float = 0.6,
                 car_location: Point = Point(), car_model: str = 'Trash'):
        """
        Initializer

        :param f_capacity: The capacity of FuelTank
        :type f_capacity: int
        :param f_consumption: Fuel consumption per unit of distance
        :type f_consumption: float
        :param car_location: Car's location
        :type car_location: Point
        :param car_model: Car's model name
        :type car_model: str
        :raise TypeError: object instantiated with incorrect data
        """

        self._fuel_amount = 0
        self._fuel_capacity = self._validate_numeric(f_capacity)
        self._fuel_consumption = self._validate_numeric(f_consumption)
        self._location = self._validate_location_point(car_location)
        self._model = car_model

    def __copy__(self):
        car_copy = Car(self._fuel_capacity,
                       self._fuel_consumption,
                       copy.copy(self._location),
                       self._model)
        car_copy.fuel_amount = self.fuel_amount
        return car_copy

    def __str__(self):
        return f'Car {self._model} [' \
               f'fuel:{round(self._fuel_capacity, 2)}/' \
               f'{round(self._fuel_amount, 2)}, ' \
               f'location:{self._location}]'

    def compute_fuel_needed(self, destination: Point):
        """
        Compute needed amount of fuel to move to destination.

        :param destination: Destination point
        :type destination: Point

        :return: needed amount of fuel
        :rtype: int or float
        """

        path_length = self._location.distance(destination)
        return path_length * self._fuel_consumption

    def drive(self, *args):
        """
        Make Car to move from current position to received coordinates.

        :param args: Coordinates as x & y or Point
        :type args: 1 or 2 elements list
        :raise TypeError: Inappropriate or more than 2 arguments
        passed to function.

        :return: Nothing
        :rtype: None
        """

        if len(args) > 2 or len(args) < 1:
            raise TypeError('drive() takes from 1 to 2 arguments ')

        if len(args) == 1 and isinstance(args[0], Point):
            if self._fuel_amount == 0:
                raise OutOfFuel('Zero fuel amount in fuel tank')

            fuel_needed = self.compute_fuel_needed(args[0])

            if fuel_needed > self._fuel_amount:
                return

            self._fuel_amount -= fuel_needed
            self._location = args[0]

        elif len(args) == 2 and all(isinstance(_, int) for _ in args):
            self.drive(Point(args[0], args[1]))

        else:
            raise TypeError(f'drive() takes either two integer/float '
                            f'numbers as some Point coordinates '
                            f'either one Point class object')

    def refill(self, fuel_amount: int or float):
        """
        Refill Car's fuel tank with certain fuel amount.

        :param fuel_amount: Quantity of fuel to be added
        :type fuel_amount: int or float

        :return: Nothing
        :rtype: None
        """
        refuel_amount = self._validate_numeric(fuel_amount)

        if refuel_amount > self._fuel_capacity - self._fuel_amount:
            raise TooMuchFuel()

        self._fuel_amount += refuel_amount
        if self._fuel_amount > self.fuel_capacity:
            self.fuel_amount = self._fuel_capacity

    @property
    def fuel_amount(self):
        return self._fuel_amount

    @property
    def fuel_capacity(self):
        return self._fuel_capacity

    @property
    def fuel_consumption(self):
        return self._fuel_consumption

    @property
    def location(self):
        return self._location

    @property
    def model(self):
        return self._model

    @fuel_amount.setter
    def fuel_amount(self, value):
        self._fuel_amount = value

    @fuel_capacity.setter
    def fuel_capacity(self, value):
        self._fuel_capacity = value

    @location.setter
    def location(self, value):
        self._location = value

    @model.setter
    def model(self, value):
        self._model = value
