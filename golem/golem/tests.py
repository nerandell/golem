import unittest

from .golem import Golem

class GolemTest(unittest.TestCase):
    def test_item_generator(self):
        name = 'TestItem'
        fields = [('username', str), ('email', str)]
        TestItem = Golem.generate_class(name, fields)
        self.assertEquals(TestItem._fields, [('username', str), ('email', str), ('created', int), ('updated', int)])

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(GolemTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
