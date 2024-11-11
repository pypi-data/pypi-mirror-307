from typing import Generic, Union, Callable

from weavearc.typing import T, P
from ..data.schema import BaseModel

class Service(BaseModel, Generic[T]):
    """Abstract base class for synchronous services within the application.

    Services extending this class must implement the `execute` method, defining the specific
    operations to be carried out by the service. The `execute` method encapsulates the service's
    main functionality and is designed to be invoked by the application's controllers or other services.
    """

    def execute(self) -> T:
        """Performs the service's main operations.

        Returns:
            T: The result of the service execution, if applicable.
        """
        ...

class AsyncService(BaseModel, Generic[T]):
    """Abstract base class for asynchronous services within the application.

    An asynchronous service is a service that can be `awaited`.
    """

    async def execute(self) -> T:
        """Performs the service's main operations asynchronously.

        Returns:
            T: The result of the service execution, if applicable.
        """
        ...

class ServiceExecutor(BaseModel):
    """Executor for services, handling both synchronous and asynchronous services.

    This class provides a unified interface to execute services, whether they are synchronous
    or asynchronous, simplifying the invocation process for the rest of the application.
    """

    async def execute(
        self,
        service_class: Callable[P, Union[Service[T], AsyncService[T]]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> T:
        """Executes a given service class with provided arguments.

        Args:
            service_class (Callable[P, Union[Service[T], AsyncService[T]]]): The service class to instantiate and execute.
            *args: Positional arguments for the service class constructor.
            **kwargs: Keyword arguments for the service class constructor.

        Returns:
            T: The result from the service execution.
        """
        ...
