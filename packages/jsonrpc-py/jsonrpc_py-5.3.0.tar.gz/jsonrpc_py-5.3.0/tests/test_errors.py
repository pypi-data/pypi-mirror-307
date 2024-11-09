from __future__ import annotations

from dataclasses import is_dataclass
from unittest import TestCase

from jsonrpc import Error, ErrorEnum


class TestError(TestCase):
    def test_inheritance(self) -> None:
        error: Error = Error(code=ErrorEnum.INTERNAL_ERROR, message="Internal Error")
        self.assertTrue(is_dataclass(error))
        self.assertIsInstance(error, Exception)

    def test_str(self) -> None:
        error: Error = Error(code=ErrorEnum.METHOD_NOT_FOUND, message="Method Not Found")
        self.assertEqual(str(error), f"{error.message!s}\u0020\u0028{error.code:d}\u0029")

    def test_json(self) -> None:
        for actual, expected in (
            (
                Error(code=ErrorEnum.INVALID_PARAMETERS, message="Invalid Parameters").json,
                {"code": ErrorEnum.INVALID_PARAMETERS, "message": "Invalid Parameters"},
            ),
            (
                Error(code=ErrorEnum.INTERNAL_ERROR, message="Internal Error", data={"additional": "information"}).json,
                {"code": ErrorEnum.INTERNAL_ERROR, "message": "Internal Error", "data": {"additional": "information"}},
            ),
        ):
            with self.subTest(actual=actual, expected=expected):
                self.assertDictEqual(actual, expected)
