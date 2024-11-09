from __future__ import annotations

from dataclasses import dataclass, field
from traceback import format_exc
from typing import TYPE_CHECKING
from weakref import WeakSet

from .utilities import Awaitable, CancellableGather, ensure_async

if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import Any

    from .typedefs import ASGIReceiveCallable, ASGISendCallable

__all__: tuple[str, ...] = ("LifespanEvents", "LifespanManager")


@dataclass(kw_only=True, slots=True)
class LifespanEvents:
    """
    Simple class for storing the user-defined functions that running
    when application is initiated and shutting down.
    """

    #: The :py:class:`~weakref.WeakSet` collection of startup functions.
    startup_events: WeakSet[Callable[..., Any]] = field(default_factory=WeakSet, init=False)

    #: The :py:class:`~weakref.WeakSet` collection of shutdown functions.
    shutdown_events: WeakSet[Callable[..., Any]] = field(default_factory=WeakSet, init=False)

    def on_startup[F: Callable[..., Any]](self, user_function: F, /) -> F:
        """
        Decorator for the adding a function which will be executed
        when application is initiated.

        Example usage::

            >>> @app.events.on_startup
            ... def startup_callback() -> None:
            ...     print("Some important message")

        :param user_function: The :py:class:`~collections.abc.Callable` object representing the user-defined function.
        :returns: The unmodified ``user_function`` object, passed in the parameters.
        """
        self.startup_events.add(user_function)
        return user_function

    def on_shutdown[F: Callable[..., Any]](self, user_function: F, /) -> F:
        """
        Decorator for the adding a function which will be executed
        when application is shutting down.

        Example usage::

            >>> @app.events.on_shutdown
            ... async def shutdown_callback() -> None:
            ...     await important_function()

        :param user_function: The :py:class:`~collections.abc.Callable` object representing the user-defined function.
        :returns: The unmodified ``user_function`` object, passed in the parameters.
        """
        self.shutdown_events.add(user_function)
        return user_function


@dataclass(kw_only=True, slots=True)
class LifespanManager(Awaitable[None]):
    receive: ASGIReceiveCallable
    send: ASGISendCallable
    events: LifespanEvents

    async def __await_impl__(self) -> None:
        match await self.receive():
            case {"type": "lifespan.startup"}:
                await self.on_startup(self.events.startup_events)
            case {"type": "lifespan.shutdown"}:
                await self.on_shutdown(self.events.shutdown_events)

    async def on_startup(self, startup_events: WeakSet[Callable[..., Any]], /) -> None:
        try:
            if startup_events:
                await CancellableGather.map(ensure_async, startup_events)
        except BaseException:
            traceback: str = format_exc()
            await self.send({"type": "lifespan.startup.failed", "message": traceback})
            raise
        else:
            await self.send({"type": "lifespan.startup.complete"})

    async def on_shutdown(self, shutdown_events: WeakSet[Callable[..., Any]], /) -> None:
        try:
            if shutdown_events:
                await CancellableGather.map(ensure_async, shutdown_events)
        except BaseException:
            traceback: str = format_exc()
            await self.send({"type": "lifespan.shutdown.failed", "message": traceback})
            raise
        else:
            await self.send({"type": "lifespan.shutdown.complete"})
