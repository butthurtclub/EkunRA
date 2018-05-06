

class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class UnitIsDead(Error):
    """Exception raised for errors in the input.

    Attributes:
        message -- explanation or specific details of the error
    """

    def __init__(self, message=None):
        if message is not None:
            self.message = message
        else:
            self.message = 'Unit is dead!'


class Unit(object):
    def __ensure_is_alive(self, message):
        if self._health_points <= 0:
            raise UnitIsDead(message=message)

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

    def _validate_string(self, name):
        """
        Checks if name of correct Type.

        :param name: Number to validate
        :type name: str
        :raise TypeError: In case argument is not str

        :return: Validated string
        :rtype: str
        """

        if not isinstance(name, str):
            raise TypeError

        return name

    def __init__(self, name, hp=100, dmg=20.5):
        """
        Initializer

        :param hp: Unit's health points
        :type hp: int or float
        :param dmg: Unit's damage dealing points
        :type dmg: int or float
        :param name: Unit's name
        :type name: str
        :raise TypeError: object instantiated with incorrect data
        """

        self._health_points = self._validate_numeric(hp)
        self._health_points_limit = self._validate_numeric(hp)
        self._damage = self._validate_numeric(dmg)
        self._name = self._validate_string(name)

    def __str__(self):
        return f'{self._name} [' \
               f'hp:{round(self._health_points, 2)}/' \
               f'{self._health_points_limit}, ' \
               f'damage:{self._damage}]'

    def __repr__(self):
        return f'<{self.__class__.__name__} [name:{self._name}, ' \
               f'hp:{self._health_points}/{self._health_points_limit}, ' \
               f'damage:{self._damage}]>'

    def add_health_points(self, hp):
        """
        Add Health point to Unit's health points if its alive.

        :param hp: Health point to be added
        :type hp: int or float
        :raises UnitIsDead, TypeError: Unit is dead, incorrect data.

        :return: Nothing
        :rtype: None
        """

        self.__ensure_is_alive(f"{self._name} can't restore health "
                               f"as it already dead")

        self._health_points += self._validate_numeric(hp)
        if self._health_points > self._health_points_limit:
            self._health_points = self._health_points_limit

    def take_damage(self, dmg):
        """
        Applies damage done.

        :param dmg: Damage to be applied to Unit
        :type dmg: int or float
        :raise TypeError: incorrect arg Type

        :return: Nothing
        :rtype: None
        """

        self._health_points -= self._validate_numeric(dmg)
        if self._health_points < 0:
            self._health_points = 0

    def attack(self, enemy):
        """
        Making physical damage to an enemy.

        :param enemy: Enemy need to be attacked
        :type enemy: Unit
        :raise UnitIsDead: In case Unit's health is equal to zero.

        :return: Nothing
        :rtype: None
        """

        self.__ensure_is_alive("Unit can't attack as it is dead")

        enemy.take_damage(self._damage)
        enemy.counter_attack(self)

    def counter_attack(self, enemy):
        """
        Making physical damage to an enemy with half damage power.

        :param enemy: Enemy need to be attacked
        :type enemy: Unit
        :raise UnitIsDead: In case Unit is dead

        :return: Nothing
        :rtype: None
        """

        self.__ensure_is_alive("Unit can't counter attack as it is dead")
        enemy.take_damage(self._damage / 2)

    @property
    def damage(self):
        return self._damage

    @property
    def hp(self):
        return self._health_points

    @property
    def hp_limit(self):
        return self._health_points_limit

    @property
    def name(self):
        return self._name
