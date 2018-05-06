__author__ = 'ekunra'

from math import hypot


class Point(object):
    """A Point class represents a point on the coordinate plane with
    two coordinates (x, y) stored in one object."""

    fields_types = [int, float]

    def _validate(self, value: int or float) -> int or float:
        """
        Data type validator.

        :param value: Value to validate
        :type value: int or float
        :raise TypeError: If value type is unsupported
        :rtype: int or float
        :return: Validated value
        """

        if type(value) not in self.fields_types:
            raise TypeError

        return value

    def __init__(self, x: int or float = 0, y: int or float =0):
        """
        The initializer

        :param x: The abscissa
        :type x: int or float
        :param y: The ordinate
        :type y: int or float
        :raise TypeError: If params don't pass validation
        """

        self._x = self._validate(x)
        self._y = self._validate(y)

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __repr__(self):
        return f'<{self.__class__.__name__}({self.x}, {self.y})>'

    def __eq__(self, other):
        return self._x == other.x and self._y == other.y

    def __ne__(self, other):
        return not self == other

    def __add__(self, other):
        return self.__class__(self._x + other.x, self._y + other.y)

    def __sub__(self, other):
        return self.__class__(self._x - other.x, self._y - other.y)

    def __radd__(self, other):
        return self.__class__(other.x - self._x, other.y - self._y)

    def __rsub__(self, other):
        return self.__class__(other.x - self._x, other.y - self._y)

    def __iadd__(self, other):
        self._x += other.x
        self._y += other.y
        return self

    def __isub__(self, other):
        self._x -= other.x
        self._y -= other.y
        return self

    def __bool__(self):
        return True if self._x or self._y else False

    def __copy__(self):
        return self.__class__(self.x, self.y)

    def distance(self, other):
        """Returns a distance between two Points"""
        return hypot(self._x - other.x, self._y - other.y)

    @property
    def x(self) -> int or float:
        return self._x

    @property
    def y(self) -> int or float:
        return self._y

    @x.setter
    def x(self, value: int or float):
        self._x = self._validate(value)

    @y.setter
    def y(self, value: int or float):
        self._y = self._validate(value)


if __name__ == '__main__':
    p1 = Point(3, 42)
