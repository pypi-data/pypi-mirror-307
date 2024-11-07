from datetime import date as _date
from datetime import datetime as _datetime
from datetime import time as _time
from datetime import timedelta as _timedelta
from datetime import tzinfo as _tzinfo
from typing import Any
from typing import Callable
from zoneinfo import ZoneInfo

DEFAULT_TIMEZONE = ZoneInfo('Asia/Jakarta')


class timedeltautils:

    @classmethod
    def create(cls, days=0, seconds=0, microseconds=0,
               milliseconds=0, minutes=0, hours=0, weeks=0) -> _timedelta:
        timedelta = _timedelta(days=days, seconds=seconds, microseconds=microseconds,
                               milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks)
        return timedelta

    @classmethod
    def total_seconds(cls, timedelta) -> float:
        return timedelta.total_seconds()

    @classmethod
    def days(cls, timedelta) -> int:
        return timedelta.days

    @classmethod
    def seconds(cls, timedelta) -> int:
        return timedelta.seconds

    @classmethod
    def microseconds(cls, timedelta) -> int:
        return timedelta.microseconds

    @classmethod
    def get_timedelta_min(cls) -> _timedelta:
        return _timedelta.min

    @classmethod
    def get_timedelta_max(cls) -> _timedelta:
        return _timedelta.max

    @classmethod
    def get_timedelta_resolution(cls) -> _timedelta:
        return _timedelta.resolution


class dateutils:
    @classmethod
    def create(cls, year, month=None, day=None) -> _date:
        return _date(year=year, month=month, day=day)

    # Additional constructors

    @classmethod
    def fromtimestamp(cls, t) -> _date:
        return _date.fromtimestamp(t)

    @classmethod
    def today(cls) -> _date:
        return _date.today()

    @classmethod
    def fromordinal(cls, n):
        return _date.fromordinal(n)

    @classmethod
    def fromisoformat(cls, date_string):
        return _date.fromisoformat(date_string)

    @classmethod
    def fromisocalendar(cls, year, week, day):
        return _date.fromisocalendar(year=year, week=week, day=day)

    @classmethod
    def ctime(cls, date) -> str:
        return date.ctime()

    @classmethod
    def strftime(cls, date, fmt) -> str:
        return date.strftime(fmt)

    @classmethod
    def isoformat(cls, date) -> str:
        return date.isoformat()

    @classmethod
    def year(cls, date) -> int:
        return date.year

    @classmethod
    def month(cls, date) -> int:
        return date.month

    @classmethod
    def day(cls, date) -> int:
        return date.day

    @classmethod
    def timetuple(cls, date):
        return _date.timetuple()

    @classmethod
    def toordinal(cls, date) -> int:
        return date.toordinal

    @classmethod
    def replace(cls, date, year=None, month=None, day=None):
        return date.replace(year=year, month=month, day=day)

    @classmethod
    def get_date_min(cls) -> _date:
        return _date.min

    @classmethod
    def get_date_max(cls) -> _date:
        return _date.max

    @classmethod
    def get_date_resolution(cls) -> _timedelta:
        return _date.resolution


