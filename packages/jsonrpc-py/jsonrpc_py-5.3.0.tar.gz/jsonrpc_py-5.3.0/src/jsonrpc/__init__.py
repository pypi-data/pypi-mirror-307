"""
Pure zero-dependency JSON-RPC 2.0 and OpenRPC implementation.
"""

from __future__ import annotations

from .asgi import ASGIHandler, HTTPException
from .dispatcher import AsyncDispatcher, Function
from .errors import Error, ErrorEnum
from .lifespan import LifespanEvents
from .requests import BatchRequest, Request
from .responses import BatchResponse, Response
from .serializers import JSONSerializer

__all__: tuple[str, ...] = (
    "ASGIHandler",
    "AsyncDispatcher",
    "BatchRequest",
    "BatchResponse",
    "Error",
    "ErrorEnum",
    "Function",
    "HTTPException",
    "JSONSerializer",
    "LifespanEvents",
    "Request",
    "Response",
)
