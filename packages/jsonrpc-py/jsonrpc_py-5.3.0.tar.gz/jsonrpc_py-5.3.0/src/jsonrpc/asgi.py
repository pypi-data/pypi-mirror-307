from __future__ import annotations

import re
from asyncio import CancelledError
from collections.abc import MutableSequence
from dataclasses import dataclass, field
from http import HTTPMethod, HTTPStatus
from io import DEFAULT_BUFFER_SIZE, BytesIO
from typing import TYPE_CHECKING

from .dispatcher import AsyncDispatcher
from .errors import Error
from .lifespan import LifespanEvents, LifespanManager
from .openrpc import Info, OpenRPC
from .requests import BatchRequest, Request
from .responses import BatchResponse, Response
from .serializers import JSONSerializer
from .utilities import Awaitable, CancellableGather, run_in_background

if TYPE_CHECKING:
    from collections.abc import Coroutine
    from typing import Any

    from .openrpc import Components, Contact, ExternalDocumentation, License, Server
    from .typedefs import ASGIReceiveCallable, ASGIReceiveEvent, ASGISendCallable, HTTPConnectionScope, Scope

__all__: tuple[str, ...] = ("ASGIHandler", "HTTPException")

#: ---
#: Useful typing aliases.
type AnyRequest = Request | Error | BatchRequest
type AnyResponse = Response | BatchResponse | None

#: ---
#: Ensure that "Content-Type" is a valid JSON header.
JSON_CTYPE_REGEXB: re.Pattern[bytes] = re.compile(
    rb"(?:application/|[\w.-]+/[\w.+-]+?\+)json$",
    flags=re.IGNORECASE,
)


@dataclass(kw_only=True, slots=True)
class ASGIHandler:
    """
    Base class representing the ``ASGI`` entry point.
    """

    #: The title of the API.
    title: str = "jsonrpc-py"

    #: The version of the API.
    version: str = "0.1.0"

    #: A description of the API.
    description: str | None = None

    #: A URL to the Terms of Service for the API.
    terms_of_service: str | None = None

    #: The contact information for the API.
    contact: Contact | None = None

    #: The license information for the API.
    license: License | None = None

    #: An array of servers, which provide connectivity information to a target server.
    servers: list[Server] | None = None

    #: An element to hold various schemas for the specification.
    components: Components | None = None

    #: Additional external documentation.
    external_docs: ExternalDocumentation | None = None

    #: The URL where the OpenRPC schema will be served from.
    openrpc_url: str = "/openrpc.json"

    #: The :class:`~jsonrpc.AsyncDispatcher` object for this instance.
    dispatcher: AsyncDispatcher = field(default_factory=AsyncDispatcher, init=False)

    #: The :class:`~jsonrpc.JSONSerializer` object for this instance.
    serializer: JSONSerializer = field(default_factory=JSONSerializer, init=False)

    #: The :class:`~jsonrpc.LifespanEvents` object for this instance.
    events: LifespanEvents = field(default_factory=LifespanEvents, init=False)

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}()"

    async def __call__(self, scope: Scope, receive: ASGIReceiveCallable, send: ASGISendCallable) -> None:
        match scope["type"]:
            case "http":
                await HTTPHandler(scope=scope, receive=receive, send=send, app=self)  # type: ignore[arg-type]
            case "lifespan":
                await LifespanManager(receive=receive, send=send, events=self.events)
            case _:
                raise ValueError("Only ASGI/HTTP connections are allowed")

    @property
    def openrpc(self) -> OpenRPC:
        """
        Returns the :class:`~jsonrpc.openrpc.OpenRPC` schema object.
        """
        return OpenRPC(
            info=Info(
                title=self.title,
                version=self.version,
                description=self.description,
                terms_of_service=self.terms_of_service,
                contact=self.contact,
                license=self.license,
            ),
            servers=self.servers,
            methods=[function.schema for function in self.dispatcher.registry.values()],
            components=self.components,
            external_docs=self.external_docs,
        )


class RequestAborted(Exception):
    __slots__: tuple[str, ...] = ()


@dataclass(kw_only=True, slots=True)
class HTTPException(Exception):
    """
    Describes an exception that occurred during the processing of HTTP requests.
    """

    #: HTTP response status code.
    status: HTTPStatus


