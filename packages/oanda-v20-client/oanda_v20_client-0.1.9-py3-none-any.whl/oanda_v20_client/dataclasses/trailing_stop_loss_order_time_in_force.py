from __future__ import annotations
from typing import Literal, Set, cast

TrailingStopLossOrderTimeInForce = Literal["FOK", "GFD", "GTC", "GTD", "IOC"]
TRAILING_STOP_LOSS_ORDER_TIME_IN_FORCE_VALUES: Set[TrailingStopLossOrderTimeInForce] = {
    "FOK",
    "GFD",
    "GTC",
    "GTD",
    "IOC",
}


def check_trailing_stop_loss_order_time_in_force(
    value: str,
) -> TrailingStopLossOrderTimeInForce:
    if value in TRAILING_STOP_LOSS_ORDER_TIME_IN_FORCE_VALUES:
        return cast(TrailingStopLossOrderTimeInForce, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {TRAILING_STOP_LOSS_ORDER_TIME_IN_FORCE_VALUES!r}"
    )
