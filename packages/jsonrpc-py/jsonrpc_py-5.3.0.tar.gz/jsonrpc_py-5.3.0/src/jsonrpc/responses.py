from __future__ import annotations

from collections.abc import Collection
from dataclasses import InitVar, dataclass, field
from numbers import Number
from types import NoneType
from typing import TYPE_CHECKING

from .openrpc import Undefined, UndefinedType

if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator
    from typing import Any

    from .errors import Error

__all__: tuple[str, ...] = ("BatchResponse", "Response")


@dataclass(kw_only=True, slots=True)
class Response:
    """
    Base JSON-RPC response object.
    """

    #: An any type of object that contains a result of successful processing
    #: the :class:`~jsonrpc.Request` object. This attribute must not be set if there an error has occurred.
    body: Any = Undefined
    #: The :class:`~jsonrpc.Error` object representing an erroneous processing
    #: the :class:`~jsonrpc.Request` object. This attribute must not be set if no one error has occurred.
    error: Error | UndefinedType = Undefined
    #: The same attribute as :attr:`~jsonrpc.Request.request_id`
    #: except that its value might be equal to :py:data:`None` in erroneous responses.
    response_id: str | float | None | UndefinedType = Undefined

    def __post_init__(self) -> None:
        if isinstance(self.body, UndefinedType) == isinstance(self.error, UndefinedType):
            raise TypeError("Either 'body' or 'error' attribute must be set")
        if not isinstance(self.response_id, str | Number | UndefinedType | NoneType):
            raise TypeError(f"Response id must be an optional string or number, not a {type(self.response_id).__name__!r}")

    @property
    def json(self) -> dict[str, Any]:
        """
        Returns the :py:class:`dict` object needed for the serialization.

        Example successful response::

            >>> response: Response = Response(body="foobar", response_id=65535)
            >>> response.json
            {"jsonrpc": "2.0", "result": "foobar", "id": 65535}

        Example erroneous response::

            >>> error: Error = Error(code=ErrorEnum.INTERNAL_ERROR, message="Unexpected error")
            >>> response: Response = Response(error=error, response_id="6ba7b810")
            >>> response.json
            {"jsonrpc": "2.0", "error": {"code": -32603, "message": "Unexpected error"}, "id": "6ba7b810"}
        """
        obj: dict[str, Any] = {"jsonrpc": "2.0"}

        if isinstance(error := self.error, UndefinedType):
            obj |= {"result": self.body}
        else:
            obj |= {"error": error.json}
        if not isinstance(response_id := self.response_id, UndefinedType):
            obj |= {"id": response_id}

        return obj


@dataclass(slots=True)
class BatchResponse(Collection[Response]):
    """
    A :py:class:`~collections.abc.Collection` of the :class:`~jsonrpc.Response` objects.
    """

    iterable: InitVar[Iterable[Response]] = ()
    data: list[Response] = field(default_factory=list, init=False)

    def __post_init__(self, iterable: Iterable[Response]) -> None:
        self.data.extend(iterable)

    def __contains__(self, item: Any) -> bool:
        return item in self.data

    def __iter__(self) -> Iterator[Response]:
        return iter(self.data)

    def __len__(self) -> int:
        return len(self.data)

    @property
    def json(self) -> list[dict[str, Any]]:
        """
        Returns the :py:class:`list` of :py:class:`dict` objects needed for the serialization.

        Example output::

            >>> response: BatchResponse = BatchResponse([
            ...     Response(body="foobar", response_id=1024),
            ...     Response(
            ...         error=Error(code=ErrorEnum.INTERNAL_ERROR, message="Unexpected error"),
            ...         response_id="6ba7b810"
            ...     )
            ... ])
            >>> response.json
            [
                {"jsonrpc": "2.0", "result": "foobar", "id": 1024},
                {"jsonrpc": "2.0", "error": {"code": -32603, "message": "Unexpected error"}, "id": "6ba7b810"}
            ]
        """
        return [response.json for response in self.data]
