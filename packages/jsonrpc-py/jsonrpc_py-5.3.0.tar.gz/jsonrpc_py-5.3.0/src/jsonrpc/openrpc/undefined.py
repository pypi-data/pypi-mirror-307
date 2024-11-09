from __future__ import annotations

from typing import TYPE_CHECKING, final

if TYPE_CHECKING:
    from typing import Final, Literal

__all__: tuple[str, ...] = ("Undefined", "UndefinedType")


@final
class UndefinedType:
    """
    Sentinel to indicate the lack of a value when :py:data:`None` is ambiguous.
    """

    __slots__: tuple[str, ...] = ()

    def __repr__(self) -> Literal["Undefined"]:
        return "Undefined"

    def __hash__(self) -> Literal[0xDEADBEEF]:
        return 0xDEADBEEF

    def __bool__(self) -> Literal[False]:
        return False


Undefined: Final[UndefinedType] = UndefinedType()
