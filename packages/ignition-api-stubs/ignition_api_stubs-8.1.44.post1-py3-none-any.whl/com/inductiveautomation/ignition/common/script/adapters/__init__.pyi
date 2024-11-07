from typing import Any, Iterator, List, Optional

from com.inductiveautomation.ignition.common.gson import JsonObject
from dev.coatl.helper.types import AnyStr
from java.lang import Object
from org.python.core import PyObject

class PyJsonObjectAdapter(Object):
    def __init__(self, obj: JsonObject) -> None: ...
    def __delitem__(self, key: PyObject) -> None: ...
    def __findattr_ex__(self, name: AnyStr) -> PyObject: ...
    def __finditem__(self, key: PyObject) -> PyObject: ...
    def __iter__(self) -> Iterator[Any]: ...
    def __len__(self) -> int: ...
    def __setitem__(self, key: PyObject, value: PyObject) -> None: ...
    def clear(self) -> None: ...
    def get(self, key: PyObject, default: Optional[PyObject] = ...) -> PyObject: ...
    def has_key(self, key: PyObject) -> bool: ...
    def items(self) -> List[PyObject]: ...
    def iteritems(self) -> PyObject: ...
    def iterkeys(self) -> PyObject: ...
    def itervalues(self) -> PyObject: ...
    def keys(self) -> List[PyObject]: ...
    def pop(self, key: PyObject) -> PyObject: ...
    def popitem(self) -> PyObject: ...
    def setdefault(self, key: PyObject, default: PyObject) -> PyObject: ...
    def update(self, *args: PyObject, **kwargs: AnyStr) -> None: ...
    def values(self) -> List[PyObject]: ...
