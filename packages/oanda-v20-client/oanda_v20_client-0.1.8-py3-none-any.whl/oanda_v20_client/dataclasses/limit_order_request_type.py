from __future__ import annotations
from typing import Literal, Set, cast

LimitOrderRequestType = Literal[
    "FIXED_PRICE",
    "LIMIT",
    "MARKET",
    "MARKET_IF_TOUCHED",
    "STOP",
    "STOP_LOSS",
    "TAKE_PROFIT",
    "TRAILING_STOP_LOSS",
]
LIMIT_ORDER_REQUEST_TYPE_VALUES: Set[LimitOrderRequestType] = {
    "FIXED_PRICE",
    "LIMIT",
    "MARKET",
    "MARKET_IF_TOUCHED",
    "STOP",
    "STOP_LOSS",
    "TAKE_PROFIT",
    "TRAILING_STOP_LOSS",
}


def check_limit_order_request_type(value: str) -> LimitOrderRequestType:
    if value in LIMIT_ORDER_REQUEST_TYPE_VALUES:
        return cast(LimitOrderRequestType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {LIMIT_ORDER_REQUEST_TYPE_VALUES!r}"
    )