@dataclass(kw_only=True, slots=True)
class HTTPHandler(Awaitable[None]):
    scope: HTTPConnectionScope
    receive: ASGIReceiveCallable
    send: ASGISendCallable
    app: ASGIHandler

    async def __await_impl__(self) -> None:
        try:
            #: ---
            #: Handle HTTP requests for the API documentation.
            if payload := self.get_openrpc_schema():
                await self.send_response(payload=payload)
                return

            #: ---
            #: Might be "405 Method Not Allowed" or "415 Unsupported Media Type".
            self.negotiate_content()

            #: ---
            #: Might be "400 Bad Request" or abort.
            try:
                payload = await self.read_request_body()
            except RequestAborted:
                return
            if not payload:
                raise HTTPException(status=HTTPStatus.BAD_REQUEST)

            #: ---
            #: Should be "200 OK" or "204 No Content".
            if payload := await self.parse_payload(payload):
                await self.send_response(payload=payload)
            else:
                await self.send_response(status=HTTPStatus.NO_CONTENT)

        #: ---
        #: Should be sent as is.
        except HTTPException as exc:
            await self.send_response(status=exc.status)
        #: ---
        #: Must be "504 Gateway Timeout" only.
        except (TimeoutError, CancelledError):
            await self.send_response(status=HTTPStatus.GATEWAY_TIMEOUT)

    def negotiate_content(self) -> None:
        if self.scope["method"] != HTTPMethod.POST:
            raise HTTPException(status=HTTPStatus.METHOD_NOT_ALLOWED)
        for key, value in self.scope["headers"]:
            if key == b"content-type" and not JSON_CTYPE_REGEXB.match(value):
                raise HTTPException(status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE)

    async def read_request_body(self) -> bytes:
        with BytesIO() as raw_buffer:
            while True:
                event: ASGIReceiveEvent = await self.receive()
                match event["type"]:
                    case "http.request":
                        raw_buffer.write(event.get("body", b""))  # type: ignore[arg-type]
                        if not event.get("more_body", False):
                            break
                    case "http.disconnect":
                        #: ---
                        #: Client was disconnected too early:
                        raise RequestAborted

            return raw_buffer.getvalue()

    async def send_response(
        self,
        *,
        status: HTTPStatus = HTTPStatus.OK,
        payload: bytes = b"",
        buffer_size: int = DEFAULT_BUFFER_SIZE,
    ) -> None:
        headers: list[tuple[bytes, bytes]] = [
            (b"content-type", b"application/json"),
        ]
        if status == HTTPStatus.METHOD_NOT_ALLOWED:
            headers.insert(0, (b"allow", HTTPMethod.POST.encode("ascii")))
        #: ---
        #: Initial response message:
        await self.send({"type": "http.response.start", "status": status, "headers": headers})
        #: ---
        #: Yield chunks of response:
        with BytesIO(payload) as raw_buffer:
            while chunk := raw_buffer.read(buffer_size):
                await self.send({"type": "http.response.body", "body": chunk, "more_body": True})
            else:
                #: ---
                #: Final closing message:
                await self.send({"type": "http.response.body", "body": b"", "more_body": False})

    def get_openrpc_schema(self) -> bytes:
        if self.scope["method"] == HTTPMethod.GET and self.scope["path"] == self.app.openrpc_url:
            return self.app.serializer.serialize(self.app.openrpc.json)

        return b""

    async def parse_payload(self, payload: bytes) -> bytes:
        def write_error(error: Error) -> bytes:
            response: Response = Response(error=error, response_id=None)
            return self.app.serializer.serialize(response.json)

        try:
            obj: Any = self.app.serializer.deserialize(payload)
        except Error as error:
            return write_error(error)

        is_batch_request: bool = isinstance(obj, MutableSequence) and len(obj) >= 1
        request: AnyRequest = (BatchRequest if is_batch_request else Request).from_json(obj)

        if not (response := await self.process_request(request)):
            return b""

        try:
            return self.app.serializer.serialize(response.json)
        except Error as error:
            return write_error(error)

    async def process_request(self, obj: AnyRequest) -> AnyResponse:
        match obj:
            case Error():
                return self.on_error(obj)
            case Request():
                return await self.on_request(obj)
            case BatchRequest():
                return await self.on_batch_request(obj)

    def on_error(self, error: Error) -> Response:
        return Response(error=error, response_id=None)

    async def on_request(self, request: Request) -> Response | None:
        coroutine: Coroutine[Any, Any, Any] = self.app.dispatcher.dispatch(
            request.method,
            *request.args,
            **request.kwargs,
        )
        if request.is_notification:
            run_in_background(coroutine)
            return None
        try:
            result: Any = await coroutine
            return Response(body=result, response_id=request.request_id)
        except Error as error:
            return Response(error=error, response_id=request.request_id)

    async def on_batch_request(self, batch_request: BatchRequest) -> BatchResponse:
        responses: tuple[AnyResponse, ...] = await CancellableGather.map(self.process_request, batch_request)
        return BatchResponse(response for response in responses if isinstance(response, Response))
