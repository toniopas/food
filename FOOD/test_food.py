import unittest
from food import Food


class TestFood(unittest.TestCase):
    """ class test food """

    def test_get_name(self):
        """ test_get_name """
        print('test_get_name')
        food_one = Food()
        food_two = Food()

        food_two.set_name('faiselle')

        self.assertEqual(food_one.get_name(), None)
        self.assertEqual(food_two.get_name(), 'faiselle')

    def test_is_fat(self):
        """ test_is_fat : test 3 different foods """
        print('test_is_fat')

        # Avocat : gras (37g lipides, 360 kcal → ~92% des calories)
        food_avocat = Food()
        food_avocat.set_name('avocat')
        food_avocat.set_calories(360.0)
        food_avocat.set_fat(37.0)
        self.assertTrue(food_avocat.is_fat())

        # Tomate : pas grasse (0.3g lipides, 21 kcal → ~1% des calories)
        food_tomate = Food()
        food_tomate.set_name('tomate')
        food_tomate.set_calories(21.0)
        food_tomate.set_fat(0.3)
        self.assertFalse(food_tomate.is_fat())

        # Amande : grasse (4.5g lipides, 50 kcal → ~81% des calories)
        food_amande = Food()
        food_amande.set_name('amande')
        food_amande.set_calories(50.0)
        food_amande.set_fat(4.5)
        self.assertTrue(food_amande.is_fat())

    def test_get_calories(self):
        """ test_get_calories """
        print('test_get_calories')

        food_one = Food()
        food_two = Food()

        food_two.set_calories(21.0)

        self.assertEqual(food_one.get_calories(), None)
        self.assertEqual(food_two.get_calories(), 21.0)

    def test_get_carbs(self):
        """ test_get_carbs """
        print('test_get_carbs')

        food_one = Food()
        food_two = Food()

        food_two.set_carbs(4.6)

        self.assertEqual(food_one.get_carbs(), None)
        self.assertEqual(food_two.get_carbs(), 4.6)


if __name__ == '__main__':
    unittest.main()
