from __future__ import annotations

from asyncio import CancelledError
from collections import OrderedDict
from dataclasses import dataclass, field
from functools import partial
from inspect import Signature, isfunction
from typing import TYPE_CHECKING, overload

from .errors import Error, ErrorEnum
from .openrpc import Method
from .utilities import ensure_async

if TYPE_CHECKING:
    from collections.abc import Callable
    from inspect import BoundArguments
    from typing import Any, Self, Unpack

    from .typedefs import FunctionSchema

__all__: tuple[str, ...] = ("AsyncDispatcher", "Function")


@dataclass(kw_only=True, slots=True)
class AsyncDispatcher:
    """
    A simple class for storing user-defined functions.
    """

    #: The :py:class:`~collections.OrderedDict` object storage of user-defined functions.
    registry: OrderedDict[str, Function[..., Any]] = field(
        default_factory=OrderedDict,
        init=False,
        repr=False,
    )

    @overload
    def register[**P, T](
        self,
        user_function: Callable[P, T],
        /,
    ) -> Function[P, T]: ...

    @overload
    def register[**P, T](
        self,
        user_function: Callable[P, T],
        /,
        **kwargs: Unpack[FunctionSchema],
    ) -> Function[P, T]: ...

    @overload
    def register[**P, T](
        self,
        /,
        **kwargs: Unpack[FunctionSchema],
    ) -> Callable[[Callable[P, T]], Function[P, T]]: ...

    def register(self, user_function: Callable[..., Any] | None = None, /, **kwargs: Unpack[FunctionSchema]) -> Any:
        """
        Adds a user-defined function to the registry.

        :param user_function: A user-defined function.
        :param kwargs: Schema parameters of a function, also see :class:`~jsonrpc.openrpc.Method` parameters.
        :returns: The :class:`~jsonrpc.Function` object that has the same signature as ``user_function`` object.
        """
        if user_function is None:
            return partial(self.register, **kwargs)

        function: Function[..., Any] = Function.from_callable(user_function, **kwargs)
        self.registry[function.schema.name] = function
        self.registry.move_to_end(function.schema.name)
        return function

    async def dispatch(self, function_name: str, /, *args: Any, **kwargs: Any) -> Any:
        """
        Invokes a user-defined function by the function name.

        :param function_name: The name of function.
        :param args: Positional arguments for the provided function.
        :param kwargs: Keyword arguments for the provided function.
        :raises jsonrpc.Error: If the function doesn't exists, got invalid parameters or an unexpected internal error has occurred.
        :returns: Result of execution the user-defined function.
        """
        try:
            function: Function[..., Any] = self.registry[function_name]
        except KeyError as exc:
            raise Error(code=ErrorEnum.METHOD_NOT_FOUND, message=f"Function {function_name!r} isn't found") from exc

        try:
            params: BoundArguments = function.signature.bind(*args, **kwargs)
        except TypeError as exc:
            raise Error(code=ErrorEnum.INVALID_PARAMETERS, message=f"Invalid parameters: {exc!s}") from exc

        try:
            return await ensure_async(function.callback, *params.args, **params.kwargs)
        except (TimeoutError, CancelledError, Error):
            raise
        except Exception as exc:
            raise Error(code=ErrorEnum.INTERNAL_ERROR, message=f"Unexpected internal error: {exc!s}") from exc


@dataclass(kw_only=True, slots=True)
class Function[**P, T]:
    """
    Almost the same as a :py:func:`~functools.partial` function.
    """

    #: The original :py:class:`~collections.abc.Callable` object.
    callback: Callable[P, T]

    #: A :py:class:`~inspect.Signature` object of a function.
    signature: Signature

    #: A :class:`~jsonrpc.openrpc.Method` schema object of a function.
    schema: Method

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}()"

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T:
        return self.callback(*args, **kwargs)

    @classmethod
    def from_callable(cls, user_function: Callable[P, T], /, **kwargs: Unpack[FunctionSchema]) -> Self:
        """
        Constructs :class:`~jsonrpc.Function` object for the given callable object.

        :param user_function: A user-defined function.
        :param kwargs: Schema parameters of a function, also see :class:`~jsonrpc.openrpc.Method` parameters.
        :raises TypeError: If a ``user_function`` object is not a user-defined function.
        """
        if not isfunction(user_function):
            raise TypeError(f"a user-defined function was expected, got {type(user_function).__name__!r}")

        if not kwargs.get("name"):
            kwargs |= {"name": user_function.__name__}

        return cls(
            callback=user_function,
            signature=Signature.from_callable(user_function),
            schema=Method(**kwargs),
        )
