from __future__ import annotations

from inspect import Signature
from types import BuiltinFunctionType, NoneType
from typing import TYPE_CHECKING
from unittest import IsolatedAsyncioTestCase as AsyncioTestCase, TestCase

from jsonrpc import AsyncDispatcher, Error, ErrorEnum, Function

if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import Any, NoReturn


class TestAsyncDispatcher(AsyncioTestCase):
    def setUp(self) -> None:
        self.dispatcher: AsyncDispatcher = AsyncDispatcher()

    async def test_dispatch_non_existent_function(self) -> None:
        with self.assertRaises(Error) as context:
            await self.dispatcher.dispatch("non_existent_function")

        self.assertEqual(context.exception.code, ErrorEnum.METHOD_NOT_FOUND)

    async def test_dispatch_non_existent_parameter(self) -> None:
        test_lambda: Callable[..., Any] = lambda obj: obj  # noqa: E731
        self.dispatcher.register(test_lambda, name="test_lambda")

        with self.assertRaises(Error) as context:
            await self.dispatcher.dispatch("test_lambda", non_existent_parameter="non_existent_parameter")

        self.assertEqual(context.exception.code, ErrorEnum.INVALID_PARAMETERS)

    async def test_dispatch_division(self) -> None:
        @self.dispatcher.register(name="my_div")
        def _(a: float, b: float) -> float:
            return a / b

        with self.assertRaises(Error) as context:
            await self.dispatcher.dispatch("my_div", 10, 0)

        self.assertEqual(context.exception.code, ErrorEnum.INTERNAL_ERROR)
        self.assertIn("division by zero", context.exception.message)

    async def test_dispatch_raising(self) -> None:
        @self.dispatcher.register
        def raising(*, code: int, message: str) -> NoReturn:
            raise Error(code=code, message=message)

        with self.assertRaises(Error) as context:
            await self.dispatcher.dispatch("raising", code=ErrorEnum.INTERNAL_ERROR, message="for testing purposes")

        self.assertEqual(context.exception.code, ErrorEnum.INTERNAL_ERROR)
        self.assertEqual(context.exception.message, "for testing purposes")


class TestFunction(TestCase):
    def test_from_callable_exception(self) -> None:
        for obj, objtype in (
            (None, NoneType),
            (print, BuiltinFunctionType),
        ):
            with self.subTest(objtype=objtype):
                with self.assertRaises(TypeError) as context:
                    Function.from_callable(obj)

                self.assertEqual(str(context.exception), f"a user-defined function was expected, got {objtype.__name__!r}")

    def test_from_callable_name(self) -> None:
        def first() -> None:
            raise NotImplementedError

        first_function: Function[..., Any] = Function.from_callable(first)
        self.assertEqual(first_function.schema.name, "first")

        second_function: Function[..., Any] = Function.from_callable(first, name="second")
        self.assertEqual(second_function.schema.name, "second")

    def test_from_callable(self) -> None:
        def my_sum(a: str, b: str) -> str:
            return a + b

        function: Function[[str, str], str] = Function.from_callable(my_sum)
        self.assertEqual(function("a", "b"), "ab")

        signature: Signature = Signature.from_callable(my_sum)
        self.assertEqual(function.signature, signature)
