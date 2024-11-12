from __future__ import annotations
from typing import Literal, Set, cast

TimeInForce = Literal["FOK", "GFD", "GTC", "GTD", "IOC"]
TIME_IN_FORCE_VALUES: Set[TimeInForce] = {"FOK", "GFD", "GTC", "GTD", "IOC"}


def check_time_in_force(value: str) -> TimeInForce:
    if value in TIME_IN_FORCE_VALUES:
        return cast(TimeInForce, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {TIME_IN_FORCE_VALUES!r}"
    )
