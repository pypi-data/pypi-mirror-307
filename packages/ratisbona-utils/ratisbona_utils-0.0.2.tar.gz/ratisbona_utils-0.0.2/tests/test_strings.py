import unittest

from ratisbona_utils.strings import (
    snake_to_words, words_to_camel, camel_to_words, pascal_to_words
)


class MyTestCase(unittest.TestCase):

    def test_snake_to_words_must_yield_words(self):
        words = snake_to_words('this_is_a_test')
        self.assertEqual(words, ['this', 'is', 'a', 'test'])

    def test_words_to_camel_must_yield_camel_casing(self):
        result = words_to_camel(['this', 'is', 'a', 'test'])
        self.assertEqual('thisIsATest', result)

    def test_camel_to_words_must_yield_words_in_lowercase(self):
        result = camel_to_words('entityFactoryProviderInterface')
        self.assertEqual(['entity','factory', 'provider', 'interface'], result)

    def test_camel_to_words_must_yield_word_if_only_one_word_given(self):
        result = camel_to_words('entity')
        self.assertEqual(['entity'], result)

    def test_camel_to_words_must_complain_if_not_camel_given(self):
        with self.assertRaises(ValueError) as ve:
            camel_to_words('EntityProvider')
        self.assertTrue('camel' in str(ve.exception))
        self.assertTrue('not' in str(ve.exception))

    def test_pascal_to_words_must_yield_words_in_lowercase(self):
        result = pascal_to_words('EntityFactoryProviderInterface')
        self.assertEqual(['entity','factory', 'provider', 'interface'], result)

    def test_pascal_to_words_must_yield_word_if_only_one_word_given(self):
        result = pascal_to_words('Entity')
        self.assertEqual(['entity'], result)

    def test_camel_to_words_must_complain_if_not_pascal_given(self):
        with self.assertRaises(ValueError) as ve:
            camel_to_words('EntityProvider')
        self.assertTrue('camel' in str(ve.exception))
        self.assertTrue('not' in str(ve.exception))

    def test_pascal_to_words_must_complain_if_not_pascal_given(self):
        with self.assertRaises(ValueError) as ve:
            pascal_to_words('entityProvider')
        self.assertTrue('pascal' in str(ve.exception))
        self.assertTrue('not' in str(ve.exception))


if __name__ == '__main__':
    unittest.main()
