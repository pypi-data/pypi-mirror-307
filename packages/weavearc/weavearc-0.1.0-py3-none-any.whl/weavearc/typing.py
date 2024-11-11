"""Common types and decorators for the application."""

import functools
import warnings
from typing import (
    Any,
    Callable,
    Optional,
    Type,
    TypeVar,
    Union,
    overload,
)
from typing_extensions import ParamSpec, Awaitable

# Define type variables for general use
T = TypeVar("T")
R = TypeVar("R")
C = TypeVar("C")
K = TypeVar("K")
V = TypeVar("V")
F = TypeVar("F", bound=Callable[..., Awaitable[Any]])
s_F = TypeVar("s_F", bound=Callable[..., Any])
P = ParamSpec("P")

# Covariant type variables
T_co = TypeVar("T_co", covariant=True)
C_co = TypeVar("C_co", covariant=True)

# Define a tuple of string types for compatibility checks
string_types = (str, bytes)


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


def deprecated(
    obj: Optional[Union[Callable[P, R], Type[C]]] = None,
    *,
    reason: Optional[str] = None,
    alternative: Optional[str] = None,
    version: Optional[str] = None,
    category: Type[Warning] = DeprecationWarning,
) -> Union[
    Callable[P, R],
    Type[C],
    Callable[[Union[Callable[P, R], Type[C]]], Union[Callable[P, R], Type[C]]],
]:
    """
    Decorator to mark functions or classes as deprecated.

    Usage:
    - Without arguments: `@deprecated`
    - With arguments: `@deprecated(reason="...", alternative="...", version="...")`

    Parameters:
        obj: The function or class to be deprecated. If None, the decorator is used with arguments.
        reason: Reason for deprecation.
        alternative: Suggested alternative.
        version: Version in which deprecation occurred.
        category: Warning category (default: DeprecationWarning).

    Returns:
        The decorated function or class, or a decorator.
    """
    if obj is not None:
        # Used as @deprecated without arguments
        if isinstance(obj, type):
            # Decorating a class
            return _decorate_class(
                obj,
                reason=reason,
                alternative=alternative,
                version=version,
                category=category,
            )
        elif callable(obj):
            # Decorating a function
            return _decorate_function(
                obj,
                reason=reason,
                alternative=alternative,
                version=version,
                category=category,
            )
        else:
            raise TypeError(
                f"Unsupported type for deprecated decorator: {type(obj).__name__}"
            )
    else:
        # Used as @deprecated(...) with arguments
        def decorator(
            obj: Union[Callable[P, R], Type[C]],
        ) -> Union[Callable[P, R], Type[C]]:
            if isinstance(obj, type):
                return _decorate_class(
                    obj,
                    reason=reason,
                    alternative=alternative,
                    version=version,
                    category=category,
                )
            elif callable(obj):
                return _decorate_function(
                    obj,
                    reason=reason,
                    alternative=alternative,
                    version=version,
                    category=category,
                )
            else:
                raise TypeError(
                    f"Unsupported type for deprecated decorator: {type(obj).__name__}"
                )

        return decorator


def _decorate_function(
    func: Callable[P, R],
    *,
    reason: Optional[str],
    alternative: Optional[str],
    version: Optional[str],
    category: Type[Warning],
) -> Callable[P, R]:
    message = f"Call to deprecated function '{func.__name__}'."
    if reason:
        message += f" {reason}"
    if alternative:
        message += f" Use '{alternative}' instead."
    if version:
        message += f" Deprecated since version {version}."

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        warnings.simplefilter("always", category)
        warnings.warn(
            message,
            category=category,
            stacklevel=2,
        )
        warnings.simplefilter("default", category)
        return func(*args, **kwargs)

    return wrapper


def _decorate_class(
    cls: Type[C],
    *,
    reason: Optional[str],
    alternative: Optional[str],
    version: Optional[str],
    category: Type[Warning],
) -> Type[C]:
    message = f"Call to deprecated class '{cls.__name__}'."
    if reason:
        message += f" {reason}"
    if alternative:
        message += f" Use '{alternative}' instead."
    if version:
        message += f" Deprecated since version {version}."

    def __init__(self: Any, *args: Any, **kwargs: Any) -> None:
        warnings.simplefilter("always", category)
        warnings.warn(
            message,
            category=category,
            stacklevel=2,
        )
        warnings.simplefilter("default", category)
        super(cls, self).__init__(*args, **kwargs)

    Wrapped = type(
        cls.__name__,
        (cls,),
        {
            "__init__": __init__,
            "__doc__": cls.__doc__,
            "__module__": cls.__module__,
        },
    )
    return Wrapped  # Wrapped is of type Type[C]
