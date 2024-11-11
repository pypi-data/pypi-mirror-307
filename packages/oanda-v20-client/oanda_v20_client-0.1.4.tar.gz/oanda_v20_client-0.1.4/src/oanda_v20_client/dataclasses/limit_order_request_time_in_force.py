from __future__ import annotations
from typing import Literal, Set, cast

LimitOrderRequestTimeInForce = Literal["FOK", "GFD", "GTC", "GTD", "IOC"]
LIMIT_ORDER_REQUEST_TIME_IN_FORCE_VALUES: Set[LimitOrderRequestTimeInForce] = {
    "FOK",
    "GFD",
    "GTC",
    "GTD",
    "IOC",
}


def check_limit_order_request_time_in_force(value: str) -> LimitOrderRequestTimeInForce:
    if value in LIMIT_ORDER_REQUEST_TIME_IN_FORCE_VALUES:
        return cast(LimitOrderRequestTimeInForce, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {LIMIT_ORDER_REQUEST_TIME_IN_FORCE_VALUES!r}"
    )
