from __future__ import annotations

from dataclasses import Field, dataclass, field
from typing import TYPE_CHECKING, dataclass_transform

if TYPE_CHECKING:
    from typing import Any

__all__: tuple[str, ...] = ("ModelMeta",)


@dataclass_transform(kw_only_default=True, field_specifiers=(Field, field))
class ModelMeta(type):
    """
    A metaclass that simplifies the creation of data classes.
    """

    __slots__: tuple[str, ...] = ()

    def __new__(cls, name: str, bases: tuple[Any, ...], namespace: dict[str, Any], /, **kwargs: Any) -> type[Any]:
        klass, dataclass_wrapper = type(name, bases, namespace, **kwargs), dataclass(kw_only=True, slots=True)
        return dataclass_wrapper(klass)
