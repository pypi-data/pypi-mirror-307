from __future__ import annotations
from typing import Literal, Set, cast

LimitOrderTimeInForce = Literal["FOK", "GFD", "GTC", "GTD", "IOC"]
LIMIT_ORDER_TIME_IN_FORCE_VALUES: Set[LimitOrderTimeInForce] = {
    "FOK",
    "GFD",
    "GTC",
    "GTD",
    "IOC",
}


def check_limit_order_time_in_force(value: str) -> LimitOrderTimeInForce:
    if value in LIMIT_ORDER_TIME_IN_FORCE_VALUES:
        return cast(LimitOrderTimeInForce, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {LIMIT_ORDER_TIME_IN_FORCE_VALUES!r}"
    )
