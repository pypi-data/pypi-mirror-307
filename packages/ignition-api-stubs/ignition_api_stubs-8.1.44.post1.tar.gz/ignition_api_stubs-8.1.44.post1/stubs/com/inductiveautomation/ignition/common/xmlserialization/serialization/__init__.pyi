from typing import Any, List

from com.inductiveautomation.ignition.common.xmlserialization import ClassNameResolver
from com.inductiveautomation.ignition.common.xmlserialization.encoding import (
    AttributeEncoder,
)
from com.inductiveautomation.ignition.common.xmlserialization.serialization.equalitydelegates import (
    EqualityDelegate,
)
from dev.coatl.helper.types import AnyStr as AnyStr
from java.lang import Class, Object

class Element(Object):
    def __init__(self, *args: Any) -> None: ...
    def addChild(self, element: Element) -> None: ...
    def getAttributes(self) -> List[Element.Attribute]: ...
    def getBody(self) -> Any: ...
    def getChildCount(self) -> int: ...
    def getChildren(self) -> List[Element]: ...
    def getName(self) -> AnyStr: ...
    def getObject(self) -> Object: ...
    def getSubName(self) -> AnyStr: ...
    def isSkipRefTracking(self) -> bool: ...
    def setAttribute(self, *args: Any) -> None: ...
    def setBody(self, body: Any) -> None: ...
    def setSkipRefTrack(self, skipRefTracking: bool) -> None: ...

    class Attribute(Object):
        def __init__(self, name: AnyStr, value: AttributeEncoder) -> None: ...
        def getName(self) -> AnyStr: ...
        def getValue(self) -> AttributeEncoder: ...

class SerializationDelegate:
    def isSkipReferenceTracking(self) -> bool: ...
    def serialize(self, context: XMLSerializationContext, obj: Any) -> Element: ...

class XMLSerializationContext(Object):
    def __init__(self, serializer: XMLSerializer) -> None: ...
    def getClassNameMap(self) -> ClassNameResolver: ...
    def getCleanCopy(self, type_: Class) -> Object: ...
    def getRefForElement(self, elm: Element) -> int: ...
    def registerEqualityDelegate(
        self, clazz: Class, delegate: EqualityDelegate
    ) -> None: ...
    def safeEquals(self, foo: Object, bar: Object) -> bool: ...
    def serialize(self, obj: Object) -> Element: ...

class XMLSerializer(Object):
    def __init__(self) -> None: ...
    def addObject(self, obj: Object) -> None: ...
    def addRootAttribute(self, key: AnyStr, value: AnyStr) -> None: ...
    def addSerializationDelegate(
        self, clazz: Class, delegate: SerializationDelegate
    ) -> None: ...
