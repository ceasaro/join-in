from datetime import datetime, timezone

from django.utils.dateparse import parse_date


def utc_now():
    return datetime.now(tz=timezone.utc)


def datetime_to_millis(dt: datetime) -> int:
    """Convert datetime object to milliseconds (UTC Epoch)
    Args:
        dt (datetime): datetime object to convert (if tzinfo not set, will address as UTC)

    Returns:
        int: milliseconds representation of the given date object.

    Raises:
        TypeError: if no instancfe of datetime is passed.
    """
    return int(datetime_to_timestamp(dt) * 1000)


def datetime_to_timestamp(dt: datetime) -> float:
    """Convert date/datetime object into timestamp in seconds (UTC Epoch)
    Args:
        dt (datetime | date): date object to convert (if tzinfo not set, will address as UTC)

    Returns:
        float | None: timestamp representation of the given date object.

    Raises:
        TypeError: if no instancfe of datetime is passed.
    """

    if not isinstance(dt, datetime):
        raise TypeError("Can only convert datetime objects to timestamp")

    if not dt.tzinfo:
        dt = dt.replace(tzinfo=timezone.utc)
    return datetime.timestamp(dt)


def timestamp_to_datetime(timestamp: float) -> datetime:
    """convert epoch timestamp in seconds to datetime object with UTC timezone

    Args:
        timestamp (float): epoch timestamp in seconds

    Returns:
        datetime: datetime object represent the input epoch. object timezone is set to UTC
    """
    _datetime = datetime.utcfromtimestamp(timestamp)
    return _datetime.replace(tzinfo=timezone.utc)


def millis_to_datetime(millis: float) -> datetime:
    """convert epoch timestamp in millis to datetime object with UTC timezone

    Args:
        millis (float): epoch timestamp in milliseconds

    Returns:
        datetime: datetime object represent the input epoch. object timezone is set to UTC
    """
    return timestamp_to_datetime(millis / 1000)


def str_to_datetime(date_str: str) -> datetime:
    """convert time from string into a datetime object.

    Args:
        date_str (str): Any date/time string using the supported formats.


    Raises:
        ParserError: Raised for invalid or unknown string format, if the provided
        OverflowError: Raised if the parsed date exceeds the largest valid C integer on your system.
        TypeError: Raised for non-string or character stream input.

    Returns:
        datetime: Returns a `datetime.datetime` object
    """
    return parse_date(date_str)


def str_to_timestamp(date_str: str) -> float:
    """convert time represented as string to UTC timestamp

    Args:
        date_str (str): datetime string

    Returns:
        float: UTC timestamp
    """
    return datetime_to_timestamp(str_to_datetime(date_str))
