from __future__ import annotations

from asyncio import Event, create_task, get_running_loop, sleep, wait_for
from types import BuiltinFunctionType, NoneType
from typing import TYPE_CHECKING
from unittest import IsolatedAsyncioTestCase as AsyncioTestCase
from unittest.mock import AsyncMock, MagicMock, sentinel

from jsonrpc.utilities import CancellableGather, ensure_async, run_in_background

if TYPE_CHECKING:
    from typing import Any, NoReturn


class TestCancellableGather(AsyncioTestCase):
    async def test_awaited_once(self) -> None:
        mocks: set[AsyncMock] = {AsyncMock(return_value=i) for i in ("a", "b", "c")}

        async def inner(mock: AsyncMock) -> Any:
            return await mock()

        results: tuple[str, ...] = await CancellableGather.map(inner, mocks)
        self.assertCountEqual(results, ("a", "b", "c"))

        for mock in mocks:
            with self.subTest(mock=mock):
                mock.assert_awaited_once()

    async def test_preserved_order(self) -> None:
        results: tuple[str, ...] = await CancellableGather(
            (
                sleep(0.004, "a"),  # <-- accepted latest but should be first in results
                sleep(0.002, "b"),  # <-- accepted second and should be second in results
                sleep(0.001, "c"),  # <-- accepted first but should be third in results
                sleep(0.003, "d"),  # <-- accepted third but should be latest in results
            )
        )
        self.assertTupleEqual(results, ("a", "b", "c", "d"))

    async def test_exception(self) -> None:
        first_exception_mock: AsyncMock = AsyncMock(side_effect=Exception("first exception"))
        second_exception_mock: AsyncMock = AsyncMock(side_effect=Exception("second exception"))

        async def inner(mock: AsyncMock) -> Any:
            return await mock()

        with self.assertRaises(Exception) as context:
            await CancellableGather.map(inner, (first_exception_mock, second_exception_mock))

        self.assertRegex(str(context.exception), r"(?:first|second) exception")
        first_exception_mock.assert_awaited_once()
        second_exception_mock.assert_awaited_once()

    async def test_timeout_error(self) -> None:
        hello_task, world_task = (
            create_task(sleep(3600.0, "hello")),
            create_task(sleep(3600.0, "world")),
        )
        with self.assertRaises(TimeoutError):
            await CancellableGather(
                [
                    wait_for(hello_task, timeout=0.001),
                    wait_for(world_task, timeout=0.002),
                ]
            )
        self.assertTrue(hello_task.cancelled())
        self.assertTrue(world_task.cancelled())

    async def test_exception_group(self) -> None:
        async def inner() -> NoReturn:
            raise ExceptionGroup(
                "one",
                (
                    Exception("for testing purposes"),  # <-- this should be raised first
                    ExceptionGroup(
                        "two",
                        (
                            Exception("2"),
                            Exception("3"),
                        ),
                    ),
                    ExceptionGroup(
                        "three",
                        (
                            Exception("4"),
                            Exception("5"),
                        ),
                    ),
                ),
            )

        with self.assertRaises(Exception) as context:
            await CancellableGather([inner()])

        self.assertEqual(str(context.exception), "for testing purposes")


class TestAsyncioUtilities(AsyncioTestCase):
    async def test_ensure_async(self) -> None:
        for mock in (
            MagicMock(return_value=sentinel.sync_def),
            AsyncMock(return_value=sentinel.async_def),
        ):
            with self.subTest(mock=mock):
                result: Any = await ensure_async(mock, 1, 2, 3, key="value")
                self.assertIs(result, mock.return_value)
                mock.assert_called_once_with(1, 2, 3, key="value")

    def test_run_in_background_exception(self) -> None:
        for obj, objtype in (
            (None, NoneType),
            (print, BuiltinFunctionType),
        ):
            with self.subTest(objtype=objtype):
                with self.assertRaises(TypeError) as context:
                    run_in_background(obj)

                self.assertEqual(str(context.exception), f"a coroutine was expected, got {objtype.__name__!r}")

    async def test_run_in_background(self) -> None:
        loop, mock, event = get_running_loop(), AsyncMock(), Event()

        async def background_task() -> None:
            try:
                await mock()
            finally:
                loop.call_soon(event.set)

        run_in_background(background_task())

        await event.wait()
        mock.assert_awaited_once()
