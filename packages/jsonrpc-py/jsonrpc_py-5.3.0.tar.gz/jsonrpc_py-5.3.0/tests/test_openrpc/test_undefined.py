from __future__ import annotations

from unittest import TestCase

from jsonrpc.openrpc import Undefined


class TestUndefined(TestCase):
    def test_hash(self) -> None:
        self.assertEqual(hash(Undefined), 0xDEADBEEF)

    def test_bool(self) -> None:
        self.assertFalse(Undefined)
