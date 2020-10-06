"""This module defineds the internal JSON Class mapping graph."""
from __future__ import annotations
from typing import Dict, Type, TypeVar, TYPE_CHECKING
from inspect import getmodule
if TYPE_CHECKING:
    from .json_object import JSONObject
    T = TypeVar('T', bound=JSONObject)


class JSONClassRedefinitionError(Exception):
    """This error is raised when you define a JSON Class with a name that
    exists before.
    """

    def __init__(self, new_cls: Type[JSONObject], exist_cls: Type[JSONObject]):
        name = new_cls.__name__
        original_module = getmodule(exist_cls)
        assert original_module is not None
        original_file = original_module.__file__
        new_module = getmodule(new_cls)
        assert new_module is not None
        new_file = new_module.__file__
        graph = exist_cls.config.graph
        message = (f'Existing JSON Class \'{name}\' in graph \'{graph}\' is '
                   f'defined at \'{original_file}\'. Cannot define new JSON '
                   f'Class with same name in same graph \'{graph}\' at '
                   f'\'{new_file}\'.')
        super().__init__(message)


class JSONClassNotFoundError(Exception):
    """This exception is raised when a specified JSON Class is not found on a
    graph.
    """
    def __init__(self, name: str, graph: str = 'default'):
        message = (f'JSON Class with name \'{name}\' in graph \'{graph}\' is '
                   'not found.')
        super().__init__(message)


class ClassGraphMap:

    def __init__(self):
        self._map: Dict[str, ClassGraph] = {}

    def graph(self, graph_name: str) -> ClassGraph:
        if self._map.get(graph_name) is None:
            self._map[graph_name] = ClassGraph(graph_name=graph_name)
        return self._map[graph_name]


class ClassGraph:

    def __init__(self, graph_name: str):
        self._graph_name = graph_name
        self._map: Dict[str, Type[JSONObject]] = {}

    def add(self, cls: Type[T]) -> Type[T]:
        """Add a JSON Class to the graph."""
        if self._map.get(cls.__name__) is not None:
            raise JSONClassRedefinitionError(cls, self._map[cls.__name__])
        self._map[cls.__name__] = cls
        return cls

    def get(self, cls_name: str) -> Type[JSONObject]:
        try:
            return self._map[cls_name]
        except KeyError:
            raise JSONClassNotFoundError(name=cls_name, graph=self._graph_name)


class_graph_map = ClassGraphMap()
