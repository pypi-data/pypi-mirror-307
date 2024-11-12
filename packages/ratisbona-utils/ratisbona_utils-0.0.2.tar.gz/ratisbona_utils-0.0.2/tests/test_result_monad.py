# Copilot: Create unittest Testclass and main function
import unittest
from unittest import TestCase, main

from ratisbona_utils.monads.monads import ResultMonad


class TestResultMonad(TestCase):

    def test_success_must_not_be_error_and_must_unwrap(self):
        # Given

        # When
        result = ResultMonad.ok("Good value")

        # Then
        self.assertFalse(result.is_error)
        self.assertEqual("Good value", result.unwrap_value())


    def test_success_must_not_allow_unwrap_error(self):
        # When
        result = ResultMonad.ok("Good value")

        # Then
        with self.assertRaises(ValueError) as ve:
            result.unwrap_error()

        self.assertEqual("You must not unwrap the error of a ResultMonad that in fact is a success.", str(ve.exception))


    def test_error_must_be_error_and_unwrap_error(self):
        # Given

        # When
        result = ResultMonad.err("Bad value")

        # Then
        self.assertTrue(result.is_error)
        self.assertEqual("Bad value", result.unwrap_error())


    def test_error_must_not_unwrap_value(self):

        # When
        result = ResultMonad.err("Bad value")

        # Then
        with self.assertRaises(ValueError) as ve:
            result.unwrap_value()

        self.assertEqual("You must not unwrap a ResultMonad with an error status.", str(ve.exception))

    def test_bind_must_not_execute_for_error(self):
        # Given
        def add_one(x):
            raise AssertionError('This code never should run!')

        # When
        result = ResultMonad.err("Bad value").bind(add_one)

        # Then
        self.assertTrue(result.is_error)
        self.assertEqual("Bad value", result.unwrap_error())


    def test_bind_must_execute_for_value(self):
        # Given
        def add_one(x):
            return x + 1

        # When
        result = ResultMonad.ok(42).bind(add_one)

        # Then
        self.assertFalse(result.is_error)
        self.assertEqual(43, result.unwrap_value())


    def test_bind_must_catch_errors_and_record_stacktrace(self):
        # Given
        def add_one(x):
            raise ValueError('This is an error!')

        # When
        result = ResultMonad.ok(42).bind(add_one, monad_add_stacktrace=True)

        # Then
        self.assertTrue(result.is_error)
        error, stacktrace = result.unwrap_error()
        self.assertEqual('This is an error!', error.args[0])
        self.assertTrue('add_one' in stacktrace)

    def test_bind_must_allow_for_additional_arguments(self):
        # Given
        def add(x, y):
            return x + y

        # When
        result = ResultMonad.ok(42).bind(add, 1)

        # Then
        self.assertFalse(result.is_error)
        self.assertEqual(43, result.unwrap_value())


    def test_bind_result_must_accept_result_valued_functions(self):
        # Given
        def add_one(x):
            return ResultMonad.ok(str(x + 1))

        # When
        result = ResultMonad.ok(42).bind_resultmonad(add_one)

        # Then
        self.assertFalse(result.is_error)
        self.assertEqual("43", result.unwrap_value())

    def test_bind_result_must_accept_result_valued_functions(self):
        # Given
        def add_one(x):
            return ResultMonad.err("Praise Discordia!")

        # When
        result = ResultMonad.ok(42).bind_resultmonad(add_one)

        # Then
        self.assertTrue(result.is_error)
        self.assertEqual("Praise Discordia!", result.unwrap_error())

    def test_map_must_be_able_to_turn_failure_into_success(self):

        # Given
        def recover(result):
            self.assertTrue(result.is_error)
            self.assertEqual("Bad value", result.unwrap_error())
            return ResultMonad.ok("All good again, don't worry.")

        # When
        result = ResultMonad.err("Bad value")

        mapped_result = result.map(recover)

        # Then
        self.assertFalse(mapped_result.is_error)
        self.assertEqual("All good again, don't worry.", mapped_result.unwrap_value())

    def test_map_must_be_able_to_fail_a_result(self):

        # Given
        def postcheck(result):
            self.assertFalse(result.is_error)
            self.assertEqual("Good value", result.unwrap_value())
            return ResultMonad.err("Oh no, it's bad again!")

        # When
        result = ResultMonad.ok("Good value")

        mapped_result = result.map(postcheck)

        # Then
        self.assertTrue(mapped_result.is_error)
        self.assertEqual("Oh no, it's bad again!", mapped_result.unwrap_error())

if __name__ == '__main__':
    main()
