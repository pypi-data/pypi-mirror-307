"""Base decorators"""

import functools
from typing import Callable, Optional, Union, cast, overload

from weavearc.typing import P, R


@overload
def pure(func: Callable[P, R]) -> Callable[P, R]: ...


@overload
def pure(
    *, maxsize: int = 1024, typed: bool = False
) -> Callable[[Callable[P, R]], Callable[P, R]]: ...


def pure(
    func: Optional[Callable[P, R]] = None, *, maxsize: int = 1024, typed: bool = False
) -> Union[Callable[P, R], Callable[[Callable[P, R]], Callable[P, R]]]:
    """
    A decorator to mark functions as pure and cache their results using lru_cache.

    Args:
        func (Callable): The function to be decorated.
        maxsize (int): Maximum size of the cache. Default is 1024.
        typed (bool): If True, arguments of different types will be cached separately.

    Returns:
        Callable: The decorated function with caching applied.
    """
    if func is None:
        # The decorator is called with arguments
        def decorator(f: Callable[P, R]) -> Callable[P, R]:
            cached_f = functools.lru_cache(maxsize=maxsize, typed=typed)(f)
            # Expose cache_info and cache_clear if needed
            cached_f.cache_info = cached_f.cache_info  # type: ignore
            cached_f.cache_clear = cached_f.cache_clear  # type: ignore
            return cast(Callable[P, R], cached_f)

        return decorator
    else:
        # The decorator is called without arguments
        cached_func = functools.lru_cache(maxsize=maxsize, typed=typed)(func)
        # Expose cache_info and cache_clear if needed
        cached_func.cache_info = cached_func.cache_info  # type: ignore
        cached_func.cache_clear = cached_func.cache_clear  # type: ignore
        return cast(Callable[P, R], cached_func)
