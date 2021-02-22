"""This module defines all exceptions that JSON classes uses."""
from __future__ import annotations
from typing import Any
from inspect import getmodule


class JSONClassRedefinitionException(Exception):
    """This exception is raised when user defines a JSON class with a name that
    exists before in the same graph.
    """

    def __init__(self, new_class: type, exist_class: type) -> None:
        """Create an exception that notifies the user that a class with
        duplicated name is defined twice.

        Args:
            new_class (type): The new class which is putting on the graph.
            exist_class(type): The existing class which the user defined.
        """
        name = new_class.__name__
        original_module = getmodule(exist_class)
        assert original_module is not None
        original_file = original_module.__file__
        new_module = getmodule(new_class)
        assert new_module is not None
        new_file = new_module.__file__
        graph = exist_class.config.class_graph
        message = (f'Existing JSON Class \'{name}\' in graph \'{graph}\' is '
                   f'defined at \'{original_file}\'. Cannot define new JSON '
                   f'class with same name in same graph \'{graph}\' at '
                   f'\'{new_file}\'.')
        super().__init__(message)


class JSONClassNotFoundException(Exception):
    """This exception is raised when a JSON class with name is not found on a
    graph.
    """
    def __init__(self, class_name: str, graph_name: str):
        message = (f'JSON Class with name \'{class_name}\' in graph '
                   f'\'{graph_name}\' is not found.')
        super().__init__(message)


class ObjectNotFoundException(Exception):
    """ObjectNotFoundException is designed to be raised by jsonclasses ORM
    integration implementations. Server authors and jsonclasses server
    integration authors should catch this to present error to frontend clients.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class UniqueConstraintException(Exception):
    """UniqueConstraintException is designed to be raised by JSON Classes ORM
    integration implementations. When saving objects into the database, if
    object violates the uniqueness rule, this exception should be raised.
    """

    def __init__(self, value: Any, field: str):
        self.field = field
        self.value = value
        self.message = (f'Value \'{value}\' at \'{field}\' is not unique.')
        self.keypath_messages = {
            field: self.message
        }
        super().__init__(self.message)


class ValidationException(Exception):
    """ValidationException is throwed on jsonclass object validation or on
    eager validation. Server authors and jsonclasses server integration authors
    should catch this to present error to frontend clients.
    """

    def __init__(self, keypath_messages: dict[str, str], root: Any):
        self.keypath_messages = keypath_messages
        self.message = self.formatted_keypath_messages()
        self.root = root
        super().__init__(self.message)

    def formatted_keypath_messages(self):
        """The formatted keypath message for print."""
        retval = 'Json classes validation failed:\n'
        for k, v in self.keypath_messages.items():
            retval += f'  \'{k}\': {v}\n'
        return retval


class AbstractJSONClassException(Exception):
    """Abstract class should not be initialized nor serialized into database.
    When an abstract JSON class is initialized, this error should be raised.
    """

    def __init__(self, class_: type) -> None:
        self.class_ = class_
        self.message = (f'{class_.__name__} is an abstract class and should '
                        'not be initialized')
        super().__init__(self.message)


class JSONClassResetError(Exception):
    """This error is raised when an ORM object is new and thus cannot be reset.
    """

    def __init__(self) -> None:
        self.message = 'object is new and cannot be reset'
        super().__init__(self.message)


class JSONClassResetNotEnabledError(Exception):
    """This error is raised when calling reset on an object which class doesn't
    enable `reset_all_fields`.
    """

    def __init__(self) -> None:
        self.message = 'reset called on a reset disabled object'
        super().__init__(self.message)
