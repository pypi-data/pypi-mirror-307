from typing import Optional, Union

from dev.coatl.helper.types import AnyStr
from java.util import Date, Locale

def addDays(date: Date, value: int) -> Date: ...
def addHours(date: Date, value: int) -> Date: ...
def addMillis(date: Date, value: int) -> Date: ...
def addMinutes(date: Date, value: int) -> Date: ...
def addMonths(date: Date, value: int) -> Date: ...
def addSeconds(date: Date, value: int) -> Date: ...
def addWeeks(date: Date, value: int) -> Date: ...
def addYears(date: Date, value: int) -> Date: ...
def daysBetween(date_1: Date, date_2: Date) -> int: ...
def format(date: Date, format: AnyStr = ...) -> unicode: ...
def fromMillis(millis: int) -> Date: ...
def getAMorPM(date: Date) -> int: ...
def getDate(year: int, month: int, day: int) -> Date: ...
def getDayOfMonth(date: Date) -> int: ...
def getDayOfWeek(date: Date) -> int: ...
def getDayOfYear(date: Date) -> int: ...
def getHour12(date: Date) -> int: ...
def getHour24(date: Date) -> int: ...
def getMillis(date: Date) -> int: ...
def getMinute(date: Date) -> int: ...
def getMonth(date: Date) -> int: ...
def getQuarter(date: Date) -> int: ...
def getSecond(date: Date) -> int: ...
def getTimezone() -> AnyStr: ...
def getTimezoneOffset(date: Optional[Date] = ...) -> float: ...
def getTimezoneRawOffset() -> float: ...
def getYear(date: Date) -> int: ...
def hoursBetween(date_1: Date, date_2: Date) -> int: ...
def isAfter(date_1: Date, date_2: Date) -> bool: ...
def isBefore(date_1: Date, date_2: Date) -> bool: ...
def isBetween(target_date: Date, start_date: Date, end_date: Date) -> bool: ...
def isDaylightTime(date: Optional[Date] = ...) -> bool: ...
def midnight(date: Date) -> Date: ...
def millisBetween(date_1: Date, date_2: Date) -> long: ...
def minutesBetween(date_1: Date, date_2: Date) -> int: ...
def monthsBetween(date_1: Date, date_2: Date) -> int: ...
def now() -> Date: ...
def parse(
    dateString: AnyStr,
    formatString: AnyStr = ...,
    locale: Union[AnyStr, Locale, None] = ...,
) -> Date: ...
def secondsBetween(date_1: Date, date_2: Date) -> int: ...
def setTime(date: Date, hour: int, minute: int, second: int) -> Date: ...
def toMillis(date: Date) -> long: ...
def weeksBetween(date_1: Date, date_2: Date) -> int: ...
def yearsBetween(date_1: Date, date_2: Date) -> int: ...
