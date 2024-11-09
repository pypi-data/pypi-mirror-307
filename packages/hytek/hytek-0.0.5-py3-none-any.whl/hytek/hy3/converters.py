import datetime


__all__ = ("date", "time")


def date(data: str) -> datetime.date:
    month = int(data[:2])
    day = int(data[2:4])
    year = int(data[-4:])
    return datetime.date(year, month, day)


def time(data: str) -> datetime.time:
    _time, ampm = data.split(" ")
    hours, minutes = _time.split(":")
    hours = int(hours)
    minutes = int(minutes)
    if ampm == "PM" and hours != 12:
        hours += 12
    return datetime.time(hours, minutes)
