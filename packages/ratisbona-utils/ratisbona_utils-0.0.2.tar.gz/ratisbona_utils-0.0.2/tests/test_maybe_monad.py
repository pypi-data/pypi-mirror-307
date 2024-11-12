import unittest

from ratisbona_utils.monads import Just, Nothing, Maybe


def add_one(x):
    return x + 1


def double(x):
    return x * 2

class MyTestCase(unittest.TestCase):

    def test_maybe_int_must_be_just_int(self):
        just_42 = Just(42)
        self.assertEqual(just_42.unwrap(), 42)
        self.assertEqual(str(just_42), 'Just 42')

    def test_nothing_must_be_nothing(self):
        nothing = Nothing
        self.assertEqual(nothing.unwrap(), None)
        self.assertEqual(str(nothing), 'Nothing')

    def test_nothing_must_equal_nothing(self):
        self.assertEqual(Nothing, Nothing)

    def just_value_must_equal_just_value(self):
        self.assertEqual(Just(42), Just(42))
    def test_nothing_must_equal_Maybe_None(self):
        self.assertEqual(Nothing, Maybe(None))

    def test_just_none_must_not_be_allowed(self):
        with self.assertRaises(ValueError) as ve:
            Just(None)
        self.assertTrue('None' in str(ve.exception))

    def test_just_must_equal_maybe_value(self):
        self.assertEqual(Just(42), Maybe(42))

    def test_maybe_or_must_return_just_value(self):
        just_42 = Just(42)
        self.assertEqual(just_42 | Just(0), Just(42))
        self.assertEqual(just_42 | Nothing, Just(42))
        nothing = Nothing
        self.assertEqual(nothing | Just(42), Just(42))
        self.assertEqual(nothing | Nothing, Nothing)

    def test_or_else_must_return_default_value(self):
        nothing = Nothing
        self.assertEqual(nothing.or_else(42).unwrap(), 42)
        just_42 = Just(42)
        self.assertEqual(just_42.or_else(0).unwrap(), 42)

    def test_bind_must_apply_function_to_just_value(self):
        just_42 = Just(42)
        self.assertEqual(just_42.bind(add_one), Just(43))
        self.assertEqual(just_42.bind(double), Just(84))

    def test_bind_must_return_nothing_for_nothing(self):
        nothing = Nothing
        self.assertEqual(nothing.bind(add_one), Nothing)
        self.assertEqual(nothing.bind(double), Nothing)

    def test_bind_multiarg_function_just_bind_just_bin_results_in_just_value(self):

        just_42 = Just(42)
        just_48 = Just(48)

        def add(a, b):
            return a + b

        retval = just_42.bind(lambda a: just_48.bind(lambda b: add(a, b)))

        self.assertEqual(Just(90), retval)


    def test_bind_multiarg_function_just_bind_nothing_results_in_nothing(self):

        just_42 = Just(42)
        nothing = Nothing

        def add(a, b):
            return a + b

        retval = just_42.bind(lambda a: nothing.bind(lambda b: add(a, b)))

        self.assertEqual(Nothing, retval)



if __name__ == '__main__':
    unittest.main()
