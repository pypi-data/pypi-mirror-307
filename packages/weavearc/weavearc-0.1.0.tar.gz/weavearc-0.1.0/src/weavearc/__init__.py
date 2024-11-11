"""
cortex.base is a module that provides the core
functionality any API needs to run.
"""

from msgspec import Meta, field

from .data import (
    AsyncRepository,
    ConstContainer,
    CreateResult,
    DeleteResult,
    Entity,
    BaseModel,
    ReadAllResult,
    ReadResult,
    Repository,
    UpdateResult,
    ValueObject,
)
from .services import AsyncService, ServiceExecutor
from .utils.builders import DynamicDict

__all__: list[str] = [
    "ConstContainer",
    "BaseModel",
    "field",
    "Meta",
    "BaseRequest",
    "Meta",
    "field",
    "AsyncRepository",
    "Repository",
    "ReadAllResult",
    "ReadResult",
    "CreateResult",
    "UpdateResult",
    "DeleteResult",
    "ServiceExecutor",
    "Entity",
    "ValueObject",
    "AsyncService",
    "DynamicDict",
]
