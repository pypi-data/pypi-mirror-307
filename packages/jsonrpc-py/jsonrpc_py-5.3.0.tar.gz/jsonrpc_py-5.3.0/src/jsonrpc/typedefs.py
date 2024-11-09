from __future__ import annotations

from typing import TYPE_CHECKING, Any, Protocol, TypedDict

if TYPE_CHECKING:
    from collections.abc import Iterable, MutableMapping
    from typing import Literal, NotRequired

    from .openrpc import ContentDescriptor, Error, ExamplePairing, ExternalDocumentation, Link, ParamStructure, Server, Tag

__all__: tuple[str, ...] = (
    "ASGIReceiveCallable",
    "ASGIReceiveEvent",
    "ASGISendCallable",
    "ASGISendEvent",
    "ASGIVersions",
    "FunctionSchema",
    "HTTPConnectionScope",
    "HTTPDisconnectEvent",
    "HTTPRequestEvent",
    "HTTPResponseBodyEvent",
    "HTTPResponseStartEvent",
    "LifespanScope",
    "LifespanShutdownCompleteEvent",
    "LifespanShutdownEvent",
    "LifespanShutdownFailedEvent",
    "LifespanStartupCompleteEvent",
    "LifespanStartupEvent",
    "LifespanStartupFailedEvent",
    "Scope",
)


class ASGIVersions(TypedDict):
    spec_version: str
    version: str


class HTTPConnectionScope(TypedDict):
    type: Literal["http"]
    asgi: ASGIVersions
    http_version: str
    method: str
    scheme: NotRequired[str]
    path: str
    raw_path: NotRequired[bytes | None]
    query_string: bytes
    root_path: NotRequired[str]
    headers: Iterable[tuple[bytes, bytes]]
    client: NotRequired[tuple[str, int] | None]
    server: NotRequired[tuple[str, int | None] | None]
    state: NotRequired[MutableMapping[str, Any]]
    extensions: NotRequired[MutableMapping[str, MutableMapping[Any, Any]] | None]


class HTTPRequestEvent(TypedDict):
    type: Literal["http.request"]
    body: NotRequired[bytes]
    more_body: NotRequired[bool]


class HTTPResponseStartEvent(TypedDict):
    type: Literal["http.response.start"]
    status: int
    headers: Iterable[tuple[bytes, bytes]]
    trailers: NotRequired[bool]


class HTTPResponseBodyEvent(TypedDict):
    type: Literal["http.response.body"]
    body: NotRequired[bytes]
    more_body: NotRequired[bool]


class HTTPDisconnectEvent(TypedDict):
    type: Literal["http.disconnect"]


class LifespanScope(TypedDict):
    type: Literal["lifespan"]
    asgi: ASGIVersions
    state: NotRequired[MutableMapping[str, Any]]


class LifespanStartupEvent(TypedDict):
    type: Literal["lifespan.startup"]


class LifespanStartupCompleteEvent(TypedDict):
    type: Literal["lifespan.startup.complete"]


class LifespanStartupFailedEvent(TypedDict):
    type: Literal["lifespan.startup.failed"]
    message: NotRequired[str]


class LifespanShutdownEvent(TypedDict):
    type: Literal["lifespan.shutdown"]


class LifespanShutdownCompleteEvent(TypedDict):
    type: Literal["lifespan.shutdown.complete"]


class LifespanShutdownFailedEvent(TypedDict):
    type: Literal["lifespan.shutdown.failed"]
    message: NotRequired[str]


type Scope = HTTPConnectionScope | LifespanScope
type ASGIReceiveEvent = HTTPRequestEvent | HTTPDisconnectEvent | LifespanStartupEvent | LifespanShutdownEvent
type ASGISendEvent = (
    HTTPResponseStartEvent
    | HTTPResponseBodyEvent
    | HTTPDisconnectEvent
    | LifespanStartupCompleteEvent
    | LifespanStartupFailedEvent
    | LifespanShutdownCompleteEvent
    | LifespanShutdownFailedEvent
)


class ASGIReceiveCallable(Protocol):
    async def __call__(self) -> ASGIReceiveEvent: ...


class ASGISendCallable(Protocol):
    async def __call__(self, event: ASGISendEvent, /) -> None: ...


class FunctionSchema(TypedDict, total=False):
    name: str
    tags: list[Tag]
    summary: str
    description: str
    external_docs: ExternalDocumentation
    params: list[ContentDescriptor]
    result: ContentDescriptor
    deprecated: bool
    servers: list[Server]
    errors: list[Error]
    links: list[Link]
    param_structure: ParamStructure
    examples: list[ExamplePairing]
