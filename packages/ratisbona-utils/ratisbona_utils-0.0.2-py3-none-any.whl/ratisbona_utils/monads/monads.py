"""
    This module contains the implementation of the Maybe, Failure and List monads in pure Python.
"""

from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Callable
from typing import Dict, TypeVar, Generic

import traceback

T = TypeVar("T")
VT = TypeVar("VT")


class Maybe(Generic[T]):
    """
    The Maybe monad is a way to handle optional values in a functional way.
    """

    def __init__(self, value: T | Maybe[T]):
        """
        Constructor for the Monad. Maybe you want to use the convenience functions Just and Nothing instead.
        """
        if isinstance(value, Maybe):
            self._value = value.unwrap()
        else:
            self._value = value

    def bind(self, func: Callable[[T], VT] | Maybe[Callable[[T], VT]]) -> Maybe[VT]:
        """
        Bind the value of the monad to a function. What if I have a function that takes two arguments?
        Well use currying like so:
        ```
        def add(a, b):
            return a + b

        maybe_a = Just(1)
        maybe_b = Just(2)

        maybe_a_adder = lambda a: b.bind(lambda b: add(a, b))
        maybe_result = maybe_b.bind(maybe_a_adder)

        ```

        """
        if self._value is None:
            return Maybe(None)

        if isinstance(func, Maybe):
            if not func:
                return Maybe(None)
            return Maybe(func.unwrap()(self._value))
        else:
            return Maybe(func(self._value))

    def or_else(self, default: T) -> Maybe[T]:
        """
        Return the value of the monad or a default value if the monad is Nothing.

        Args:
            default: The default value to return if the monad is Nothing.

        Returns:
            Maybe: The value of the monad or the default
        """
        if self._value is None:
            return Maybe(default)
        else:
            return self

    def unwrap(self) -> T:
        """
        Get the value of the monad. If the monad is Nothing, None will be returned.
        """
        return self._value

    def __or__(self, other) -> Maybe[T]:
        """
        Return the value of the monad or the value of another monad if the monad is Nothing.

        Args:
            other: The other monad to return if the monad is Nothing.

        Returns:
            Maybe: The value of the monad or the value of another monad.
        """
        return Maybe(self._value or other._value)

    def __str__(self) -> str:
        """
        Return a string representation of the monad: "Just <value>" or "Nothing"

        Returns:
            str: The string representation of the monad.
        """
        if self._value is None:
            return "Nothing"
        else:
            return "Just {}".format(self._value)

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other) -> bool:
        """
        Compare the value of the monad with the value of another monad: Two monads are equal if their values are
        equal. Nothing is not equal to Maybe(None). Nothing is equal to itself.

        """
        if isinstance(other, Maybe):
            return self._value == other._value
        else:
            return False

    def __ne__(self, other) -> bool:
        return not (self == other)

    def __bool__(self):
        """
        A Monad is true if it is Just and false if it is Nothing.

        Retruns:
            bool: True if the monad is Just, False if the monad is Nothing
        """
        return self._value is not None


def Just(value: T) -> Maybe[T]:
    """
    Constructor for Just Values
        Args: value: any
        Returns: Maybe
    """
    if not value:
        raise ValueError(
            "None is not what I would call Just value. I'm assuming you f-ed up, but if you really want to use None, use Nothing() instead."
        )
    return Maybe(value)


Nothing = Maybe(None)


ST = TypeVar("ST")  # Success type
ET = TypeVar("ET")  # Error Type
AET = TypeVar("AET")  # Alternate Error Type
AST = TypeVar("AST")  # Alternate Success Type

GENERIC_ERROR = Exception | tuple[Exception, str] | None