class timeutils:

    @classmethod
    def create(cls, hour: int = 0, minute: int = 0, second: int = 0, microsecond: int = 0, tzinfo: _tzinfo | None = None, *, fold: int = 0) -> _time:
        time = _time(hour=hour, minute=minute, second=second,
                     microsecond=microsecond, tzinfo=tzinfo, fold=fold)
        return cls.make_aware(time)

    @classmethod
    def make_aware(cls, time: _time) -> _time:
        if time.tzinfo is None:
            return time.replace(tzinfo=DEFAULT_TIMEZONE)
        return time.astimezone(DEFAULT_TIMEZONE)

    @classmethod
    def hour(cls, time: _time) -> int:
        return cls.make_aware(time).hour

    @classmethod
    def minute(cls, time: _time) -> int:
        return cls.make_aware(time).minute

    @classmethod
    def second(cls, time: _time) -> int:
        return cls.make_aware(time).second

    @classmethod
    def microsecond(cls, time: _time) -> int:
        return cls.make_aware(time).microsecond

    @classmethod
    def tzinfo(cls, time: _time) -> _tzinfo | None:
        return time.tzinfo

    @classmethod
    def fold(cls, time: _time) -> int:
        return time.fold

    @classmethod
    def isoformat(cls, time: _time, timespec: str = 'auto') -> str:
        return cls.make_aware(time).isoformat(timespec)

    @classmethod
    def fromisoformat(cls, time_string: str) -> _time:
        res = _time.fromisoformat(time_string)
        return cls.make_aware(res)

    @classmethod
    def strftime(cls, time: _time, fmt: str) -> str:
        return cls.make_aware(time).strftime(fmt)

    @classmethod
    def utcoffset(cls, time: _time) -> _timedelta | None:
        return time.utcoffset()

    @classmethod
    def tzname(cls, time: _time) -> str | None:
        return time.tzname()

    @classmethod
    def dst(cls, time: _time) -> _timedelta | None:
        return time.dst()

    @classmethod
    def replace(cls, time: _time, hour: int | None = None, minute: int | None = None, second: int | None = None, microsecond: int | None = None,
                tzinfo: bool = True, *, fold: int | None = None) -> _time:
        return time.replace(hour, minute, second, microsecond, tzinfo, fold=fold)

    @classmethod
    def get_time_min(cls) -> _time:
        return cls.make_aware(_time.min)

    @classmethod
    def get_time_max(cls) -> _time:
        return cls.make_aware(_time.max)

    @classmethod
    def get_time_resolution(cls) -> _timedelta:
        return cls.make_aware(_time.resolution)


