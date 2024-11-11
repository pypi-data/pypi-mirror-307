"""Type stubs for common_types module."""

from typing import (
    Any,
    Awaitable,
    Callable,
    Optional,
    Type,
    TypeVar,
    Union,
    overload,
)
from typing_extensions import ParamSpec

# Type variables
T = TypeVar("T")
R = TypeVar("R")
C = TypeVar("C")
K = TypeVar("K")
V = TypeVar("V")
F = TypeVar("F", bound=Callable[..., Awaitable[Any]])
P = ParamSpec("P")

# Covariant type variables
T_co = TypeVar("T_co", covariant=True)
C_co = TypeVar("C_co", covariant=True)

# Deprecated decorator overloads
@overload
def deprecated(
    obj: Union[Callable[P, R], Type[C]],
) -> Union[Callable[P, R], Type[C]]: ...
@overload
def deprecated(
    *,
    reason: Optional[str] = ...,
    alternative: Optional[str] = ...,
    version: Optional[str] = ...,
    category: Type[Warning] = ...,
) -> Callable[[Union[Callable[P, R], Type[C]]], Union[Callable[P, R], Type[C]]]: ...
