"""Base service classes for all services in the application.

This module defines an abstract base class for synchronous services, ensuring a
consistent interface across all service implementations. Services are responsible
for encapsulating the core business logic of the application, providing a clear
separation between the application's interface (controllers) and its core
operational logic (services).

Each service should implement the `execute` method, which contains the logic to
be performed. This approach allows for a modular, maintainable, and testable
architecture, where services can be independently developed, tested, and
reused across the application.
"""

from __future__ import annotations

import asyncio
import functools
from typing import Awaitable, Callable, Generic, Union

from weavearc.typing import P, R, T

from ..data.schema import BaseModel


class Service(BaseModel, Generic[T]):
    """Abstract base class for synchronous services within the application.

    Services extending this class must implement the `execute` method, defining the specific
    operations to be carried out by the service. The `execute` method encapsulates the service's
    main functionality and is designed to be invoked by the application's controllers or other services.

    Raises:
        NotImplementedError: If a subclass does not implement the `execute` method.
    """

    def execute(self) -> T:
        """Performs the service's main operations.

        This method should contain the primary business logic for the service. It may
        return a result or `None` if there is no result to return.

        Returns:
            T: The result of the service execution, if applicable.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError("Method not implemented.")

    @staticmethod
    def setup(func: Callable[P, R]) -> Callable[P, R]:
        """
        Decorator to invoke the instance's `setup` method before executing the synchronous `execute` method.

        This decorator ensures that the `setup` method is called on the instance (`self`)
        before the decorated synchronous method is executed. It's designed to provide
        a flexible setup mechanism for different service classes, allowing each class
        to define its own setup logic.

        **Requirements:**
        - The decorated class must implement a `setup` method that takes no arguments and returns `None`.

        Args:
            func (Callable[P, R]): The synchronous method to be decorated.

        Returns:
            Callable[P, R]: The wrapped synchronous method with setup invoked beforehand.

        Raises:
            AttributeError: If the class does not implement a callable `setup` method.

        Example:
            ```python
            class ExampleService(Service):
                def setup(self) -> None:
                    # Setup logic here
                    pass

                @Service.setup
                def execute(self) -> SomeResultType:
                    # Method implementation
                    pass
            ```
        """

        @functools.wraps(func)
        def wrapper(self, *args: P.args, **kwargs: P.kwargs) -> R:
            """
            Wrapper function that calls `self.setup()` before executing the decorated method.

            Args:
                self: The instance of the class containing the method.
                *args: Variable length argument list.
                **kwargs: Arbitrary keyword arguments.

            Returns:
                R: The result of the decorated synchronous method.

            Raises:
                AttributeError: If the class does not implement a callable `setup` method.
            """
            setup_method = getattr(self, "setup", None)
            if not callable(setup_method):
                raise AttributeError(
                    f"Class '{self.__class__.__name__}' must implement a callable 'setup' method."
                )
            setup_method()
            return func(self, *args, **kwargs)

        return wrapper


class AsyncService(BaseModel, Generic[T]):
    """Abstract base class for asynchronous services within the application.

    An asynchronous service is a service that can be `awaited`.

    Raises:
        NotImplementedError: If the subclass doesn't implement the `execute` method.
    """

    async def execute(self) -> T:
        """Performs the service's main operations asynchronously.

        This method should contain the primary business logic for the service. It may
        return a result or `None` if there is no result to return.

        Returns:
            T: The result of the service execution, if applicable.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError("Method not implemented.")

    @staticmethod
    def setup(func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        """
        Decorator to invoke the instance's `setup` method before executing the asynchronous `execute` method.

        This decorator ensures that the `setup` method is called on the instance (`self`)
        before the decorated asynchronous method is executed. It's designed to provide
        a flexible setup mechanism for different service classes, allowing each class
        to define its own setup logic.

        **Requirements:**
        - The decorated class must implement a `setup` method that takes no arguments and returns `None`.
        - The `setup` method can be either synchronous or asynchronous.

        Args:
            func (Callable[P, Awaitable[R]]): The asynchronous method to be decorated.

        Returns:
            Callable[P, Awaitable[R]]: The wrapped asynchronous method with setup invoked beforehand.

        Raises:
            AttributeError: If the class does not implement a callable `setup` method.

        Example:
            ```python
            class ExampleAsyncService(AsyncService):
                async def setup(self) -> None:
                    # Asynchronous setup logic here
                    await some_async_initialization()

                @AsyncService.setup
                async def execute(self) -> SomeAsyncResult:
                    # Method implementation
                    pass
            ```
        """

        @functools.wraps(func)
        async def wrapper(self, *args: P.args, **kwargs: P.kwargs) -> R:
            """
            Wrapper function that calls `self.setup()` before executing the decorated method.

            Args:
                self: The instance of the class containing the method.
                *args: Variable length argument list.
                **kwargs: Arbitrary keyword arguments.

            Returns:
                R: The result of the decorated asynchronous method.

            Raises:
                AttributeError: If the class does not implement a callable `setup` method.
            """
            setup_method = getattr(self, "setup", None)
            if not callable(setup_method):
                raise AttributeError(
                    f"Class '{self.__class__.__name__}' must implement a callable 'setup' method."
                )
            if asyncio.iscoroutinefunction(setup_method):
                await setup_method()
            else:
                setup_method()
            return await func(self, *args, **kwargs)

        return wrapper


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

        This method instantiates the service class with the given arguments and executes it.
        It automatically handles both synchronous and asynchronous services.

        Args:
            service_class (Callable[P, Union[Service[T], AsyncService[T]]]): The service class to instantiate and execute.
            *args: Positional arguments to pass to the service class constructor.
            **kwargs: Keyword arguments to pass to the service class constructor.

        Returns:
            T: The result from the service execution.

        Raises:
            ValueError: If the provided class instance is neither a Service nor an AsyncService.
        """
        service_instance = service_class(*args, **kwargs)

        if isinstance(service_instance, AsyncService):
            result: T = await service_instance.execute()
        elif isinstance(service_instance, Service):
            result: T = await asyncio.get_running_loop().run_in_executor(service_instance.execute)()
        else:
            raise ValueError(
                "Invalid service type. Must be either Service or AsyncService."
            )
        return result
