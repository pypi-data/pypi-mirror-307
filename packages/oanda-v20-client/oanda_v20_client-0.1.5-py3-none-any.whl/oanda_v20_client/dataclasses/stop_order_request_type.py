from __future__ import annotations
from typing import Literal, Set, cast

StopOrderRequestType = Literal[
    "FIXED_PRICE",
    "LIMIT",
    "MARKET",
    "MARKET_IF_TOUCHED",
    "STOP",
    "STOP_LOSS",
    "TAKE_PROFIT",
    "TRAILING_STOP_LOSS",
]
STOP_ORDER_REQUEST_TYPE_VALUES: Set[StopOrderRequestType] = {
    "FIXED_PRICE",
    "LIMIT",
    "MARKET",
    "MARKET_IF_TOUCHED",
    "STOP",
    "STOP_LOSS",
    "TAKE_PROFIT",
    "TRAILING_STOP_LOSS",
}


def check_stop_order_request_type(value: str) -> StopOrderRequestType:
    if value in STOP_ORDER_REQUEST_TYPE_VALUES:
        return cast(StopOrderRequestType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {STOP_ORDER_REQUEST_TYPE_VALUES!r}"
    )
