from __future__ import annotations

import datetime
import math
import time
import typing as t

DEFAULT_TIMER_PRECISION: t.Final = 2


class Timer:
    def __init__(self, precision: int = DEFAULT_TIMER_PRECISION) -> None:
        self.precision = precision
        self.start: float | None = None
        self.end: float | None = None

    def __enter__(self) -> Timer:
        self.start = time.time()
        return self

    def __exit__(self, *args: t.Any) -> None:
        self.end = time.time()

    def __str__(self) -> str:
        return self.verbose()

    def __repr__(self) -> str:
        return f"<Timer [start={self.start}, end={self.end}]>"

    def verbose(self) -> str:
        fraction_seconds, whole_seconds = math.modf(self.elapsed)
        rounded_fraction = round(fraction_seconds, self.precision)
        if rounded_fraction >= 1:
            whole_seconds += 1
            formatted_fraction = "0" * self.precision
        elif fraction_seconds == 0:
            formatted_fraction = "0" * self.precision
        else:
            fraction = int(rounded_fraction * 10**self.precision)
            formatted_fraction = str(fraction).zfill(self.precision)
        return f"{datetime.timedelta(seconds=whole_seconds)}.{formatted_fraction}"

    @property
    def elapsed(self) -> float:
        if not self.start:
            return 0.0
        return (self.end or time.time()) - self.start