@dataclass(frozen=True)
class ResultMonad(Generic[ST, ET]):
    """
    The FailureMonad is a way to handle errors in a functional way. It is similar to the Maybe monad, but it
    contains an error status in case of an error.

    Fields:
        value: ST | ET: The value of the monad. If the monad is an error, the error value will be stored here.
        is_error: bool: True if the monad is an error, False if it is a success.
    """

    value: ST | ET
    is_error: bool

    @staticmethod
    def ok(value: ST) -> ResultMonad[ST, None]:
        return ResultMonad(value, False)

    @staticmethod
    def err(value: ET) -> ResultMonad[None, ET]:
        return ResultMonad(value, True)

    @staticmethod
    def call_with_monadic_error_handling(
        f: Callable[[...], ST], *args, monad_add_stacktrace=True, **kwargs
    ) -> ResultMonad[ST, GENERIC_ERROR]:
        """
        Calls a function with monadic error handling. If the function raises an exception, the exception will
        be caught and returned as an error status in the ResultMonad.

        Args:
            f: The function to call. Will be passed the other arguments.
            args: The other arguments to pass to the function
            monad_add_stacktrace: If True, the stacktrace will be added to the error status. KW-only. Default: True
            kwargs: The other keyword arguments to pass to the function
        """
        try:
            return ResultMonad.ok(f(*args, **kwargs))
        except Exception as any_exception:
            err_val = any_exception, (
                traceback.format_exc() if monad_add_stacktrace else any_exception
            )
            return ResultMonad.err(err_val)

    def bind_resultmonad(
        self, f: Callable[[ST, ...], ResultMonad[AST, AET]], *args, **kwargs
    ) -> ResultMonad[AST, ET | AET]:
        """
        Binds a function to the result monad that returns a result monad. Intended
        for functions that might fail and already do monadic error handling.

        Args:
            f: The function to bind to the result monad. Result-monad-returning.
               Will be passed the value of the result monad as the first argument.
            args: The other arguments to pass to the function
            kwargs: The other keyword arguments to pass to the function

        Returns:
            ResultMonad: The result of the function or a FailureMonad with an error status.
        """
        if self.is_error:
            return ResultMonad.err(self.value)

        return f(self.value, *args, **kwargs)

    def bind(
        self, f: Callable[[ST, ...], AST], *args, monad_add_stacktrace=False, **kwargs
    ) -> ResultMonad[AST, ET | GENERIC_ERROR]:
        """
        Binds a function to the ResultMonad. Function can throw exceptions which will
        be caught and returned as an error status in the ResultMonad, for convenience.

        Args:
            f: The function to bind to the result monad. Will be passed the
            value of the result monad as the first argument.
            args: The other arguments to pass to the function
            monad_add_stacktrace: If True, the stacktrace will be added to the error status.
            kwargs: The other keyword arguments to pass to the function
        """

        if self.is_error:
            return ResultMonad.err(self.value)

        return ResultMonad.call_with_monadic_error_handling(
            f, self.value, *args, monad_add_stacktrace=monad_add_stacktrace, **kwargs
        )

    def map(
        self,
        f: Callable[[ResultMonad[ST, ET], ...], ResultMonad[AST, AET]],
        *args: object,
        **kwargs: object,
    ) -> ResultMonad[AST, AET]:
        """
        Maps a the result monad by a function that returns a result monad. Can be used
        to recover from errors or to do checks and issue an error from a former success
        state.

        Args:
            f: The function to map to the result monad. Result-monad-returning.
               Will be passed the result monad as the first argument.
               Not expected to throw any exceptions.
            args: The other arguments to pass to the function
            kwargs: The other keyword arguments to pass to the function

        Returns:
            ResultMonad: The result of the function or a FailureMonad with an error status.
        """
        return f(self, *args, **kwargs)

    def __or__(self, other: ResultMonad[AST, AET]) -> ResultMonad[ST | AST, ET | AET]:
        """
        Return the value of the monad or the value of another monad if the monad is error.
        """
        if self.is_error:
            return other
        return self

    def unwrap_value(self) -> ST:
        """
        Get the value of the monad. If the monad is Nothing, None will be returned.

        Returns:
            The value of the monad.

        Raises:
            ValueError: If the monad is an error.
        """
        if self.is_error:
            raise ValueError("You must not unwrap a ResultMonad with an error status.")
        return self.value

    def unwrap_error(self) -> ET:
        """
        Get the error value of the monad.

        Returns:
            The error value of the monad.

        Raises:
            ValueError: If the monad is not an error.
        """
        if not self.is_error:
            raise ValueError(
                "You must not unwrap the error of a ResultMonad that in fact is a success."
            )
        return self.value

# List Element Type
LT = TypeVar("LT")

def concat(list_of_lists: ListMonad[ListMonad[LT]]) -> ListMonad[LT]:
    """
    Concatenate a list of ListMonads into a single ListMonad.
    """
    values = []
    for alist in list_of_lists.unwrap():
        if isinstance(alist, ListMonad):
           values.append(alist.unwrap())
        elif isinstance(alist, list):
            values.append(alist)
        else:
            raise ValueError(f"Expected ListMonad or list, got {type(alist)}")
    return ListMonad(values)

@dataclass
class ListMonad(Generic[LT]):
    value: list[LT]

    def __init__(self, value: LT):
        if isinstance(value, list):
            self.value = value
        elif isinstance(value, tuple):
            self.value = list(*value)
        elif isinstance(value, ListMonad):
            self.value = value.unwrap()
        else:
            self.value = list(*value)

    def __repr__(self):
        return f"ListMonad({self.value})"

    def unwrap(self) -> list[LT]:
        return self.value

    def bind(self, func):
        return ListMonad([func(x) for x in self.value])

    def __eq__(self, other):
        return self.value == other.value

    @staticmethod
    def wrap(*value):
        return ListMonad(value)



