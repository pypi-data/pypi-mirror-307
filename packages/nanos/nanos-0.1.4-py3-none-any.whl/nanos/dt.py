import datetime


def days_after_now(
    days_num: int = 1, tz: datetime.tzinfo | None = datetime.timezone.utc
) -> datetime.datetime:
    return datetime.datetime.now(tz=tz) + datetime.timedelta(days=days_num)


def tomorrow(tz: datetime.tzinfo | None = datetime.timezone.utc) -> datetime.datetime:
    return days_after_now(tz=tz)


def days_before_now(
    days_num: int = 1, tz: datetime.tzinfo | None = datetime.timezone.utc
) -> datetime.datetime:
    return days_after_now(-days_num, tz=tz)


def yesterday(tz: datetime.tzinfo | None = datetime.timezone.utc) -> datetime.datetime:
    return days_before_now(tz=tz)


def yesterday_start(tz: datetime.tzinfo | None = datetime.timezone.utc) -> datetime.datetime:
    return datetime.datetime.combine(yesterday(tz=tz), datetime.datetime.min.time()).replace(
        tzinfo=tz
    )


def yesterday_end(tz: datetime.tzinfo | None = datetime.timezone.utc) -> datetime.datetime:
    return datetime.datetime.combine(yesterday(tz=tz), datetime.datetime.max.time()).replace(
        tzinfo=tz
    )


def today_eod(tz: datetime.tzinfo = datetime.timezone.utc) -> datetime.datetime:
    today = datetime.datetime.now().date()
    return datetime.datetime.combine(today, datetime.datetime.max.time()).replace(tzinfo=tz)
