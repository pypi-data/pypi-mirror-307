from abc import ABC, ABCMeta
from dataclasses import dataclass
from enum import Flag, auto, Enum
from typing import Self, Optional, Any

from edri.dataclass.directive import ResponseDirective
from edri.dataclass.directive.base import InternalServerErrorResponseDirective
from edri.dataclass.event import Event
from edri.dataclass.response import ResponseStatus


class MiddlewareMeta(ABCMeta):
    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)

        # Dynamically create the list of methods from the class being created
        required_methods = []
        for base in cls.__mro__:
            for method_name, method in base.__dict__.items():
                if callable(method) and not method_name.startswith('__'):
                    required_methods.append(method_name)

        # Check if at least one method is implemented in the subclass
        if not any(attr in cls.__dict__ for attr in required_methods):
            raise TypeError(
                f"Class '{cls.__name__}' must implement at least one of the following methods: {", ".join(required_methods)}. "
                "Ensure that your class provides an implementation for at least one of these methods."
            )


@dataclass
class MiddlewareControl:
    """
    Encapsulates the outcome of middleware processing with details on the action type, optional data, errors,
    and an optional replacement event.
    """

    class ActionType(Enum):
        """Enum to define middleware processing actions."""
        CONTINUE = auto()
        STOP = auto()
        REPLACE_EVENT = auto()

    action: ActionType
    event: Optional[Event] = None

    @classmethod
    def continue_processing(cls) -> Self:
        """Creates a MiddlewareControl instance indicating processing should continue."""
        return cls(action=cls.ActionType.CONTINUE)

    @classmethod
    def stop_processing(cls, directive: Optional[ResponseDirective] = None) -> Self:
        """Creates a MiddlewareControl instance indicating processing should stop."""
        return cls(action=cls.ActionType.STOP)

    @classmethod
    def replace_event(cls, event: Event) -> Self:
        """
        Creates a MiddlewareControl instance that replaces the current event with a new one.

        Args:
            event (Event): The event that should replace the current event in processing.

        Returns:
            MiddlewareControl: An instance with action set to REPLACE_EVENT.
        """
        return cls(action=cls.ActionType.REPLACE_EVENT, event=event)


class MiddlewareProcessor:
    """
    Processes the MiddlewareControl outcome from each middleware layer, determining if processing should continue
    and handling alternate events if returned by a middleware.

    Attributes:
        logger (Any): Logger instance for logging outcomes.

    Methods:
        process_control (Optional[Event]): Evaluates the control object and handles each action type.
    """

    def __init__(self, logger: Any):
        """Initializes MiddlewareProcessor with a logger."""
        self.logger = logger

    def process_control(self, control: MiddlewareControl, event: Event) -> Optional[Event]:
        """
        Evaluates the MiddlewareControl action and determines the flow of processing.

        Args:
            control (MiddlewareControl): The outcome of a middleware's processing.
            event (Event): The event being processed.

        Returns:
            Optional[Event]: If a new event is returned, processing should stop, and the new event will be processed.
        """
        if control.action == MiddlewareControl.ActionType.CONTINUE:
            return None  # Continue processing to the next middleware

        elif control.action == MiddlewareControl.ActionType.STOP:
            self.logger.debug("Processing stopped: %s", control.error)
            event.response.set_status(ResponseStatus.FAILED)
            if control.error:
                event.response.add_directive(InternalServerErrorResponseDirective(control.error))
            return None  # Stop processing

        elif control.action == MiddlewareControl.ActionType.MODIFY_RESPONSE:
            self.logger.debug("Response modified with data: %s", control.data)
            if control.data:
                # Apply data modifications to event/response here as needed
                pass
            return None  # Continue processing after modification

        elif control.action == MiddlewareControl.ActionType.ERROR:
            self.logger.error("Error in middleware: %s", control.error)
            event.response.set_status(ResponseStatus.FAILED)
            event.response.add_directive(InternalServerErrorResponseDirective(control.error))
            return None  # Stop processing due to error

        elif control.action == MiddlewareControl.ActionType.REPLACE_EVENT:
            self.logger.debug("Event replaced by middleware. New event: %s", control.new_event)
            return control.new_event  # Return new event to replace the current one

        return None


class Middleware(ABC, metaclass=MiddlewareMeta):
    """
    Abstract base class for middleware components.
    Middleware classes derived from this must implement at least one of
    'process_request' and 'process_response'.
    """

    def process_request(self, event: Event) -> MiddlewareControl:
        """
        Method to process the request before it reaches the main application logic.
        Should be implemented in a subclass.

        :param event: The request event to be processed.
        """
        raise NotImplementedError("Must implement process_request or process_response")

    def process_response(self, event: Event) -> MiddlewareControl:
        """
        Method to process the response before it is sent to the client.
        Should be implemented in a subclass.

        :param event: The response event to be processed.
        """
        raise NotImplementedError("Must implement process_request or process_response")

    @classmethod
    def __getattr__(cls, name):
        prefix = "is_"
        if name.startswith(prefix):
            capability_name = f"process_{name[len(prefix):]}"
            method = cls.__dict__.get(capability_name)
            return callable(method)
        raise AttributeError("type object '%s' has no attribute '%s'", cls.__name__, name)
