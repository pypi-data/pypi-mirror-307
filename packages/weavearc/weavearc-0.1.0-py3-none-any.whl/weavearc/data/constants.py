from __future__ import annotations

from typing import Any, Type

from weavearc.typing import T

from ..schema import BaseModel


class ConstContainer(BaseModel, kw_only=True, frozen=True):  # type: ignore[call-arg]
    """
    A fast and memory-efficient immutable container class using BaseModel.

    This class provides a base for creating constant containers with the following features:
    - Immutability (frozen=True)
    - Fast serialization and deserialization
    - Memory efficiency
    - Type checking support
    """

    @classmethod
    def create(cls: Type[T], **kwargs: Any) -> T:
        """
        Create a new instance of the ConstContainer or its subclass.
        This method provides a convenient way to create instances while maintaining type safety.
        """
        return cls(**kwargs)
