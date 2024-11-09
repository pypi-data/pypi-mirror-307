from __future__ import annotations

from collections.abc import Collection
from dataclasses import is_dataclass
from functools import partial
from typing import TYPE_CHECKING
from unittest import TestCase
from unittest.mock import MagicMock
from uuid import uuid4

from jsonrpc import BatchResponse, Error, ErrorEnum, Response
from jsonrpc.openrpc import Undefined

if TYPE_CHECKING:
    from uuid import UUID


class TestResponse(TestCase):
    @property
    def random_id(self) -> str:
        uuid: UUID = uuid4()
        return str(uuid)

    def test_inheritance(self) -> None:
        response: Response = Response(body=[1, 2, 3], response_id=self.random_id)
        self.assertTrue(is_dataclass(response))

    def test_validate_body_and_error(self) -> None:
        for invalid_response in (
            partial(Response),
            partial(Response, body=Undefined, error=Undefined),
            partial(Response, body=[1, 2, 3], error=Error(code=ErrorEnum.INTERNAL_ERROR, message="for testing purposes")),
        ):
            with self.subTest(response=invalid_response):
                with self.assertRaises(TypeError) as context:
                    invalid_response(response_id=self.random_id)

                self.assertEqual(str(context.exception), "Either 'body' or 'error' attribute must be set")

    def test_validate_response_id(self) -> None:
        for response_id in ("1", 2, Undefined, None):
            with self.subTest(response_id=response_id):
                try:
                    Response(body="for testing purposes", response_id=response_id)
                except TypeError as exception:
                    self.fail(exception)

        with self.assertRaises(TypeError) as context:
            Response(body="for testing purposes", response_id=[1, 2, 3])

        self.assertIn("must be an optional string or number", str(context.exception))

    def test_json(self) -> None:
        for actual, expected in (
            (
                Response(body="for testing purposes", response_id=(response_id := self.random_id)).json,
                {"jsonrpc": "2.0", "result": "for testing purposes", "id": response_id},
            ),
            (
                Response(error=Error(code=ErrorEnum.INVALID_PARAMETERS, message="Invalid Parameters", data=[1, 2, 3])).json,
                {"jsonrpc": "2.0", "error": {"code": ErrorEnum.INVALID_PARAMETERS, "message": "Invalid Parameters", "data": [1, 2, 3]}},
            ),
        ):
            with self.subTest(actual=actual, expected=expected):
                self.assertDictEqual(actual, expected)


class TestBatchResponse(TestCase):
    @property
    def random_id(self) -> int:
        uuid: UUID = uuid4()
        return int(uuid)

    def test_inheritance(self) -> None:
        mock: MagicMock = MagicMock()
        batch_response: BatchResponse = BatchResponse([mock])

        self.assertTrue(is_dataclass(batch_response))
        self.assertIsInstance(batch_response, Collection)
        self.assertIn(mock, batch_response)
        self.assertEqual(len(batch_response), 1)

        for response in batch_response:
            with self.subTest(response=response):
                self.assertIs(response, mock)

    def test_json(self) -> None:
        batch_response: BatchResponse = BatchResponse(
            [
                Response(body="for testing purposes"),
                Response(
                    error=Error(code=ErrorEnum.INTERNAL_ERROR, message="Internal Error", data=[1, 2, 3]),
                    response_id=(response_id := self.random_id),
                ),
            ]
        )
        self.assertCountEqual(
            batch_response.json,
            [
                {"jsonrpc": "2.0", "result": "for testing purposes"},
                {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": ErrorEnum.INTERNAL_ERROR,
                        "message": "Internal Error",
                        "data": [1, 2, 3],
                    },
                    "id": response_id,
                },
            ],
        )
