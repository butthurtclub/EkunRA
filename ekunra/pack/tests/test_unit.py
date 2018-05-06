import unittest

from pack.unit.unit import Unit, UnitIsDead


class TestUnit(unittest.TestCase):

    unit = Unit('Zulu', hp=120, dmg=30)

    def test_init(self):
        self.assertEqual(self.unit.hp, 120)
        self.assertEqual(self.unit.hp_limit, 120)
        self.assertEqual(self.unit.damage, 30)
        self.assertEqual(self.unit.name, 'Zulu')

        with self.assertRaises(TypeError):
            _ = Unit(100, 120, 30)
        with self.assertRaises(TypeError):
            _ = Unit('Xuli', '120', 30)

    def test_unit_validators(self):
        with self.assertRaises(TypeError):
            self.unit._validate_numeric(Unit('hopa'))
        with self.assertRaises(TypeError):
            self.unit._validate_numeric('100500')

        with self.assertRaises(TypeError):
            self.unit._validate_string(10)
        with self.assertRaises(TypeError):
            self.unit._validate_string(Unit('opa'))
        with self.assertRaises(TypeError):
            self.unit._validate_string(10.004)

    def test_representation(self):
        self.assertEqual(str(self.unit), 'Zulu [hp:120/120, damage:30]')
        self.assertEqual(repr(self.unit),
                         '<Unit [name:Zulu, hp:120/120, damage:30]>')

    def test_ensure_is_alive(self):
        u = Unit('Kolya')
        u._health_points = 0

        with self.assertRaises(UnitIsDead):
            u._Unit__ensure_is_alive('test')

    def test_add_health_points(self):
        u = Unit('Drozd', hp=100, dmg=30)
        u.add_health_points(100)

        self.assertEqual(u.hp, 100)

        u._health_points = 50
        u.add_health_points(50)

        self.assertEqual(u.hp, 100)
        with self.assertRaises(TypeError):
            u.add_health_points('mnogo')

        u._health_points = 0

        with self.assertRaises(UnitIsDead):
            u.add_health_points(100)

    def test_take_damage(self):
        u = Unit('Drozd', hp=100, dmg=30)
        u.take_damage(50)

        self.assertEqual(u.hp, 50)

        with self.assertRaises(TypeError):
            u.take_damage('oshenmnogo')
        with self.assertRaises(TypeError):
            u.take_damage(u)

        u.take_damage(70)

        self.assertEqual(u.hp, 0)

    def test_counter_attack(self):
        u = Unit('Drozd', hp=100, dmg=30)
        v = Unit('Grach', hp=100, dmg=30)
        u.counter_attack(v)

        self.assertEqual(u.hp, 100)
        self.assertEqual(v.hp, 85)

        u._health_points = 0

        with self.assertRaises(UnitIsDead):
            u.counter_attack(v)
        self.assertEqual(u.hp, 0)
        self.assertEqual(v.hp, 85)

    def test_attack(self):
        u = Unit('Drozd', hp=100, dmg=30)
        v = Unit('Grach', hp=100, dmg=30)
        u.attack(v)

        self.assertEqual(u.hp, 85)
        self.assertEqual(v.hp, 70)

        u.attack(v)

        self.assertEqual(u.hp, 70)
        self.assertEqual(v.hp, 40)

        u._health_points = 0

        with self.assertRaises(UnitIsDead):
            u.attack(v)
        self.assertEqual(u.hp, 0)
        self.assertEqual(v.hp, 40)
