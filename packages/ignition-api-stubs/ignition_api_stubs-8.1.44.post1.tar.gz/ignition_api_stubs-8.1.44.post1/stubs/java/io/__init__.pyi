from typing import Any, Optional, Union

from dev.coatl.helper.types import AnyStr
from java.lang import (
    Appendable,
    AutoCloseable,
    CharSequence,
    Exception,
    Object,
    Readable,
    Throwable,
)
from java.nio.charset import Charset, CharsetDecoder

class Closeable(AutoCloseable):
    def close(self) -> None: ...

class Flushable:
    def flush(self) -> None: ...

class File(Object):
    pathSeparator: AnyStr
    pathSeparatorChar: AnyStr
    separator: AnyStr
    separatorChar: AnyStr
    def __init__(self, *args: Any) -> None: ...

class FileDescriptor(Object):
    def sync(self) -> None: ...
    def valid(self) -> bool: ...

class OutputStream(Object, Closeable, Flushable):
    def close(self) -> None: ...
    def flush(self) -> None: ...
    @staticmethod
    def nullOutputStream() -> OutputStream: ...
    def write(self, *args: Any) -> None: ...

class FileOutputStream(OutputStream):
    def __init__(self, *args: Any) -> None: ...
    def getChannel(self) -> Any: ...
    def getFD(self) -> FileDescriptor: ...

class FilterOutputStream(OutputStream):
    def __init__(self, out: OutputStream) -> None: ...

class DataOutputStream(FilterOutputStream):
    out: OutputStream
    def __init__(self, out: OutputStream) -> None: ...
    def size(self) -> int: ...
    def writeBoolean(self, v: bool) -> None: ...
    def writeByte(self, v: int) -> None: ...
    def writeBytes(self, s: AnyStr) -> None: ...
    def writeChar(self, v: int) -> None: ...
    def writeChars(self, s: AnyStr) -> None: ...
    def writeDouble(self, v: float) -> None: ...
    def writeFloat(self, v: float) -> None: ...
    def writeInt(self, v: int) -> None: ...
    def writeLong(self, v: long) -> None: ...
    def writeShort(self, v: int) -> None: ...
    def writeUTF(self, s: AnyStr) -> None: ...

class PrintStream(FilterOutputStream):
    def __init__(self, *args: Any) -> None: ...
    def append(self, *args: Any) -> PrintStream: ...
    def checkError(self) -> bool: ...
    def format(self, *args: Any) -> PrintStream: ...
    def print(self, arg: Any) -> None: ...
    def printf(self, *args: Any) -> None: ...
    def println(self, arg: Any) -> None: ...

class InputStream(Object, Closeable):
    def available(self) -> int: ...
    def close(self) -> None: ...
    def mark(self, readlimit: int) -> None: ...
    def markSupported(self) -> bool: ...
    @staticmethod
    def nullInputStream() -> InputStream: ...
    def read(self, *args: Any) -> int: ...
    def readAllBytes(self) -> bytearray: ...
    def readNBytes(self, *args: Any) -> int: ...
    def reset(self) -> None: ...
    def skip(self, n: long) -> long: ...
    def transferTo(self, out: OutputStream) -> long: ...

class IOException(Exception):
    def __init__(
        self, message: Optional[str] = ..., cause: Optional[Throwable] = ...
    ) -> None: ...

class Reader(Object, Readable, Closeable):
    def __init__(self, lock: Optional[Object] = ...) -> None: ...
    def close(self) -> None: ...
    def mark(self, readAheadLimit: int) -> None: ...
    def markSupported(self) -> bool: ...
    @staticmethod
    def nullReader() -> Reader: ...
    def read(self, *args: Any) -> int: ...
    def ready(self) -> bool: ...
    def reset(self) -> None: ...
    def skip(self, n: long) -> long: ...
    def transferTo(self, out: Writer) -> long: ...

class BufferedReader(Reader):
    def __init__(self, in_: Reader, sz: Optional[int] = ...) -> None: ...

class InputStreamReader(Reader):
    def __init__(
        self,
        in_: InputStream,
        arg: Optional[Union[AnyStr, Charset, CharsetDecoder]] = ...,
    ) -> None: ...
    def getEncoding(self) -> AnyStr: ...

class Writer(Object, Appendable, Closeable, Flushable):
    def append(
        self, c_csq: Union[CharSequence, str], start: int = ..., end: int = ...
    ) -> Writer: ...
    def close(self) -> None: ...
    def flush(self) -> None: ...
    @staticmethod
    def nullWriter() -> Writer: ...
    def write(self, *args: Any) -> None: ...

class BufferedWriter(Writer):
    def __init__(self, out: Writer, sz: Optional[int] = ...) -> None: ...

class PrintWriter(Writer):
    def __init__(self, *args: Any) -> None: ...
    def append(
        self, c_csq: Union[CharSequence, str], start: int = ..., end: int = ...
    ) -> PrintWriter: ...
    def checkError(self) -> bool: ...
    def format(self, *args: Any) -> PrintWriter: ...
    def print(self, arg: Any) -> None: ...
    def printf(self, *args: Any) -> PrintWriter: ...
    def println(self, arg: Any) -> None: ...
    def write(self, *args: Any) -> None: ...
