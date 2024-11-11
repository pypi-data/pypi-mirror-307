from __future__ import annotations
from typing import Literal, Set, cast

TakeProfitOrderRequestTimeInForce = Literal["FOK", "GFD", "GTC", "GTD", "IOC"]
TAKE_PROFIT_ORDER_REQUEST_TIME_IN_FORCE_VALUES: Set[
    TakeProfitOrderRequestTimeInForce
] = {"FOK", "GFD", "GTC", "GTD", "IOC"}


def check_take_profit_order_request_time_in_force(
    value: str,
) -> TakeProfitOrderRequestTimeInForce:
    if value in TAKE_PROFIT_ORDER_REQUEST_TIME_IN_FORCE_VALUES:
        return cast(TakeProfitOrderRequestTimeInForce, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {TAKE_PROFIT_ORDER_REQUEST_TIME_IN_FORCE_VALUES!r}"
    )
