from __future__ import annotations
from typing import Literal, Set, cast

StopLossOrderTimeInForce = Literal["FOK", "GFD", "GTC", "GTD", "IOC"]
STOP_LOSS_ORDER_TIME_IN_FORCE_VALUES: Set[StopLossOrderTimeInForce] = {
    "FOK",
    "GFD",
    "GTC",
    "GTD",
    "IOC",
}


def check_stop_loss_order_time_in_force(value: str) -> StopLossOrderTimeInForce:
    if value in STOP_LOSS_ORDER_TIME_IN_FORCE_VALUES:
        return cast(StopLossOrderTimeInForce, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {STOP_LOSS_ORDER_TIME_IN_FORCE_VALUES!r}"
    )
