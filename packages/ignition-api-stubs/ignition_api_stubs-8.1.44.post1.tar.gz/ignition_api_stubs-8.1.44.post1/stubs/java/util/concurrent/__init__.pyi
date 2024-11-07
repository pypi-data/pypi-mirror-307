from typing import Any, List, Optional

from java.lang import Comparable, Enum, Object, Thread
from java.time.temporal import ChronoUnit

class Delayed(Comparable):
    def compareTo(self, o: Any) -> int: ...
    def getDelay(self, unit: TimeUnit) -> long: ...

class Future:
    def cancel(self, mayInterruptIfRunning: bool) -> bool: ...
    def get(
        self, timeout: Optional[long] = ..., unit: Optional[TimeUnit] = ...
    ) -> Any: ...
    def isCancelled(self) -> bool: ...
    def isDone(self) -> bool: ...

class ScheduledFuture(Delayed, Future):
    def cancel(self, mayInterruptIfRunning: bool) -> bool: ...
    def compareTo(self, o: Any) -> int: ...
    def get(
        self, timeout: Optional[long] = ..., unit: Optional[TimeUnit] = ...
    ) -> Any: ...
    def getDelay(self, unit: TimeUnit) -> long: ...
    def isCancelled(self) -> bool: ...
    def isDone(self) -> bool: ...

class CompletableFuture(Object):
    def __init__(self) -> None: ...

class TimeUnit(Enum):
    DAYS: TimeUnit
    HOURS: TimeUnit
    MICROSECONDS: TimeUnit
    MILLISECONDS: TimeUnit
    MINUTES: TimeUnit
    NANOSECONDS: TimeUnit
    SECONDS: TimeUnit
    def convert(self, *args: Any) -> long: ...
    @staticmethod
    def of(chronoUnit: ChronoUnit) -> TimeUnit: ...
    def sleep(self, timeout: long) -> None: ...
    def timedJoin(self, thread: Thread, timeout: long) -> None: ...
    def timedWait(self, obj: Object, timeout: long) -> None: ...
    def toChronoUnit(self) -> ChronoUnit: ...
    def toDays(self, duration: long) -> long: ...
    def toHours(self, duration: long) -> long: ...
    def toMicros(self, duration: long) -> long: ...
    def toMillis(self, duration: long) -> long: ...
    def toMinutes(self, duration: long) -> long: ...
    def toNanos(self, duration: long) -> long: ...
    def toSeconds(self, duration: long) -> long: ...
    @staticmethod
    def values() -> List[TimeUnit]: ...