class datetimeutils:

    @classmethod
    def create(cls, year: int, month: int | None = None, day: int | None = None, hour: int = 0, minute: int = 0, second: int = 0, microsecond: int = 0, tzinfo: _tzinfo | None = None, *, fold=0):
        datetime = _datetime(year=year, month=month, day=day, hour=hour, minute=minute,
                             second=second, microsecond=microsecond, tzinfo=tzinfo, fold=fold)
        return cls.make_aware(datetime)

    @classmethod
    def make_aware(cls, datetime: _datetime) -> _datetime:
        if datetime.tzinfo is None:
            return datetime.replace(tzinfo=DEFAULT_TIMEZONE)
        return datetime.astimezone(DEFAULT_TIMEZONE)

    @classmethod
    def today(cls, datetime) -> _datetime:
        return cls.make_aware(datetime).today()

    @classmethod
    def fromordinal(cls, n: int) -> _datetime:
        return _datetime.fromordinal(n)

    @classmethod
    def fromisoformat(cls, date_string: str) -> _datetime:
        return _datetime.fromisoformat(date_string)

    @classmethod
    def fromisocalendar(cls, year: int, week: int, day: int) -> _datetime:
        return _datetime.fromisocalendar(year, week, day)

    @classmethod
    def fromtimestamp(cls, t, tz=None):
        return cls.make_aware(_datetime.fromtimestamp(t, tz=tz))

    @classmethod
    def strftime(cls, datetime: _datetime, fmt: str) -> str:
        return datetime.strftime(fmt)

    @classmethod
    def year(cls, datetime: _datetime) -> int:
        return cls.make_aware(datetime).year

    @classmethod
    def month(cls, datetime: _datetime) -> int:
        return cls.make_aware(datetime).month

    @classmethod
    def day(cls, datetime: _datetime) -> int:
        return cls.make_aware(datetime).day

    @classmethod
    def timetuple(cls, datetime: _datetime) -> Any:
        return cls.make_aware(datetime).timetuple()

    @classmethod
    def toordinal(cls, datetime: _datetime) -> int:
        return cls.make_aware(datetime).toordinal()

    @classmethod
    def weekday(cls, datetime: _datetime) -> int:
        return cls.make_aware(datetime).weekday()

    @classmethod
    def isoweekday(cls, datetime: _datetime) -> int:
        return cls.make_aware(datetime).isoweekday()

    @classmethod
    def isocalendar(cls, datetime: _datetime) -> Any:
        return cls.make_aware(datetime).isocalendar()

    @classmethod
    def hour(cls, datetime: _datetime) -> int:
        return cls.make_aware(datetime).hour

    @classmethod
    def minute(cls, datetime: _datetime) -> int:
        return cls.make_aware(datetime).minute

    @classmethod
    def second(cls, datetime: _datetime) -> int:
        return cls.make_aware(datetime).second

    @classmethod
    def microsecond(cls, datetime: _datetime) -> int:
        return cls.make_aware(datetime).microsecond

    @classmethod
    def now(cls, tz=None) -> _datetime:
        if tz is not None:
            return _datetime.now(tz)
        return cls.make_aware(_datetime.now())

    @classmethod
    def utcnow(cls) -> _datetime:
        return _datetime.utcnow()

    @classmethod
    def combine(cls, date: _date, time: _time, tzinfo: _tzinfo = DEFAULT_TIMEZONE) -> _datetime:
        return cls.make_aware(_datetime.combine(date, time, tzinfo))

    @classmethod
    def timestamp(cls, datetime: _datetime) -> float:
        return cls.make_aware(datetime).timestamp()

    @classmethod
    def utctimetuple(cls, timestamp: float) -> _datetime:
        return _datetime.utcfromtimestamp(timestamp)

    @classmethod
    def date(cls, datetime: _datetime) -> _date:
        return cls.make_aware(datetime).date()

    @classmethod
    def time(cls, datetime: _datetime) -> _time:
        return cls.make_aware(datetime).time()

    @classmethod
    def timetz(cls, datetime: _datetime) -> _time:
        return cls.make_aware(datetime).timetz()

    @classmethod
    def replace(cls, datetime: _datetime, year=None, month=None, day=None, hour=None,
                minute=None, second=None, microsecond=None, tzinfo=True,
                *, fold=None):
        return cls.make_aware(datetime).replace(year, month, day, hour,
                                                minute, second, microsecond, tzinfo, fold=fold)

    @classmethod
    def astimezone(cls, datetime: _datetime, tz=None) -> _datetime:
        return datetime.astimezone(tz)

    @classmethod
    def ctime(cls, datetime: _datetime) -> str:
        return cls.make_aware(datetime).ctime()

    @classmethod
    def isoformat(cls, datetime: _datetime, sep='T', timespec='auto') -> str:
        return cls.make_aware(datetime).isoformat(sep, timespec)

    @classmethod
    def strptime(cls, date_string, format) -> _datetime:
        return cls.make_aware(_datetime.strptime(date_string, format))

    @classmethod
    def utcoffset(cls, datetime: _datetime) -> Callable | _timedelta | None:
        return cls.make_aware(datetime).utcoffset

    @classmethod
    def tzname(cls, datetime: _datetime) -> Callable | _timedelta | None:
        return cls.make_aware(datetime).tzname

    @classmethod
    def dst(cls, datetime: _datetime) -> Callable | _timedelta | None:
        return cls.make_aware(datetime).dst

    @classmethod
    def get_datetime_min(cls) -> _datetime:
        return cls.make_aware(_datetime.min)

    @classmethod
    def get_datetime_max(cls) -> _datetime:
        return cls.make_aware(_datetime.max)

    @classmethod
    def get_datetime_resolution(cls) -> _timedelta:
        return cls.make_aware(_datetime.resolution)


class timezoneutils:

    @classmethod
    def get_current_timezone(cls):
        return DEFAULT_TIMEZONE
