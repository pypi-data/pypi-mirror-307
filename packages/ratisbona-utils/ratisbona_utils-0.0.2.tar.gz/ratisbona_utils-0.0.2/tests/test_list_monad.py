import unittest

from ratisbona_utils.monads import List


class MyTestCase(unittest.TestCase):

    def test_binding_must_apply_function_to_list_flatmapping_results(self):
        ls = List([1, 2, 3, 4, 5])
        self.assertEqual(ls.bind(lambda x: [x, -x]),
                         List([1, -1, 2, -2, 3, -3, 4, -4, 5, -5]))


if __name__ == '__main__':
    unittest.main()
